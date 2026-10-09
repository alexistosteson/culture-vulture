# Handoff — rot-check build: steps 1–2 live, steps 3–7 to do, 9 October 2026

Session name: Draft the build spec for the rot-detection checks

Read `CLAUDE.md` first; it is binding. **`docs/` is the published web root.** The build
record is [`specs/rot-checks-build.md`](../specs/rot-checks-build.md) — tier, the seven
steps, every owner decision (§7) and the evidence for steps 1 and 2 (§10) are there and
are not repeated here.

## Changed since last session

On `main`: step 2, the venue declarations in `config/sources.yml`, with its evidence in
spec §10. Check 4's undeclared count on the working branch fell from 30 to 0; check 3's
warnings fell from 8 to 5.

The working branch `claude/priceless-euclid-56c3ca` (worktree
`.claude/worktrees/zen-varahamihira-9e0602`) has `main` merged in and still carries
`scripts/drift.py` with checks 2–4, **not wired into the gate and not mergeable**: it
exits 1 by design until step 4.

Settled this session and written nowhere else:

- `observed_venues:` entries carry `found_via:` (prose), an optional `url:` and a `note:`
  saying what the route omits. `drift.py` reads only `name` and `venues:` from them.
- **Songkick and Funcheap refuse a fetch that announces itself as a browser** (406, 403)
  and answer a plain one. From this Mac: `curl -A "curl/8.7.1"`. The unattended run's own
  fetch tool reads both, and reads JamBase.
- `curl` needs `--compressed` for techcuarena.com, or the body comes back unreadable.

## Do not re-read

- `handoff/route-research-2026-10-08/` — used up by step 2 for the venues it declared.
  Open `stale-and-fallback-routes.md` only for steps 5–7 (items 1–12), and re-fetch
  before writing anything from it: step 2's re-fetch overturned four of its claims (§10).
- `handoff/session-2026-10-08-build.md` — superseded by this file. Its Lessons section
  (merging from a worktree; `[skip ci]` on the red branch) still applies.
- `specs/fallback-sourcing.md`, `scripts/validate.py`, `scripts/build.py`, `docs/`.

## Read only these

- [`specs/rot-checks-build.md`](../specs/rot-checks-build.md) — §2 for the step being
  built, §7 decision 1 for how the gate shows a warning.
- `scripts/drift.py` on the working branch; `scripts/verify.sh`;
  `prompts/weekly-research.md` (its verification pass).

## Current state

- `bash scripts/verify.sh` on `main` → exit 0, 9 passed, 0 failed, **1 skipped** (the
  page-render check; this Mac has no Chromium where the gate looks).
- On the working branch `python3 scripts/drift.py` → self-test 38/38, exit 1 by design:
  check 2 blocks on DNA Lounge and Regency Ballroom. Check 3 warns on Stern Grove, Music
  on the Square, Filoli, Felton Music Hall, Sweetwater Music Hall. Check 4: 0.

## Next action

In the worktree `.claude/worktrees/zen-varahamihira-9e0602`, do **step 3** of
`specs/rot-checks-build.md` inline: make checks 3 and 4 warning-only in the gate —
`scripts/verify.sh` counts `  WARN  ` lines under a fourth word, WARN, in its summary
line, and they never change the exit code — and tell `prompts/weekly-research.md` to
repeat every warning in the weekly report, in the same merge. Check 2 must stay out of
the gate until step 4, so step 3 has to land without it: either gate check 2 behind a
flag that is off, or split the commit.

## Unresolved questions

- **Owner's, new on 9 October — how a listing shows that it is uncertain.** He ruled that
  sourcing detail cannot sit in the listing text, least of all on a phone. Today 18 of the
  newest week's 351 listings carry a sourcing sentence in their note, and 46 carry a
  confidence mark (33 medium, 13 low) the page never shows. Options put to him: keep it
  out of listings altogether; footnotes; or a short mark on the uncertain listings only,
  with the reason one tap away and one legend at the foot. Recommended the third, as its
  own small spec after this build — spec §9 keeps this build off the page. **Not decided.**
- **Owner's:** removing a tier-1 venue is editorial (step 7: Felton, Sweetwater, Filoli).
  The 8 October research says all three are open and readable past the 100 KB line.
- **Owner's, later:** check 4 counts "3 or more weeks" over the whole history.
- **Owner action, not a decision:** paste the updated `prompts/weekly-run.md` into the
  routine once step 4 lands.

## Constraints

- **Do not merge check 2 before the newest week's digest accounts for its flags.** If
  Monday's run (03:00 UTC, 12 October) publishes first, the newest week becomes
  12 October: run `drift.py` again and treat whatever it flags the same way.
- Steps 3 and 4 must update `prompts/weekly-research.md` in the same merge as the check.
- Still owed at the end: the owner's behavioural check as a click-by-click page (spec
  §8), a `BACKLOG.md` row for the per-source run log, and §10 evidence for each step.
- PayPal Park's `found_via` is "not recorded". Fill it in when a run next lists it.

## Lessons

- **A research report's "could not read" is a claim about one fetcher.** Two venues were
  about to be written down as unreachable because a 403 was not retried without a
  browser user-agent.
- **Step work on a branch that is red by design cannot be verified there.** Step 2 was
  applied as a patch to a fresh branch from `origin/main` in a scratch worktree, verified
  and merged from there, and `main` then merged back into the working branch.
