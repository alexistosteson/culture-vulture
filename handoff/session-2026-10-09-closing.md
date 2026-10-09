# Handoff — rot-check build: all seven steps live, closing items owed, 9 October 2026 (night)

Session name: Draft the build spec for the rot-detection checks

Read `CLAUDE.md` first; it is binding. **`docs/` is the published web root.** The build
record is [`specs/rot-checks-build.md`](../specs/rot-checks-build.md) — tier, the seven
steps, every owner decision (§7) and the evidence for every step (§10) are there and are
not repeated here.

## Changed since last session

**Steps 5, 6 and 7 are on `main`. The build's seven steps are done.** What remains is the
closing list under "Next action".

Settled this session and written nowhere else:

- **The 8 October route research judged pages by `curl` and a 100 KB cut-off. The fetch
  tool the run uses read every one of them to the end.** Do not trust its "truncated"
  verdicts; re-read with the fetch tool.
- Felton and Sweetwater are `outer` venues, admitted only when a show would be a
  top-three event of the week. Their warnings may persist with working routes. Whether
  check 3 should exempt outer venues is undecided and wants a few weeks of evidence.
- Whether the unattended run's machine can reach DICE is unknown; nothing here can test it.
- This Mac's `python3` (3.14, python.org) has no certificate bundle; `dice.py` uses
  `certifi` when installed. A `CERTIFICATE_VERIFY_FAILED` here is the machine.
- `drift.py` takes `--data` and `--digests` although `--help` does not show them.
- The 28 August listing's note calls that night Music on the Square's season close; it
  was the second-to-last. Published week, left alone.

## Do not re-read

- Every earlier `handoff/session-*.md` — superseded by this file.
- `handoff/route-research-2026-10-08/` — open `stale-and-fallback-routes.md` only for the
  item being worked, and **re-fetch before writing anything from it**: six of its claims
  have now been overturned or corrected.
- `specs/fallback-sourcing.md`, `scripts/validate.py`, `scripts/build.py`, `docs/`.

## Read only these

- [`specs/rot-checks-build.md`](../specs/rot-checks-build.md) — §2 for the step being
  built; §10 "Step 5" and "Step 6" for the shape `coverage`, `fallback` and `how` took.
- `config/sources.yml` — its header, and the entries the step touches.

## Current state

- `bash scripts/verify.sh` on `main` → exit 0, **11 passed, 0 failed, 0 skipped,
  4 warnings**, `rendered 359/359 listings`.
- `python3 scripts/drift.py` → self-test 43/43, exit 0. Check 3 warns on Filoli, Felton
  Music Hall, Sweetwater Music Hall (routes fixed today, not yet listed) and ODC Theater
  (added today, never listed). Check 4: 0.

## Next action

**If it is after Monday 12 October 03:00 UTC, look at the unattended run first.** It is
the first run under all seven steps. Expected in the 12 October week: an *unreached* line
for DNA Lounge under `## Thin this week`; a standing line each for SFJAZZ and DNA Lounge
under `## What could not be reached`; several Kilowatt and Knockout listings, or both
named as unreached; ODC's 16–18 October performances; and the warnings repeated in the
report. If it did not publish, read why before anything else. Record what it did in §10.

Then close the build:

1. The owner's behavioural check as a click-by-click HTML page (spec §8), rendered to
   him in the panel.
2. `BACKLOG.md` rows: the per-source run log; the mark for uncertain listings (decided
   9 October — a short mark, the reason one tap away, one legend at the foot).
3. Bring the owner the outer-venue question above once two or three weeks have run.

## Unresolved questions

- **Owner's, later:** check 4 counts "3 or more weeks" over the whole history.
- Decided, not yet built: uncertain listings get a short mark, the reason one tap away and
  one legend at the foot. Its own small spec after this build; a `BACKLOG.md` row when the
  build closes. Until then, write no sourcing sentences into listing text.

## Constraints

- `config/sources.yml` is read by the Monday run. A wrong route costs listings every
  week it stays wrong; fetch, read, then write.
- The DICE key is never written to any file here. The repository is public. `dice.py`
  has no option that prints or accepts one; do not add one.
- Still owed at the end: the owner's behavioural check as a click-by-click page (spec
  §8), a `BACKLOG.md` row for the per-source run log, and §10 evidence for each step.
- PayPal Park's `found_via` is "not recorded". Fill it in when a run next lists it.
- The main checkout has an untracked `specs/next-gen/`. It is not this build's; leave it.

## Lessons

- **Correcting an old week changes what the self-test expects of it — and the failure
  waits for the next week.** The newest week is not replayed, so adding listings to
  5 October looked clean today and would have failed Monday's run at its first step. It
  was caught by rehearsing: copy `data/` and `digests/` to a scratch directory, add a
  later week, and run `drift.py --data … --digests …`.
- **A plant that changes nothing looks like a pass.** One planted defect matched no text;
  the gate's unchanged count gave it away. Print the match count for every plant.
- **A venue that "returns errors" may be refusing the tool.** Try the other kind of
  request before recording a venue as down — in both directions.
- Merging from a worktree is unchanged: `git merge-tree --write-tree origin/main HEAD` →
  `git commit-tree` with both parents → `git push origin <commit>:refs/heads/main`, then
  fast-forward the main checkout. A `cd` into the scratch directory resets the shell to
  the main checkout afterwards; start each command with a `cd` to the worktree.
