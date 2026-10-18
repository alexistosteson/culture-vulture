#!/usr/bin/env python3
"""proposals.py — the record of what the weekly run has proposed, and what became of it.

The weekly run proposes changes to the venue list and the brief as pull
requests (specs/proposals-as-pull-requests.md). proposals/ledger.json holds one
record per proposal. It is how the run avoids proposing a declined change
again, what the trial review counts from, and where the weekly note reads each
proposal's state.

    python3 scripts/proposals.py --check              # validate the ledger (offline)
    python3 scripts/proposals.py --status             # compare it with GitHub (network)
    python3 scripts/proposals.py --status --write --week <window_start>
                                                      # ... and record new outcomes
    python3 scripts/proposals.py --add <id> <kind> <summary>
    python3 scripts/proposals.py --self-test          # offline cases, run by verify.sh

The run has no GitHub tools, so outcomes are read with `git ls-remote`. The
proposals workflow records each closed pull request as a tag,
proposal-outcome/<week>/<slug>/<outcome>, and only then deletes its
proposal/<week>/<slug> branch. So: a tag gives the outcome; a branch with no
tag is waiting; a branch gone with no tag is an error, never a guess.

Exit 0 — clean. Exit 1 — findings, printed one per line. Exit 2 — could not
check (ledger unreadable, remote unreachable, or the self-test failed).
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

LEDGER = Path(__file__).resolve().parent.parent / "proposals" / "ledger.json"
KINDS = ("upkeep", "new-venue", "site-change")
DECIDED = ("accepted", "accepted-changed", "declined")
STATUSES = ("waiting", *DECIDED)
FIELDS = {"id", "week", "kind", "summary", "status", "decided_week"}
DATE = r"\d{4}-\d{2}-\d{2}"
ID = re.compile(rf"^({DATE})/([a-z0-9][a-z0-9-]*)$")
BRANCH = re.compile(rf"^refs/heads/proposal/({DATE}/[a-z0-9][a-z0-9-]*)$")
TAG = re.compile(rf"^refs/tags/proposal-outcome/({DATE}/[a-z0-9][a-z0-9-]*)/([a-z-]+)$")


def slug_fits(kind: str, slug: str) -> bool:
    """A slug names its kind, so a branch name alone says what it proposes."""
    return slug == "upkeep" if kind == "upkeep" else slug.startswith(kind + "-")


def check(records: object) -> list[str]:
    """Every way a ledger can be malformed. Empty means clean."""
    if not isinstance(records, list):
        return ["the ledger is not a list"]
    found, seen = [], set()
    for i, r in enumerate(records):
        where = f"record {i + 1}"
        if not isinstance(r, dict):
            found.append(f"{where}: not an object")
            continue
        if set(r) != FIELDS:
            extra, missing = sorted(set(r) - FIELDS), sorted(FIELDS - set(r))
            found.append(f"{where}: fields wrong (extra {extra}, missing {missing})")
            continue
        where = f"{where} ({r['id']})"
        m = ID.match(str(r["id"]))
        if not m:
            found.append(f"{where}: id is not <YYYY-MM-DD>/<slug>")
            continue
        if r["id"] in seen:
            found.append(f"{where}: duplicate id")
        seen.add(r["id"])
        week, slug = m.groups()
        if r["week"] != week:
            found.append(f"{where}: week {r['week']} does not match its id")
        if r["kind"] not in KINDS:
            found.append(f"{where}: kind {r['kind']!r} is not one of {', '.join(KINDS)}")
        elif not slug_fits(r["kind"], slug):
            found.append(f"{where}: slug does not name its kind {r['kind']}")
        if not isinstance(r["summary"], str) or not r["summary"].strip():
            found.append(f"{where}: no summary")
        elif "`" in r["summary"]:
            found.append(f"{where}: summary has backticks, and it is shown in public")
        if r["status"] not in STATUSES:
            found.append(f"{where}: status {r['status']!r} is not one of {', '.join(STATUSES)}")
        elif (r["status"] == "waiting") != (r["decided_week"] is None):
            found.append(f"{where}: decided_week must be null exactly when waiting")
        elif r["decided_week"] is not None and (
            not re.fullmatch(DATE, str(r["decided_week"])) or r["decided_week"] < week
        ):
            found.append(f"{where}: decided_week {r['decided_week']} is not a date on or after {week}")
    return found


def read_remote(ls_remote: str) -> tuple[set[str], dict[str, list[str]]]:
    """Branches waiting, and outcome tags, from `git ls-remote` output."""
    branches, outcomes = set(), {}
    for line in ls_remote.splitlines():
        ref = line.split("\t")[-1].strip()
        if m := BRANCH.match(ref):
            branches.add(m.group(1))
        elif (m := TAG.match(ref)) and not ref.endswith("^{}"):
            outcomes.setdefault(m.group(1), []).append(m.group(2))
    return branches, outcomes


def resolve(records: list[dict], ls_remote: str) -> tuple[dict[str, str], list[str]]:
    """What GitHub says each record's status is, and every disagreement."""
    branches, outcomes = read_remote(ls_remote)
    status, found = {}, []
    for r in records:
        pid, tags = r["id"], outcomes.get(r["id"], [])
        if len(tags) > 1:
            found.append(f"{pid}: more than one outcome recorded ({', '.join(sorted(tags))})")
            continue
        if tags and tags[0] not in DECIDED:
            found.append(f"{pid}: outcome tag {tags[0]!r} is not one of {', '.join(DECIDED)}")
            continue
        now = tags[0] if tags else "waiting" if pid in branches else None
        if now is None:
            found.append(f"{pid}: its branch is gone and no outcome was recorded")
            continue
        if r["status"] != "waiting" and r["status"] != now:
            found.append(f"{pid}: the ledger says {r['status']}, GitHub says {now}")
            continue
        status[pid] = now
    return status, found


