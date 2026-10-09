# Handoff — rot-check build: steps 1–6 live, step 7 to do, 9 October 2026 (late)

Session name: Draft the build spec for the rot-detection checks

Read `CLAUDE.md` first; it is binding. **`docs/` is the published web root.** The build
record is [`specs/rot-checks-build.md`](../specs/rot-checks-build.md) — tier, the seven
steps, every owner decision (§7) and the evidence for steps 1–6 (§10) are there and are
not repeated here.

## Changed since last session

**Step 5 is on `main`.** Stern Grove and Music on the Square carry `season_ends`; SFJAZZ
and DNA Lounge are declared `coverage: partial` with what each route omits; DNA has a
two-address `fallback:`; `prompts/weekly-research.md` tells the run what those keys mean
and to write a standing line for each partial venue under "What could not be reached".
`prompts/weekly-run.md` did not change, so no paste is owed.

**Step 6 is on `main`.** New `scripts/dice.py` reads Kilowatt's and The Knockout's
calendars (16 and 18 events for 9–18 October, against 1–2 a week published). Both entries
carry a new `how:` key giving the command; The Knockout's Funcheap page is now its
`fallback:` and the entry says to read both. The gate has an eleventh check, the script's
offline self-test.

Settled this session and written nowhere else:

- **Whether the unattended run's machine can reach DICE is unknown.** Nothing here can
  test it. If it cannot, the run reports both venues unreached; Monday's digest says which.
- This Mac's `python3` (3.14, python.org) has no certificate bundle of its own; `dice.py`
  uses `certifi` when it is installed. A `CERTIFICATE_VERIFY_FAILED` here is the machine.
- DICE lists from today forward only, and can carry one night twice.

- **The spec's season end for Music on the Square was wrong** — 4 September, not
  31 August. §2 and §10 carry the correction.
- **SFJAZZ's `note:` is already rewritten** (step 7 listed it). Step 7 has nothing left to
  do on SFJAZZ.
- `redwoodcity.org` refuses a browser-style request and the fetch tool alike. Funcheap is
  the page that reads for anything on Courthouse Square.
- The Joe Henderson Lab has a JamBase page and a Songkick page that shared no show at all
  on 9 October. They are named in SFJAZZ's note as things to read, not as coverage.
- `drift.py` takes `--data` and `--digests` although `--help` does not show them.

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
  3 warnings**, `rendered 359/359 listings`.
- `python3 scripts/drift.py` → self-test 43/43, exit 0. Check 2: 1 thin (Regency
  Ballroom), accounted for. Check 3 warns on Filoli, Felton Music Hall, Sweetwater Music
  Hall — step 7's. Check 4: 0.

## Next action

**If it is after Monday 12 October 03:00 UTC, look at the unattended run before anything
else.** It is the first run to meet a blocking check it has to answer in writing, and the
first to be asked for standing lines. Expected: it publishes the 12 October week with an
*unreached* line for DNA Lounge under `## Thin this week`, a standing line each for SFJAZZ
and DNA Lounge under `## What could not be reached`, three warnings repeated in its
report, and **either several Kilowatt and Knockout listings or both named as unreached**.
If it did not publish, read why before building further.

Then **step 7**, inline, in the worktree: the stale entries §2 lists (SFJAZZ's note is
already done), and Felton, Sweetwater and Filoli — a route fix, a `season_ends`, or a
removal that goes to the owner with the evidence.

## Unresolved questions

- **Owner's:** removing a tier-1 venue is editorial (step 7: Felton, Sweetwater, Filoli).
- **Owner's, later:** check 4 counts "3 or more weeks" over the whole history.
- Decided, not yet built: uncertain listings get a short mark, the reason one tap away and
  one legend at the foot. Its own small spec after this build; a `BACKLOG.md` row when the
  build closes. Until then, write no sourcing sentences into listing text.

## Constraints

- Step 7 changes `config/sources.yml`, which the Monday run reads. A wrong route costs
  listings every week it stays wrong; fetch, read, then write.
- The DICE key is never written to any file here. The repository is public. `dice.py`
  has no option that prints or accepts one; do not add one.
- Still owed at the end: the owner's behavioural check as a click-by-click page (spec
  §8), a `BACKLOG.md` row for the per-source run log, and §10 evidence for each step.
- PayPal Park's `found_via` is "not recorded". Fill it in when a run next lists it.
- The main checkout has an untracked `specs/next-gen/`. It is not this build's; leave it.
- The 28 August listing's note calls that night Music on the Square's season close; it was
  the second-to-last. Published week, left alone.

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
