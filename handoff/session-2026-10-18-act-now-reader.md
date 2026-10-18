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

## Outcome (16:10 UTC)

Test run passed: all four sends refused, no shell or web, the test alert
arrived in the mailbox. Test routine disabled. Daily routine "Act-now alerts
(daily)" `trig_01DgzZwGVY6fSTYDfxPDBqkh` created, 14:00 UTC daily, first run
19 Oct. Evidence recorded in the spec. Finding: the routine setting meant to
narrow the Gmail connector to read+send did not take effect (forward and draft
tools were visible); the guard covers them.

## Next

1. After 19 Oct 14:00 UTC, read the first daily run (`RemoteTrigger list_runs`
   on the daily routine, then `get_run_log`): it should send nothing unless a
   venue announced a dated on-sale moment, and report no guard refusals.
2. With the owner: a Gmail rule starring mail whose subject contains
   "act-now". (Monthly check-in: owner kept it, 18 Oct.)
3. Stern Grove and Hammer confirmation emails — not arrived as of 16:00 UTC.
   Open a link only from that venue's own sender, after showing the owner.