def load() -> list[dict]:
    return json.loads(LEDGER.read_text())


def save(records: list[dict]) -> None:
    lines = ",\n".join(" " + json.dumps(r, ensure_ascii=False) for r in records)
    LEDGER.write_text(f"[\n{lines}\n]\n" if records else "[]\n")


def ls_remote() -> str:
    return subprocess.run(
        ["git", "ls-remote", "origin", "refs/heads/proposal/*", "refs/tags/proposal-outcome/*"],
        check=True, capture_output=True, text=True, timeout=60,
    ).stdout


def cmd_status(write: bool, week: str | None) -> int:
    records = load()
    if found := check(records):
        print("\n".join(found))
        return 1
    status, found = resolve(records, ls_remote())
    changed = 0
    for r in records:
        now = status.get(r["id"])
        mark = "" if now in (None, r["status"]) else f"  -> {now}"
        print(f"  {r['status']:<17} {r['id']}{mark}")
        if mark and write:
            r["status"], r["decided_week"] = now, week
            changed += 1
    if write and changed:
        save(records)
    print(f"checked {len(records)} records against GitHub; {changed} newly decided"
          + ("" if write else " (not written)"))
    print("\n".join(found))
    return 1 if found else 0


def cmd_add(pid: str, kind: str, summary: str) -> int:
    records = load()
    m = ID.match(pid)
    records.append({"id": pid, "week": m.group(1) if m else "", "kind": kind,
                    "summary": summary, "status": "waiting", "decided_week": None})
    if found := check(records):
        print("\n".join(found))
        return 1
    save(records)
    print(f"added {pid}; the ledger has {len(records)} records")
    return 0


