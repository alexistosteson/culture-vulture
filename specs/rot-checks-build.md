# Spec — Rot checks: the build

**Status: 8 October 2026.** Tier and all three open decisions taken by the owner (§7).
Nothing here is built yet.

## Tier

**probe** — declared by the owner, 8 October 2026.

One condition travels with it, because a detector's failure mode is silence — a check that
has gone blind prints nothing, and nothing looks like a healthy week: **the gate replays
cases whose answers are already known and fails if the checks stop finding them** (§4).
No plan, no code-safety audit, no tier registry owed.

## 1. What this is

[`fallback-sourcing.md` → Addendum 3](fallback-sourcing.md#addendum-3-8-october--decisions-and-the-measurements-behind-them)
is the decision record. This spec turns it into changes and adds no decisions of its own
beyond §7. Where this file and Addendum 3 disagree, Addendum 3 wins and this file is wrong.

In one paragraph: the weekly digest loses listings quietly — a venue's name gets spelled a
new way and splits in two, a venue's count collapses and nobody says why, a venue the
project claims to watch stops producing, or a venue the project has come to rely on was
never written down. Four checks make each of those visible. Two can stop a week publishing;
two only report.

| Check | Catches | When it fires | Effect |
|---|---|---|---|
| 1 · Spelling split | The same room under two names | A spelling new in the newest week collides with an earlier week's | **Blocks** |
| 2 · Thin venue | A venue far below its own recent normal | Newest week < 40% of the median of the prior four, median ≥ 3 | **Blocks until** the digest's "Thin this week" names it |
| 3 · Declared, not producing | A watched venue gone quiet | Tier-1 venue, zero listings in the last four weeks | Warning |
| 4 · Observed, not declared | A relied-on venue never written down | ≥ 3 weeks, indoor, no entry covers it | Warning |

Venues past their `season_ends` are exempt from checks 2 and 3.

## 2. What changes, in build order

Each step lands on its own and is verified on its own. A step merges when
`scripts/verify.sh` exits 0, per `CLAUDE.md`.

**Step 1 — the script and check 1.** New `scripts/drift.py`, with `canon()` copied verbatim
from Addendum 3 — not reconstructed. Reads `data/*.json`, `config/sources.yml` and the
newest digest; no network. Wired into `verify.sh` as a REQUIRED check and into CI.

**Step 2 — declare the venues.** A `venues:` list on any `sources.yml` entry whose name is
not the venue string. The 29 venues from Addendum 3's table are declared as sorted there:
A as tier-1 entries, B as an entry for the presenter with the building in `venues:`, C as
`recurring:` entries with `venues:`, D with `found_via:`. SFJAZZ, The Greek Theatre and
Music on the Square get their `venues:`. The New Parkway is removed. Comma-suffixed venue
strings are handled as aliases in `venues:`, never by cutting at the comma. **Every new URL
is one that was fetched and read during the build** — a guessed mirror address once
returned a hotel in Northern Ireland, formatted like a correct answer.

**Step 3 — checks 3 and 4, warning-only.** They print; they never change the exit code.
`verify.sh` shows them under a fourth word, WARN (§7 decision 1).

**Step 4 — check 2 and "Thin this week".** The digest gains a section, **Thin this week**,
placed before "What could not be reached". One line per flagged venue: the venue, the word
*reached* or *unreached*, and what was checked. Check 2 reads
`digests/<window_start>.md` and is satisfied only when every flagged venue has such a
line. The convention goes into `prompts/weekly-research.md`'s verification pass, which
tells the run to execute `drift.py` *before* the gate and respond to it — fix a new
spelling to the established one, write the Thin lines — so that the gate is a confirmation
rather than the first time the run hears about it. `prompts/weekly-run.md` is updated to
match.

**Step 5 — seasons and partial coverage.** `season_ends` on tier-1 entries that have one
(Music on the Square: 31 August; Stern Grove: 16 August). `coverage: partial` with a
checked date on SFJAZZ (its mirror omits the Joe Henderson Lab) and DNA Lounge (via a
mirror declared as a fallback, which omits the club nights), and the standing line for
each in "What could not be reached", saying what is omitted and not guessing how much.

**Step 6 — DICE fallback** for Kilowatt and The Knockout. `sources.yml` describes the
route. **The key is read from the venue's own page on each run and is never written to
any file in this repository**, which is public.

**Step 7 — known-wrong entries and three quiet venues** (added by §7 decision 2). Fix the
`sources.yml` entries the 7 October handoff lists as stale: SFJAZZ's `note:` (written for
the August off-season); ODC, Smuin and A.C.T. absent though reachable; Fort Mason pointing
at a failing path, and missing the Cowell Theater; Chronicle Datebook's dead redirect; and
Thee Stork Club, Z Space and 924 Gilman each pointing at the path their own note calls
broken. Look at Felton Music Hall, Sweetwater Music Hall and Filoli and give each a route
fix, a `season_ends`, or removal — whichever the evidence supports, with the evidence
recorded in §10. Removal of a tier-1 venue is an editorial call and comes back to the
owner. Same rule as step 2: every URL written is one that was fetched and read.

