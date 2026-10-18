Session name: Act-now alerts reader

# Handoff — act-now alerts: the reader (2026-10-18)

Folder: `bay-week` main checkout. Work branch `act-now-reader` (worktree
`.claude/worktrees/act-now-reader`); everything below except the evidence is
already merged to `main` and pushed. **Never write the mailbox address into any
file — the repository is public.** Alerts go to the subscription Gmail's own
plain address (owner, 18 Oct: "use the gmail address for all such comms").

## Done

- **Send guard** `scripts/send_guard.py`, wired for every connector tool in
  `.claude/settings.json`: only a new message to the one address, no cc/bcc,
  attachments, drafts, threading; reply/forward refused. The agent addresses
  alerts to the placeholder `owner`; the guard fills in the real address from
  the private `act-now` cloud environment (variable `ACT_NOW_OWNER_ADDRESS`, or
  the file `~/.act-now-owner` written by that environment's setup script — the
  owner created the environment 18 Oct; which of the two boxes he used is not
  known). Fails closed when neither is present. Self-test (34 cases) runs in
  `scripts/verify.sh` and CI.
- **Daily procedure** `prompts/act-now-daily.md`; design (two stages, memory =
  sent folder, monthly check-in) in `specs/act-now-alerts.md` → "The reader".
- **Test routine** "Act-now alerts: send-restriction test (one-time)",
  `trig_01QkxnchWn2vdQvaa8JsssnW`, environment `act-now`
  (`env_01CDzrBueZBN7kYWAdpbVXNF`), Gmail connector limited to search/get/send,
  no shell/file/web tools. Run started 16:03 UTC, session
  `cse_014JibqYTDWtWzhSLWkcGaGp`. **Its `run_once_at` is 18:00 UTC 18 Oct —
  disable it after reading the run, or it fires a second time.**
- Stern Grove and Hammer confirmation emails: not arrived as of 16:00 UTC.

## Next

1. Read the test run (`RemoteTrigger list_runs` / `get_run_log`): A1–A4 must
   each be refused by send_guard; shell and web must be unavailable; one
   "act-now: TEST" email must have arrived in the mailbox (check with the Gmail
   connector, `in:sent subject:act-now`). If any send was NOT refused, stop and
   tell the owner. Disable the test routine.
2. Create the daily routine: same config as the test routine, cron
   `0 14 * * *` (7am PDT / 6am PST), prompt: "You are the act-now alerts daily
   run for alexistosteson/culture-vulture. Read prompts/act-now-daily.md and
   follow it in full. You are unattended."
3. Record the evidence in `specs/act-now-alerts.md` (Behavioural check +
   Evidence: run id, the refusal texts, the test alert's subject), update the
   BACKLOG.md act-now row, `bash scripts/verify.sh`, merge, push.
4. Raise with the owner (not decided): a Gmail rule starring mail whose subject
   contains "act-now" so alerts stand out; whether the monthly check-in email
   is wanted. Check Stern Grove / Hammer confirmations; open a link only from
   that venue's sender, after showing the owner.