def self_test() -> int:
    """Replay recorded cases. Each planted defect must be caught."""
    def rec(pid, kind, status="waiting", decided=None, **over):
        r = {"id": pid, "week": pid[:10], "kind": kind, "summary": "Watch a venue",
             "status": status, "decided_week": decided}
        return {**r, **over}

    clean = [
        rec("2026-10-26/upkeep", "upkeep", "accepted", "2026-11-02"),
        rec("2026-10-26/new-venue-montalvo", "new-venue"),
        rec("2026-10-26/site-change-coast", "site-change", "declined", "2026-11-02"),
        rec("2026-11-02/upkeep", "upkeep", "accepted-changed", "2026-11-09"),
    ]
    remote = "\n".join([
        "a1\trefs/tags/proposal-outcome/2026-10-26/upkeep/accepted",
        "b2\trefs/heads/proposal/2026-10-26/new-venue-montalvo",
        "c3\trefs/tags/proposal-outcome/2026-10-26/site-change-coast/declined",
        "d4\trefs/tags/proposal-outcome/2026-11-02/upkeep/accepted-changed",
        "e5\trefs/heads/main",
    ])
    planted = {  # defect -> a ledger carrying it
        "a status that is not a status": [*clean[:1], rec("2026-10-26/new-venue-montalvo", "new-venue", "approved")],
        "waiting with a decided week": [rec("2026-10-26/upkeep", "upkeep", "waiting", "2026-11-02")],
        "decided with no decided week": [rec("2026-10-26/upkeep", "upkeep", "declined")],
        "a duplicate id": [clean[1], clean[1]],
        "a week that disagrees with its id": [rec("2026-10-26/upkeep", "upkeep", week="2026-11-02")],
        "a slug that does not name its kind": [rec("2026-10-26/montalvo", "new-venue")],
        "an unknown kind": [rec("2026-10-26/upkeep", "tidy")],
        "a missing field": [{k: v for k, v in clean[1].items() if k != "summary"}],
        "backticks in a public summary": [rec("2026-10-26/upkeep", "upkeep", summary="Edit `sources.yml`")],
    }
    against_remote = {  # defect -> (ledger, remote)
        "a decided status GitHub contradicts": (
            [rec("2026-10-26/site-change-coast", "site-change", "accepted", "2026-11-02")], remote),
        "a branch gone with no outcome": ([rec("2026-10-19/upkeep", "upkeep")], remote),
        "two outcomes for one proposal": ([rec("2026-10-26/upkeep", "upkeep")],
                                          remote + "\nf6\trefs/tags/proposal-outcome/2026-10-26/upkeep/declined"),
    }
    failed, records = [], 0

    found = check(clean)
    records += len(clean)
    if found:
        failed.append(f"a clean ledger was flagged: {found}")
    status, found = resolve(clean, remote)
    want = {"2026-10-26/upkeep": "accepted", "2026-10-26/new-venue-montalvo": "waiting",
            "2026-10-26/site-change-coast": "declined", "2026-11-02/upkeep": "accepted-changed"}
    if found or status != want:
        failed.append(f"the clean ledger resolved wrongly: {status} {found}")
    newly = resolve([rec("2026-10-26/upkeep", "upkeep")], remote)[0]
    records += 1
    if newly != {"2026-10-26/upkeep": "accepted"}:
        failed.append(f"a waiting record did not pick up its outcome: {newly}")

    for name, ledger in planted.items():
        records += len(ledger)
        if not check(ledger):
            failed.append(f"not caught: {name}")
    for name, (ledger, rem) in against_remote.items():
        records += len(ledger)
        if check(ledger) or not resolve(ledger, rem)[1]:
            failed.append(f"not caught: {name}")

    cases = 3 + len(planted) + len(against_remote)
    if failed:
        print("\n".join(f"FAIL  {f}" for f in failed))
        print(f"self-test FAILED: {len(failed)} of {cases} cases")
        return 2
    print(f"self-test passed: {cases} cases, {records} records checked")
    return 0


def main(argv: list[str]) -> int:
    if argv == ["--self-test"]:
        return self_test()
    try:
        if argv == ["--check"]:
            records = load()
            found = check(records)
            print("\n".join(found) if found else f"ledger ok: {len(records)} records checked")
            return 1 if found else 0
        if argv[:1] == ["--status"]:
            rest = argv[1:]
            write = "--write" in rest
            week = rest[rest.index("--week") + 1] if "--week" in rest[:-1] else None
            if write and not (week and re.fullmatch(DATE, week)):
                print("--write needs --week <window_start>")
                return 2
            return cmd_status(write, week)
        if argv[:1] == ["--add"] and len(argv) == 4:
            return cmd_add(*argv[1:])
    except (OSError, ValueError, subprocess.SubprocessError) as e:
        print(f"could not check: {e}")
        return 2
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