## 3. What the unattended run sees

The Monday routine's prompt was created through the API and cannot be edited from here; a
change to `prompts/weekly-run.md` reaches it only when the owner pastes it in. This build
is arranged so that **nothing depends on that paste**: the routine already reads
`prompts/weekly-research.md` from the repository on every run and follows it in full, and
everything the run needs to do differently is written there. The paste is still owed, for
consistency, and is listed in §6.

The risk this guards against is the project's standing one — a stale site. A blocking
check the run was never told how to satisfy would stop every week it fired.

## 4. Proof the checks owe

Probe tier's three rungs, applied:

- **Every count prints what it was counted over.** Each check reports weeks read, venues
  examined, entries matched — so `0 flags` over nothing cannot pass for `0 flags` over 484
  venues. The match between `sources.yml` entries and venue strings reports its rate; a
  tier-1 list that matches no observed venue at all is "could not check", not "clean".
- **The checks are proven able to fail.** `drift.py` carries a self-test that the gate
  runs first. It replays known cases and fails if any is missed:
  - Check 1: the three recorded splits — *Regency Ballroom / The Regency Ballroom*,
    *4 Star / 4-Star Theater*, *Montgomery Theatre / Theater* — each flagged in the week
    its second spelling arrived; and *Fox Theater* in Oakland and Redwood City **not**
    flagged.
  - Check 2: the seven flags in Addendum 3's backtest table, exactly, across the five
    weeks 7 September – 5 October.
  - Checks 3 and 4: one planted case each, plus the pre-declaration answers below.
  - A flagged venue with no "Thin this week" line blocks; the same venue with a line
    passes; a line missing *reached/unreached* does not count.
- **"Could not check" is its own outcome and it blocks.** Three exits: 0 checked and
  clean (warnings may have printed), 1 a blocking check fired, 2 could not check — no data
  files, unreadable data, a failed self-test, a config that will not parse or has lost a
  section the checks read, no digest for the newest week. `verify.sh` treats 2 as a
  failure and says which it was.
- **Too little history is neither of those.** A check that needs more weeks than exist —
  the first weeks of a fork — is reported as *not evaluated* under WARN, with the number of
  weeks it had and the number it needs. Never as a pass. Check 1 with no earlier week at
  all is the one exception: there is nothing to collide with, so it reports zero over
  zero, with the zero printed.

All four were re-measured on 8 October with Addendum 3's `canon()` over the nine files
`data/2026-08-13.json` … `2026-10-05.json`. Checks 1 and 2 reproduce exactly. Check 3
reproduces. **Check 4 gives 27, not 29** — see §5.

## 5. One correction to Addendum 3

Addendum 3 counts **29** undeclared venues for check 4. By its own written definition
(majority `venue_type` not `street` or `park`) the count is **27**: *Noe Valley Town
Square* (street 2, park 1, civic 1) and *Colma Community Center* (park 2, civic 1) are
outdoor by that rule and would never have raised the warning.

Nothing about what gets declared changes — both are still declared in group C as the owner
accepted, and declaring a venue the check would not have flagged costs nothing. The only
effect is on the self-test, which expects 27 before step 2's declarations and 0 after.

## 6. Owed by the owner

