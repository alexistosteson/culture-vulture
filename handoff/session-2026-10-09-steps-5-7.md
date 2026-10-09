# Handoff — rot-check build: steps 1–4 live, steps 5–7 to do, 9 October 2026 (evening)

Session name: Draft the build spec for the rot-detection checks

Read `CLAUDE.md` first; it is binding. **`docs/` is the published web root.** The build
record is [`specs/rot-checks-build.md`](../specs/rot-checks-build.md) — tier, the seven
steps, every owner decision (§7) and the evidence for steps 1–4 (§10) are there and are
not repeated here.

## Changed since last session

On `main` (`bd95232`): **step 3** — checks 3 and 4 report as warnings that `verify.sh`
counts under a fourth word and lists beneath its summary — and **step 4** — check 2 is
live and blocks until the digest's `## Thin this week` names the venue.

The 5 October week was answered by hand, as the owner decided: eight DNA Lounge listings
added (351 → 359, published), a `## Thin this week` section in `digests/2026-10-05.md`,
and the Regency's single show confirmed. All four checks are now in the gate. Nothing is
held behind a switch any more.

The working branch `claude/priceless-euclid-56c3ca` (worktree
`.claude/worktrees/zen-varahamihira-9e0602`) is level with `main` and **green** — step
work can be verified and merged straight from it again.

Settled this session and written nowhere else:

- **DNA Lounge's calendar is not down; it sorts by who is asking.** A request that
  announces itself as a browser gets it (200, 18 KB); plain `curl` gets 403; the
  unattended run's fetch tool gets a page that says only "PRIVATE". The reverse of
  Songkick and Funcheap. From this Mac: `curl --compressed -A "<a Safari user-agent>"`.
- DNA's per-event pages are `/calendar/2026/10-09.html`, with a letter when a night has
  more than one event (`10-09a.html`, `10-09d.html`). A played event's page can 404.
- Its mirrors carry concerts only. JamBase (`jambase.com/venue/dna-lounge`) showed 3 of
  the window's 10 events on 8 October; plain `curl` gets 403 there, the fetch tool reads
  it. The Songkick address in the route research was **not** re-read this session.
- `verify.sh` now finds Chrome where macOS keeps it, so on this Mac the gate is
  **10 passed, 0 skipped** and the page-render check really runs.

## Do not re-read

- `handoff/session-2026-10-09-build.md` and `handoff/session-2026-10-08-build.md` —
  superseded by this file.
- `handoff/route-research-2026-10-08/` — open `stale-and-fallback-routes.md` only for the
  item being worked (items 1–12 map to steps 5–7), and **re-fetch before writing anything
  from it**: step 2 overturned four of its claims and step 4 a fifth (DNA's "200").
- `specs/fallback-sourcing.md`, `scripts/validate.py`, `scripts/build.py`, `docs/`.

## Read only these

- [`specs/rot-checks-build.md`](../specs/rot-checks-build.md) — §2 for the step being
  built; §10 "Step 4" for what is known about DNA Lounge.
- `config/sources.yml` — the entries the step touches.
- `scripts/drift.py` only if a step changes what it reads (`season_ends` is already read
  and already tested; `coverage:` is read by nothing).

## Current state

- `bash scripts/verify.sh` on `main` → exit 0, **10 passed, 0 failed, 0 skipped,
  5 warnings**, `rendered 359/359 listings`.
- `python3 scripts/drift.py` → self-test 43/43, exit 0. Check 2: 1 thin (Regency
  Ballroom), 1 accounted for. Check 3 warns on Stern Grove Festival, Music on the Square,
  Filoli, Felton Music Hall, Sweetwater Music Hall. Check 4: 0.
- CI on the step-3 merge passed. **The step-4 merge's CI run was not read** — check it
  first (`gh run list --branch main --limit 2`).

## Next action

**If it is after Monday 12 October 03:00 UTC, look at the unattended run before anything
else.** It is the first run to meet a blocking check it has to answer in writing. Expected:
it publishes the 12 October week with an *unreached* line for DNA Lounge under
`## Thin this week`, and repeats five warnings in its report. If it did not publish, read
why before building further — a check that stops a week it should not is this project's
standing failure.

Then **step 5**, inline, in the worktree: `season_ends` on Music on the Square
(31 August) and Stern Grove Festival (16 August) — two of the five warnings should go;
`coverage: partial` with a checked date on SFJAZZ and DNA Lounge, DNA's mirror declared
as its fallback route, and the standing line for each in "What could not be reached" via
`prompts/weekly-research.md`. Every URL written is one fetched and read that day.

## Unresolved questions

- **Owner's — how a listing shows that it is uncertain.** Unchanged from 9 October
  morning: he ruled sourcing detail out of listing text; three options were put;
  recommended a short mark with the reason one tap away, as its own small spec after this
  build. **Not decided.** The eight listings added this session carry no sourcing
  sentences; the rewritten Parrotfish note still has one clause of it.
- **Owner's:** removing a tier-1 venue is editorial (step 7: Felton, Sweetwater, Filoli).
- **Owner's, later:** check 4 counts "3 or more weeks" over the whole history.
- **Owner action, now due:** paste the updated `prompts/weekly-run.md` into the routine.
  Nothing breaks without it — the run reads `prompts/weekly-research.md` from the
  repository, and everything it must do differently is there.

## Constraints

- Steps 5–7 change `config/sources.yml`, which the Monday run reads. A wrong route costs
  listings every week it stays wrong; fetch, read, then write.
- Step 6: the DICE key is never written to any file here. The repository is public.
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
