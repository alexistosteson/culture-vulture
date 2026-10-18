Session name: Draft the build spec for the rot-detection checks

# Handoff: proposals build, half done (18 October 2026)

Read `CLAUDE.md` first; it is binding. **`docs/` is the published web root.** The owner
is a non-technical product manager. Bring him product choices in plain words, decide the
mechanics yourself, and end on a recommendation. This file supersedes
`session-2026-10-18-proposals-and-notes-specs.md`; don't re-read that one.

## Decided

- **The owner approved both written specs as they stand** (18 October, in chat:
  "Yes, both specs are approved as written. Go ahead with the proposals build.").
  The specs are `specs/proposals-as-pull-requests.md` (probe) and
  `specs/weekly-public-note.md` (production).
- **The first run that opens proposals is 26 October, not 19 October** (session call,
  following the spec's own dates). Leave the routine's stored prompt as it is until the
  19 October run has fired (03:04 UTC), so that run stays on the old steps. That keeps
  the trial at 26 Oct and 2, 9 and 16 Nov, with the **review on 17 November**.

## Done, on `main` (merge `7c140cb`, pushed)

- `.github/workflows/proposals.yml` handles both ends. A push to `proposal/<week>/<slug>`
  opens a pull request: title from the commit subject, description from the body, labels
  `proposal`, `kind:<kind>` and `week:<week>`. A later push to the same branch adds a
  comment instead. When a pull request closes, the workflow records the outcome as tag
  `proposal-outcome/<week>/<slug>/<accepted|accepted-changed|declined>`, then deletes the
  branch. `accepted-changed` means some commit on the PR lacks the trailer line
  `Proposal-by: weekly-run`. The close side uses `pull_request_target` and never checks
  out branch code.
- `scripts/proposals.py` has five modes. `--check` validates offline. `--status` reads
  outcomes through `git ls-remote`, and `--status --write --week W` writes them to the
  ledger. `--add` adds a record, and `--self-test` runs 15 cases. `verify.sh` check 10 and
  CI run the self-test and `--check`. The ledger is `proposals/ledger.json`, which holds
  `[]` for now.
- `prompts/weekly-run.md` has the new steps. 5a commits the week. 5b handles proposals:
  (i) bring earlier ones up to date, (ii) draft, (iii) record. 7a pushes the proposal
  branches only after `main` has the week. The install line is now
  `python3 -m pip install …`.
- `handoff/proposals-setting-walk.html` is the owner's click-by-click page for the GitHub
  setting. It has been sent to him.
- `verify.sh` exits 0 on `main`.

## In flight: five local proposal branches, NOT pushed

They live in this repository's local branches, which every checkout shares. **Pushing one
is what opens its pull request**, so nothing gets pushed until the owner has ticked the
setting.

| Branch | Commit | What |
|---|---|---|
| `proposal/2026-10-12/new-venue-pipeline-test` | `eb5fa4b` | throwaway test: a comment line in `sources.yml` |
| `proposal/2026-10-12/upkeep` | `78d4d85` | Roxie → `/calendar/`; Litquake tier-2 entry; A.C.T. `coverage: partial`; observed entries for Curran, Ferry Building, Eclectic Box |
| `proposal/2026-10-12/new-venue-montalvo` | `d799b44` | Montalvo, tier 1 South Bay, from the Carriage House season page |
| `proposal/2026-10-12/new-venue-neck-of-the-woods` | `3b826f6` | Neck of the Woods, tier 1 SF, from its own calendar |
| `proposal/2026-10-12/site-change-more-towns` | `c6d3760` | `brief.yml`: Milpitas, Daly City, Pacifica, Richmond, Pleasant Hill, Orinda; `docs/events.json` unchanged |

Every branch passed `verify.sh` and was cut from `origin/main` at `ed01b3f`, before the
build merged. They are four real proposals, where the spec expected three:

- **Item 7 (Half Moon Bay, Stanford) was already done** on 18 October, by the owner's
  decision in commit `c97e241`. The site-change proposal covers the other towns instead,
  counted from the data. Pleasanton is left out and the proposal says why.
- **California Theatre and Frost Amphitheater were already covered** by new tier-1
  entries.
- **Neck of the Woods became its own `new-venue` proposal**, because its own page reads
  in full. Item 1 had suggested it as an observed entry.
- **The re-fetch overturned two 12 October claims.** Litquake's Sched no longer refuses,
  and the Roxie's calendar page reads in one go. Both proposals say so.

All addresses were re-fetched on 18 October, and each proposal lists them with results.

## Next action, in order

*Checked 18 Oct 22:28 UTC: the setting still read `false`; walk page re-sent, the
item-6 questions asked. Resume at step 1.*

1. **Check the setting:** `gh api repos/alexistosteson/culture-vulture/actions/permissions/workflow`.
   It must read `"can_approve_pull_request_reviews":true`. If it doesn't, the owner
   hasn't ticked it yet: re-send `handoff/proposals-setting-walk.html` and stop there.
2. **Test (Done when 2):** rebase the test branch onto `origin/main` and push it. Confirm
   the pull request's title, body and labels, and that CI checks appear on it. Close it
   with `gh pr close`, never merge. Confirm the tag
   `proposal-outcome/2026-10-12/new-venue-pipeline-test/declined` exists and the branch is
   gone. Then delete that test tag. If any of this fails, fix the workflow on a branch and
   merge before going on.
3. **Ledger first, then push.** On a branch, `--add` the four records: ids
   `2026-10-12/upkeep`, `2026-10-12/new-venue-montalvo`,
   `2026-10-12/new-venue-neck-of-the-woods` and `2026-10-12/site-change-more-towns`, each
   with its commit subject minus the `Proposal (<kind>): ` prefix as the summary. Run
   `verify.sh`, merge to `main` and push. Then rebase each of the four onto `origin/main`
   and push them (Done when 3). Confirm the checks go green.
4. **Done when 1 demonstration:** plant one wrong status in the ledger, say
   `"status": "approved"`. Show `verify.sh` failing on it and printing the record count,
   then revert. Record it in the spec's `## Evidence`.
5. **Owner's check (Done when 5):** write a click-by-click HTML page. He opens one of the
   pull requests, says whether he could decide from the description alone, then accepts
   or turns it down. Send it with `SendUserFile` (render).
6. **Questions for the owner** (handoff item 2, still owed):
   - Starline Social Club: `sources.yml` records it closed since 11 June, but a sweep
     showed an 18 Oct show there. Did it reopen?
   - The SF Opera costume sale: the run included it even though "sale" matches the
     filter. Keep that call or reverse it?
7. **After 19 Oct 03:04 UTC:** update the routine `trig_01U3f8NYCvzd7WEbYSNEbvNK` with
   `RemoteTrigger` `update`. Set both prompt copies, `job_config.ccr.events[0].data.message.content`
   and `session_request.events[0].payload.message.content`, to the fenced prompt in
   `prompts/weekly-run.md`. Read it back and compare (Done when 4). If the update is
   refused, give the owner a paste page. **Done when 3a** (the routine itself pushes and
   force-pushes a test branch) is still open. Don't fire the full routine for it. Find a
   way to run a one-off routine with the same environment, or ask the owner.
8. ~~Put the 17 November trial review on Agent's Cal~~ Done 18 Oct (entry
   `B8C52A3F`); the owner was told. Run `agent-cal.py ack` when he acknowledges.
9. **Note spec** (handoff item 3 from before): run `tier-check.py --tier production` over
   its Files list, then `/nasa-code`, and fill `## Pre-plan audit`. Then write the plan in
   `specs/plans/`. Plan approval is a session boundary.

## Constraints

- No agent ever merges a proposal. Nothing may add a step that can stop a week publishing.
- The main checkout has an untracked `specs/next-gen/`. It isn't this work's; leave it.
- The build worktree is `.claude/worktrees/proposals-build` on `build/proposals`, which
  tracks `origin/main`. It can be removed once the branches are pushed.