- The behavioural check in §8.
- Pasting the updated `prompts/weekly-run.md` into the routine, once step 4 lands. Not
  urgent and nothing breaks without it (§3).

## 7. Decisions taken while drafting

1. ~~How the gate shows a warning.~~ **Decided 8 October: a fourth word, WARN.** The
   summary line counts warnings separately (`passed … failed … skipped … warnings …`),
   each warning names its venue, and the weekly report must repeat every one — the rule
   SKIP already follows. Warnings never change the exit code.
2. ~~Whether Addendum 3's three "still open" items are in this spec.~~ **Decided
   8 October:** the stale `sources.yml` entries and the three quiet venues are in (step 7);
   the per-source run log is out and gets a `BACKLOG.md` row when this spec merges.
3. ~~What happens to the already-published 5 October week when check 2 goes live.~~
   **Decided 8 October: add the section by hand.** DNA Lounge and Regency Ballroom are
   re-checked and `digests/2026-10-05.md` gains a dated "Thin this week" section before
   check 2 is enforced. Any show the re-check finds is added to the week as a dated
   backfill, as on 7 October. This is part of step 4, and it leaves Monday's unattended
   run a worked example.

## 8. Behavioural check (owner)

Delivered with the build as a click-by-click page, not as terminal instructions. In
outline, the owner sees four things happen:

1. A week with a deliberately misspelled venue is refused, and the message names both
   spellings.
2. A week with a thin venue is refused; adding the "Thin this week" line lets it through.
3. The two warnings appear in the gate's output without stopping it.
4. The live week passes.

## 9. Not in this spec

- No change to `docs/`, the page, `brief.yml`, or the events schema.
- The per-source run log (`runs/<window_start>.json`). Undesigned; a backlog row.
- PayPal Park / "minor-league and local only" — noted in Addendum 3, not changed.
- A mechanical check that partial routes are named in "What could not be reached". It is
  a writing convention in step 5; making it a fifth check was not decided.

## 10. Evidence

*Filled in as each step lands: the command, its output, the commit.*

### Step 1 — `scripts/drift.py` and check 1 · 8 October 2026

The check live, inside the gate (`bash scripts/verify.sh`, exit 0):

```
  PASS  drift.py — rot checks ran, nothing blocking
        self-test: 12/12 known cases reproduced
        weeks read: 9 (2026-08-13 … 2026-10-05), 1803 listings; newest 2026-10-05: 351 listings
        check 1 · spelling: 160 venues in 2026-10-05 compared with 418 venues from 8 earlier week(s), 94 in common — 0 new spelling(s)
        drift: checked, nothing blocking
passed 9   failed 0   skipped 1
```

The skip is the page-render check: this machine has no Chromium where the gate looks.
Step 1 changes neither the page nor `docs/events.json`.

Proven able to fail, through the gate and not only at the script. Each defect was planted
in the real files, the plant confirmed (5 and 2 listings changed), the gate run, the files
restored, and the gate run again to exit 0:

| Planted | Gate said | Exit |
|---|---|---|
| "The Fillmore" → "Fillmore" in the newest week | `FAIL drift.py — a rot check is blocking this week` · `BLOCK “Fillmore” (San Francisco, 5 listing(s)) is a new spelling of “The Fillmore”` | 1 |
| The 17 August "Regency Ballroom" rewritten, so a recorded split no longer exists | `FAIL drift.py COULD NOT CHECK — a failure, not a skip` · `self-test failed — recorded history, week of 2026-08-31` | 1 (script: 2) |

At the script alone: an empty data directory, an unparseable data file, a deleted
known week and an `--as-of` for a week that does not exist each exit 2 with the reason.

The recorded history replays as Addendum 3 measured it: `--as-of 2026-08-31` flags *The
Regency Ballroom*; `--as-of 2026-09-14` flags *4-Star Theater* and *Montgomery Theater*;
every other week replays to nothing; the two Fox theatres are never flagged.

One defect found by this exercise and fixed before merge: the self-test first replayed the
newest week too, so a split in the week being checked came out as a broken self-test (exit
2) instead of a finding (exit 1). The newest week now joins the replay only once a later
week exists.

`prompts/weekly-research.md` gained the check in its verification pass in the same step,
so the unattended run is told how to respond before it meets a check that can stop it.
