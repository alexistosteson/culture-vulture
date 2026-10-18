#!/usr/bin/env python3
"""send_guard.py — the only door out of the act-now mailbox.

The act-now reader reads untrusted marketing mail with an agent that can also
send mail. An email written to steer that agent could ask it to write to
someone else. Telling the agent not to is an instruction; this is the
enforcement. It runs as a PreToolUse hook (see .claude/settings.json) before
every MCP tool call, and for any tool that can put mail in front of anyone it
allows exactly one shape: a new message to the owner's one address, with no
copies, no attachments, no draft and no thread.

    python3 scripts/send_guard.py              # hook mode: tool call on stdin
    python3 scripts/send_guard.py --self-test  # offline cases, run by verify.sh

The owner's address is never written in this repository — it is public. It is
read from the environment variable ACT_NOW_OWNER_ADDRESS, which is set in the
routine's private settings on claude.ai. When it is unset, or does not look like
one address, every send is refused: the guard fails closed, so a session
without the setting (any local session, any other routine) can send nothing.

Exit 0 — allowed (or not a mail-sending tool).
Exit 2 — refused; the reason is on stderr and goes back to the agent. The
         reason never names the owner's address.
"""

import json
import os
import re
import subprocess
import sys

OWNER_ENV = "ACT_NOW_OWNER_ADDRESS"

# Tools that can deliver mail, or stage mail for delivery. Matched on the last
# segment of the tool name, so the server's name (a UUID locally, "Gmail" in
# the routine) does not matter. Anything whose name merely mentions sending is
# gated too: a renamed or newly added tool is refused, not waved through.
SEND_TOOLS = {"send_message", "send_draft", "reply", "reply_all", "forward",
              "create_draft", "update_draft"}
SEND_WORDS = re.compile(r"send|reply|forward|draft", re.I)

# The fields a send_message call may carry. Everything else must be empty.
ALLOWED_FIELDS = {"to", "subject", "body", "htmlBody"}
ADDRESS = re.compile(r"^[^@\s,;<>\"']+@[^@\s,;<>\"']+\.[^@\s,;<>\"']+$")


# The desktop app's own session tools (messages between Claude sessions on this
# Mac) send no email and exist only locally; the routine has none.
LOCAL_APP_PREFIX = "mcp__ccd_"


def is_mail_tool(name):
    if name.startswith(LOCAL_APP_PREFIX):
        return False
    last = name.rsplit("__", 1)[-1]
    return last in SEND_TOOLS or bool(SEND_WORDS.search(last))


def decide(tool_name, tool_input, owner):
    """Return None to allow, or the reason for refusing."""
    if not tool_name.startswith("mcp__") or not is_mail_tool(tool_name):
        return None
    if not owner or not ADDRESS.match(owner.strip()):
        return f"{OWNER_ENV} is not set to one address here, so no mail may be sent"
    if tool_name.rsplit("__", 1)[-1] != "send_message":
        return "only send_message is allowed; reply, forward and drafts are not"
    if not isinstance(tool_input, dict):
        return "the send has no readable fields"
    extra = sorted(k for k, v in tool_input.items()
                   if k not in ALLOWED_FIELDS and v not in (None, "", [], False))
    if extra:
        return f"a send may not carry: {', '.join(extra)}"
    to = tool_input.get("to")
    if not (isinstance(to, list) and len(to) == 1 and isinstance(to[0], str)):
        return "a send must have exactly one recipient"
    if to[0].strip().lower() != owner.strip().lower():
        return "the recipient is not the owner's address"
    if not (tool_input.get("body") or tool_input.get("htmlBody")):
        return "a send must have a body"
    return None


def hook():
    try:
        event = json.load(sys.stdin)
        name = event.get("tool_name", "")
        tool_input = event.get("tool_input", {})
    except Exception:  # unreadable input is refused, whatever it was
        print("send_guard: could not read the tool call; refused", file=sys.stderr)
        return 2
    reason = decide(name, tool_input, os.environ.get(OWNER_ENV, ""))
    if reason is None:
        return 0
    print(f"send_guard refused {name}: {reason}. Act-now alerts may only be "
          "sent to the owner's one address.", file=sys.stderr)
    return 2


