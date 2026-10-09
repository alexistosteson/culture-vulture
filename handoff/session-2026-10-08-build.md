# Handoff — rot-check build: step 1 live, steps 2–7 in flight, 8 October 2026

Session name: Draft the build spec for the rot-detection checks

Read `CLAUDE.md` first; it is binding. **`docs/` is the published web root.** The build
record is [`specs/rot-checks-build.md`](../specs/rot-checks-build.md) — tier, the seven
steps, every owner decision (§7) and step 1's evidence (§10) are there and are not
repeated here.

## Changed since last session

On `main`:

- `dbf215c` spec: rot checks, the build — probe tier, owner decisions of 8 October
- `7f44210` drift: spelling-split check, wired into the gate as required
- `0cc9a22` Merge: rot-check build spec and step 1, the spelling-split check

On `claude/priceless-euclid-56c3ca` only (pushed, **not merged, not mergeable yet**):

- `d875c21` drift: checks 2, 3 and 4 — work in progress, not wired into the gate

Settled this session and written nowhere else:

- Group D venues (`found_via:`) go in a new top-level `sources.yml` list named
  **`observed_venues:`**. `scripts/drift.py` on the branch already reads that name.
- `drift.py` prints warnings as lines beginning `  WARN  `. `verify.sh` does not count
  them yet; that wiring is step 3.

## Do not re-read

- `specs/fallback-sourcing.md` — unchanged since `ccbf256`. Addendum 3 is restated as
  build steps in the new spec; open it only to settle a disagreement.
- `handoff/session-2026-10-08.md`, `handoff/session-2026-10-07.md` — unchanged since
  `ccbf256`. Their trap lists still apply.
- `scripts/validate.py`, `scripts/build.py`, `docs/` — unchanged since `ccbf256`.

## Read only these

- [`specs/rot-checks-build.md`](../specs/rot-checks-build.md) — §2 for the step being built.
- `scripts/drift.py` **on the branch** (`git show d875c21:scripts/drift.py`) — `main` has
  check 1 only.
- [`handoff/route-research-2026-10-08/`](route-research-2026-10-08/) — three reports on
  which venue addresses a plain fetch can read. See the caution below.

## Current state

- `main` = `0cc9a22`. `bash scripts/verify.sh` → exit 0, 9 passed, 0 failed, **1 skipped**.
  The skip is the page-render check: this Mac has no Chromium where the gate looks. In the
  cloud container it runs.
- On the branch, `python3 scripts/drift.py` → self-test 38/38, then **exit 1 by design**:
  check 2 blocks on DNA Lounge and Regency Ballroom until `digests/2026-10-05.md` has its
  "Thin this week" section. Check 3 prints 8 warnings and check 4 prints 30 (27 rooms plus
  three comma-suffixed strings), which is what Addendum 3 predicts before any declaration.
- `config/sources.yml`, `prompts/weekly-run.md`, `digests/` — untouched. Nothing from
  steps 2–7 is in any file yet.
- The route research was done by three background research passes. **Their reports are
  accounts, not proof.** Re-fetch a URL yourself before writing it into `sources.yml`; the
  spec's rule is that every URL written is one that was fetched and read. Any item a report
  marks "not checked" was not checked. One report says it reached The Knockout's site by
  guessing the domain and confirmed it by search afterwards — treat that one as unverified.

## Next action

In the `bay-week` repo, check out `claude/priceless-euclid-56c3ca` in a worktree and do
**step 2** of `specs/rot-checks-build.md` inline (no subagent plan): write the venue
declarations into `config/sources.yml` from `handoff/route-research-2026-10-08/`,
re-fetching each URL before writing it, then run `python3 scripts/drift.py` and confirm
check 4's undeclared count falls from 30 to 0.

## Unresolved questions

- **Owner's, and the first thing step 2 needs:** the research found that several of the
  venues Addendum 3 sorted as "has its own calendar" or "recurring" have **no address a
  plain fetch can read** — The Knockout's own site, Solano 2 Drive In, de Young and Legion
  of Honor free Saturdays, Mechanics' Institute's film night — and several more are only
  partly readable (Davies, War Memorial Opera House, Swedish American Hall, 4 Star,
  Mountain View CPA, San Jose CPA, Montgomery, Tech CU Arena). Declaring them as tier 1
  would claim a route that does not exist. The options to put to him: declare them with
  `found_via:` naming how they are actually reached, as group D already is (lean — it is
  the honest description and costs nothing); or declare them tier 1 with a note and accept
  a standing check-3 warning when the sweep misses them. Not decided.
- **Owner's:** removing any tier-1 venue is editorial and goes back to him — applies if
  the research shows Felton Music Hall, Sweetwater Music Hall or Filoli should go (step 7).
- **Owner's, later:** check 4 counts "3 or more weeks" over the whole history, as
  Addendum 3 measured it. As the history grows, a room listed three times long ago would
  warn forever. Not decided; raise it when the first such warning appears.
- **Owner action, not a decision:** paste the updated `prompts/weekly-run.md` into the
  routine once step 4 lands. Nothing depends on it.

## Constraints

- **Do not merge check 2 before the newest week's digest accounts for its flags.** The
  owner chose to add "Thin this week" to the 5 October digest by hand, after really
  re-checking DNA Lounge and Regency Ballroom. If Monday's run (03:00 UTC, 12 October)
  publishes first, the newest week becomes 12 October: run `drift.py` again and treat
  whatever it flags the same way.
- Steps 3 and 4 must update `prompts/weekly-research.md` in the same merge as the check
  they add — the routine reads that file from the repo and has no other way to learn what
  a blocking check wants.
- Still owed at the end: the owner's behavioural check as a click-by-click page (spec §8),
  a `BACKLOG.md` row for the per-source run log, and §10 evidence for each step.

## Lessons

- **Merging from a worktree:** `main` is checked out in the main checkout, so
  `git checkout main` fails here. Step 1 was merged with
  `git merge-tree --write-tree origin/main HEAD` → `git commit-tree` (parents
  `origin/main`, branch head) → `git push origin <commit>:refs/heads/main`. That is a real
  `--no-ff` merge commit. Afterwards fast-forward the main checkout, or it sits behind.
- **The self-test must not replay the week under test.** It did at first, and a
  misspelling in the newest week came out as "could not check" instead of a finding.
- A push whose commit message contains `[skip ci]` keeps a deliberately red branch from
  mailing a CI failure.