# Cases whose answers are recorded here. The owner address is a placeholder on
# a reserved domain; a refused case must stay refused.
FAKE = "owner@example.invalid"
CASES = [
    # (name, tool, input, owner, allowed?)
    ("owner only", "mcp__Gmail__send_message",
     {"to": [FAKE], "subject": "s", "body": "b"}, FAKE, True),
    ("owner, case and space differ", "mcp__Gmail__send_message",
     {"to": [" Owner@Example.Invalid "], "subject": "s", "htmlBody": "<p>b</p>"}, FAKE, True),
    ("local UUID server name", "mcp__ad1a6979-fb5f__send_message",
     {"to": [FAKE], "body": "b"}, FAKE, True),
    ("empty optional fields are fine", "mcp__Gmail__send_message",
     {"to": [FAKE], "body": "b", "cc": [], "bcc": [], "includeSignature": False}, FAKE, True),
    ("someone else", "mcp__Gmail__send_message",
     {"to": ["attacker@example.com"], "body": "b"}, FAKE, False),
    ("owner plus someone", "mcp__Gmail__send_message",
     {"to": [FAKE, "attacker@example.com"], "body": "b"}, FAKE, False),
    ("two addresses in one string", "mcp__Gmail__send_message",
     {"to": [FAKE + ", attacker@example.com"], "body": "b"}, FAKE, False),
    ("cc", "mcp__Gmail__send_message",
     {"to": [FAKE], "cc": ["attacker@example.com"], "body": "b"}, FAKE, False),
    ("bcc", "mcp__Gmail__send_message",
     {"to": [FAKE], "bcc": ["attacker@example.com"], "body": "b"}, FAKE, False),
    ("send a prepared draft", "mcp__Gmail__send_message",
     {"draftId": "r123"}, FAKE, False),
    ("attachment", "mcp__Gmail__send_message",
     {"to": [FAKE], "body": "b", "attachments": [{"content": "eA=="}]}, FAKE, False),
    ("threaded into a venue's thread", "mcp__Gmail__send_message",
     {"to": [FAKE], "body": "b", "replyThreadId": "t1"}, FAKE, False),
    ("unknown field", "mcp__Gmail__send_message",
     {"to": [FAKE], "body": "b", "from": "x@example.com"}, FAKE, False),
    ("no recipient", "mcp__Gmail__send_message", {"body": "b"}, FAKE, False),
    ("to as a bare string", "mcp__Gmail__send_message",
     {"to": FAKE, "body": "b"}, FAKE, False),
    ("no body", "mcp__Gmail__send_message", {"to": [FAKE], "subject": "s"}, FAKE, False),
    ("reply", "mcp__Gmail__reply", {"messageId": "m1", "body": "b"}, FAKE, False),
    ("forward", "mcp__Gmail__forward", {"messageId": "m1", "to": [FAKE]}, FAKE, False),
    ("create draft", "mcp__Gmail__create_draft", {"to": [FAKE], "body": "b"}, FAKE, False),
    ("unknown sending tool", "mcp__Other__send_email", {"to": [FAKE]}, FAKE, False),
    ("owner setting missing", "mcp__Gmail__send_message",
     {"to": [FAKE], "body": "b"}, "", False),
    ("owner setting is two addresses", "mcp__Gmail__send_message",
     {"to": [FAKE], "body": "b"}, FAKE + "," + "attacker@example.com", False),
    ("the desktop app's session messages", "mcp__ccd_session_mgmt__send_message",
     {"message": "x"}, "", True),
    ("reading mail is not gated", "mcp__Gmail__search_threads", {"query": "x"}, "", True),
    ("a non-MCP tool is not gated", "Read", {"file_path": "/x"}, "", True),
]


def self_test():
    bad = 0
    for label, tool, tool_input, owner, want in CASES:
        got = decide(tool, tool_input, owner) is None
        if got != want:
            bad += 1
            print(f"FAIL  {label}: expected {'allow' if want else 'refuse'}")
    # The hook itself, end to end through stdin, with the address only in the
    # environment: a refusal must exit 2 and must not echo the address.
    me = os.path.abspath(__file__)
    env = {**os.environ, OWNER_ENV: FAKE}
    for tool_input, want_rc in (({"to": [FAKE], "body": "b"}, 0),
                                ({"to": ["attacker@example.com"], "body": "b"}, 2)):
        r = subprocess.run([sys.executable, me], env=env, capture_output=True, text=True,
                           input=json.dumps({"tool_name": "mcp__Gmail__send_message",
                                             "tool_input": tool_input}), check=False)
        if r.returncode != want_rc or FAKE in r.stdout + r.stderr:
            bad += 1
            print(f"FAIL  hook mode: exit {r.returncode}, expected {want_rc}, or address echoed")
    r = subprocess.run([sys.executable, me], env=env, input="not json",
                       capture_output=True, text=True, check=False)
    if r.returncode != 2:
        bad += 1
        print("FAIL  hook mode: unreadable input was not refused")
    # The wiring: the guard is useless unless the project settings call it for
    # every MCP tool. Check the matcher catches both server-name forms.
    try:
        root = os.path.dirname(os.path.dirname(me))
        settings = json.load(open(os.path.join(root, ".claude", "settings.json")))
        wired = [h for h in settings["hooks"]["PreToolUse"]
                 if any("send_guard.py" in c.get("command", "") for c in h.get("hooks", []))]
        if not wired or not all(re.fullmatch(wired[0]["matcher"], t) for t in
                                ("mcp__Gmail__send_message", "mcp__ad1a6979-fb5f__forward")):
            raise ValueError("matcher does not cover every MCP tool")
    except Exception as e:  # any failure to find the wiring is the finding
        bad += 1
        print(f"FAIL  .claude/settings.json does not wire the guard: {e}")
    n = len(CASES) + 4
    print(f"send_guard self-test: {n - bad}/{n} cases as recorded")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(self_test() if sys.argv[1:] == ["--self-test"] else hook())
