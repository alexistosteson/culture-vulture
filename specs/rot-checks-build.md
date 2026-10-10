# Spec — Rot checks: the build

**Status: 10 October 2026 — built, and checked by the owner.** All seven steps are live
on `main`; the evidence for each is in §10, and the owner's behavioural check (§8) passed
on all four items. One thing is still owed and is a `BACKLOG.md` row: a record of what the
first unattended run did (Monday 12 October).

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

**Step 2 — declare the venues** (amended by §7 decision 4). A `venues:` list on any `sources.yml` entry whose name is
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
(Music on the Square: ~~31 August~~ **4 September** — corrected when the step was built,
see §10; Stern Grove: 16 August). `coverage: partial` with a
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

- The behavioural check in §8 — delivered 9 October as
  [`handoff/rot-checks-walk.html`](../handoff/rot-checks-walk.html); walked by him, all
  four items passed (§10, "Closing").
- ~~Pasting the updated `prompts/weekly-run.md` into the routine.~~ Done 9 October and
  read back: the routine's stored prompt matches the file.

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

4. **Decided 9 October: venues with no readable address are declared by how they are
   actually reached.** The route research (`handoff/route-research-2026-10-08/`) found
   that several venues Addendum 3 sorted into group A or C have no address a plain fetch
   can read — The Knockout's own site, Solano 2 Drive In, the de Young and Legion of Honor
   free Saturdays, Mechanics' Institute's film night — and about eight more are only
   partly readable. These get `found_via:` naming the route that really reaches them, as
   group D does, and are not listed as tier 1. This overrides Addendum 3's sorting for
   those venues only. **Reading applied to the partly readable ones:** they are treated
   the same way, with `found_via:` saying what the route omits, because the owner limited
   `coverage: partial` to SFJAZZ and DNA Lounge. If he meant only the unreadable ones, the
   partly readable ones go back to tier 1 with a note.

## 8. Behavioural check (owner)

Delivered with the build as a click-by-click page, not as terminal instructions. In
outline, the owner sees four things happen:

1. A week with a deliberately misspelled venue is refused, and the message names both
   spellings.
2. A week with a thin venue is refused; adding the "Thin this week" line lets it through.
3. The two warnings appear in the gate's output without stopping it.
4. The live week passes.

Delivered 9 October: [`handoff/rot-checks-walk.html`](../handoff/rot-checks-walk.html),
one command per item, each run by `handoff/rot-checks-walk.sh`. Evidence in §10, "Closing".

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

### Step 2 — the venue declarations · 9 October 2026

`python3 scripts/drift.py` on the working branch, before and after `config/sources.yml`
was edited (checks 2–4 are not on `main` yet, so this is where the count can be read):

```
before  check 4 · observed, not declared: 88 of 484 venues appear in 3+ weeks, 70 of them rooms, 40 declared — 30 undeclared
after   check 4 · observed, not declared: 88 of 484 venues appear in 3+ weeks, 70 of them rooms, 70 declared — 0 undeclared

before  check 3 · declared, not producing: 53 tier-1 entries, 49 ever matched a listing, 0 out of season — 8 with nothing in the last 4 weeks
after   check 3 · declared, not producing: 60 tier-1 entries, 60 ever matched a listing, 0 out of season — 5 with nothing in the last 4 weeks
```

Self-test 38/38 both times. The five still quiet are the ones steps 5 and 7 own: Stern
Grove and Music on the Square (season over, no `season_ends` yet), Felton, Sweetwater,
Filoli. The 30 were the 27 rooms plus three comma-suffixed spellings, as §5 predicts.

What was written, sorted as §7 decision 4 directs:

| Declared as | Venues |
|---|---|
| Tier 1 (8) | The Midway, Madrone Art Bar, Bill Graham Civic Auditorium, The Masonic, San Francisco Neo-Futurists (`venues:` 447 Minna Street), Rooster T. Feathers, San Jose Improv, PURE Nightclub |
| `recurring:` (2 new, 2 amended) | NightLife (California Academy of Sciences), Noe Valley Town Square; Colma Summer Concert Series and Golden Gate Park Band gain `venues:` |
| `observed_venues:` with `found_via:` (18) | Unreadable: The Knockout, Solano 2 Drive In, de Young Museum, Legion of Honor, Mechanics' Institute. Partly readable: Swedish American Hall, 4 Star Theater, Tech CU Arena, Davies Symphony Hall, War Memorial Opera House, San Jose CPA, Mountain View CPA, Montgomery Theater. Group D: Oakland Arena, Levi's Stadium, Toyota Pavilion at Concord, Alameda County Fairgrounds, PayPal Park |
| `venues:` on existing tier 1 | SFJAZZ, The Greek Theatre, Music on the Square, Gray Area |
| Removed | The New Parkway |

**Every URL written was fetched on 9 October and the venue name and a dated listing read
in the response** — 21 URLs, each inside the first 100 KB of the page. Songkick, Funcheap
and JamBase were also read through the fetch tool the unattended run uses, not only from
this machine.

Re-fetching changed four things the 8 October research reported:

- **Funcheap's venue pages do read.** The research got 403 and did not retry. They refuse a
  request that announces itself as a browser and answer a plain one. So The Knockout and
  Solano 2 Drive In each have a written, fetched route rather than none.
- **Downtown SF's page for Movies at Mechanics' reads** (dates and times for 9 and 16
  October). The research called it an unfilled template.
- **JamBase reads through the run's own fetch tool** (SFJAZZ's Miner Auditorium page:
  five dated shows). The research could not say which way that would go.
- **sfsymphony.org's front page answered**, but its calendar still redirects to the waiting
  room. Davies Symphony Hall stays partly readable.

Two entries say plainly what is not known: PayPal Park's `found_via` is "not recorded" —
none of its three listings carries a source link and it was not on Songkick's sweep that
day — and the de Young and Legion free Saturdays are confirmed only on Funcheap's page for
the day, past the 100 KB line.

Venue capacities for the eight new tier-1 entries are `null`: none was read on a fetched
page, and none was guessed.

### Step 3 — checks 3 and 4 as warnings · 9 October 2026

The gate's last lines on the live week (`bash scripts/verify.sh`, exit 0):

```
passed 9   failed 0   skipped 1   warnings 6
note: 6 warning(s) — repeat each one in the report; a warning does not block.
  WARN  check 2 (thin venue) is switched off and did not look at this week
  WARN  Stern Grove Festival is declared tier 1 and has produced no listing in 4 weeks
  WARN  Filoli is declared tier 1 and has produced no listing in 4 weeks
  WARN  Music on the Square is declared tier 1 and has produced no listing in 4 weeks
  WARN  Felton Music Hall is declared tier 1 and has produced no listing in 4 weeks
  WARN  Sweetwater Music Hall is declared tier 1 and has produced no listing in 4 weeks
note: 1 check(s) skipped — say so in the report; a skip is not a pass.
VERIFICATION PASSED — safe to merge.
```

Self-test 38/38. The five venue warnings are the ones steps 5 and 7 own.

**Check 2 is in the script and switched off** (`THIN_ENFORCED = False`), because the
digest convention it reads does not exist until step 4. It is not silent about that: it
prints `NOT RUN` and a warning on every run, so the gate's count shows it. Its self-test
cases still replay. Step 4 flips the switch and that warning goes.

Planted through the gate, in the real files, each plant confirmed, the files restored and
the gate run again to the output above:

| Planted | Gate said | Exit |
|---|---|---|
| Oakland Arena's entry renamed in `sources.yml`, so no entry covers it | `WARN  Oakland Arena (Oakland) has been listed in 4 weeks and is not in sources.yml` · `warnings 7` | 0 |
| "The Fillmore" → "Fillmore" in the newest week (5 listings) | `failed 2` — the split, and `docs/events.json` gone stale from the plant — with all six warnings still counted and listed | 1 |

The first shows a warning arriving without stopping the week; the second shows a blocked
week still being told its warnings. A first attempt at the Oakland Arena plant changed
nothing — the search string did not match the entry — and the gate's unchanged count of 6
is what gave it away; the plant was redone and confirmed (`entries renamed: 1`).

The no-warnings case was checked on the counting lines alone (`warnings 0`, no note). It
cannot be reached through the gate until steps 4, 5 and 7 clear the six above.

`prompts/weekly-research.md` tells the run what a `WARN` line is, not to edit
`sources.yml` to silence one, and to repeat every one in its report word for word.
`prompts/weekly-run.md` and `CLAUDE.md` say the same. The routine reads
`weekly-research.md` from the repository on each run, so Monday's run is told without the
owner pasting anything (§3).

### Step 4 — check 2 and "Thin this week" · 9 October 2026

The gate on the live week (`bash scripts/verify.sh`, exit 0), with the page-render check
running for the first time on this machine:

```
        check 2 · thin venue: 18 of 404 venues usually have 3+ listings (0 more out of season) — 1 thin, 1 accounted for in the digest
          ok     Regency Ballroom: 1 listing(s) after 2, 2, 4, 5 — accounted for
        rendered 359/359 listings
passed 10   failed 0   skipped 0   warnings 5
```

Self-test 43/43, and 45/45 once a later week exists and 5 October joins the replay.

**The two flagged venues, re-checked on 9 October (§7 decision 3):**

- **DNA Lounge — the flag was right and the week was wrong.** Its own calendar,
  `dnalounge.com/calendar/2026/10.html`, lists ten events between 5 and 11 October; one was
  published. Eight were added to `data/2026-10-05.json` and the digest, each written from
  the club's own page for that event (nine pages fetched and read). The tenth, a Tuesday
  session on running a Discord server, was left out as not arts programming. The week went
  from 351 listings to 359 and the digest's day counts were corrected to match.
- **The Regency Ballroom — the flag was a quiet week.** Its JamBase page, read through the
  fetch tool the unattended run uses, shows Dead Kennedys on the 9th and nothing until the
  13th. The page drops a show once it has played, so 5–8 October cannot be confirmed from
  it, and the digest's line says so.

**Why DNA Lounge has read as down for three weeks.** The calendar is not down. It answers a
request that announces itself as a browser (200, 18 KB) and refuses a plain one (403); the
run's own fetch tool gets a page that says only "PRIVATE". This is the reverse of Songkick
and Funcheap. So the unattended run cannot read it, and on Monday DNA Lounge will be flagged
again; the run is expected to write an *unreached* line and publish. Step 5 is where the
mirror gets declared. Not fixed here.

**The recorded answer for 5 October was changed, deliberately.** The self-test held that
week as flagging DNA Lounge and the Regency. With eight listings added, DNA Lounge is no
longer thin in it, so the record now holds the Regency alone, with a comment saying why.
Left as it was, Monday's run would have failed its self-test the moment a newer week
existed and published nothing. That was rehearsed rather than assumed — the checks were run
against a copy of the data with a 12 October week added:

| Rehearsed for 12 October | Result | Exit |
|---|---|---|
| No digest written yet | `COULD NOT CHECK: no readable digest for the week of 2026-10-12` | 2 |
| Digest with no "Thin this week" section | `BLOCK  Regency Ballroom … has no “Thin this week” section` | 1 |
| A line naming the venue, without *reached* or *unreached* | `BLOCK … does not account for it` | 1 |
| A full line | `ok     Regency Ballroom … accounted for` | 0 |
| DNA Lounge back to one listing, the Regency answered | `BLOCK  DNA Lounge: 1 listing(s) after 4, 9, 2, 9` | 1 |

Planted through the gate, in the real digest, each plant confirmed (`plant matched: 1`),
restored, and the gate run again to exit 0:

| Planted | Gate said | Exit |
|---|---|---|
| The Regency's line deleted | `FAIL drift.py — a rot check is blocking this week` · `BLOCK  Regency Ballroom … does not account for it` | 1 |
| The word *reached* taken out of its line | the same | 1 |
| The heading written as "Thin venues" | `BLOCK … has no “Thin this week” section` | 1 |
| The digest moved away | `FAIL drift.py COULD NOT CHECK` · `no readable digest` | 1 (script: 2) |

`prompts/weekly-research.md` now defines the section, gives two example lines, says what
*reached* and *unreached* mean, and tells the run to look at a flagged venue again before
writing its line. `prompts/weekly-run.md` runs `drift.py` before the gate. `CLAUDE.md`
describes the check. The switch that held check 2 off in step 3 is gone, and its warning
with it.

One thing outside the step: `verify.sh` now finds Chrome where macOS keeps it, so the
page-render check runs locally instead of being skipped. It mattered here because this
step changes what the page shows.

### Step 5 — seasons and partial coverage · 9 October 2026

Every address below was fetched and read on 9 October. What each said:

| Read | Result |
|---|---|
| `sterngrove.org/lineup2026` | 2026 season 14 June – **16 August**, closing with Al Green |
| `redwoodcity.org` (three paths) | 403 to a browser-style request and to the fetch tool alike |
| `sf.funcheap.com/20th-annual-music-on-the-square-…-redwood-city-10/` | "May 29 through September 4"; fifteen dated Fridays, no show 3 July, last **4 September, Pride & Joy** |
| `jambase.com/venue/miner-auditorium-sfjazz-center` | 30 dated shows, Miner Auditorium only; no Joe Henderson Lab listing |
| `jambase.com/venue/joe-henderson-lab-at-sfjazz-center` | Holly Bowling, 13–15 November, and nothing else |
| `songkick.com/venues/2588888-joe-henderson-lab-sfjazz-center` | Ben Wolfe 6 Nov; Hendelman and Sutton 7–8 Nov — no show in common with JamBase's Lab page |
| `sfjazz.org/` and `/calendar/` | 403 to a browser-style request, plain `curl` and the fetch tool |
| `dnalounge.com/calendar/2026/10.html` | browser-style request 200; plain `curl` 403; the fetch tool, a page reading only "PRIVATE" |
| `app.songkick.com/venues/7516-dna-lounge` | 3 concerts (11, 13, 16 October) |
| `jambase.com/venue/dna-lounge` | 2 concerts (11, 13 October) |

**One correction to §2.** The spec gave Music on the Square's season end as 31 August. It
was 4 September: the lineup above says so, `data/2026-08-31.json` lists the 4 September
concert, and the 7 September digest recorded the season as finishing that day. The entry
carries 4 September. (The 28 August listing's note called that night the season's close;
it was the second-to-last. That week is published and was left alone.)

What changed in `config/sources.yml`:

- `season_ends` on Stern Grove Festival (16 August) and on both Music on the Square
  entries (4 September), the latter with a note naming the page that actually reads.
- SFJAZZ: `coverage: partial`, `checked`, and `omits` naming the Joe Henderson Lab. Its
  `note:` is rewritten here rather than in step 7, because the old one — "an empty
  late-August week here is real, not a fetch failure" — contradicted the new keys on the
  same entry. The two Lab pages are named in the note as things to read, not as coverage:
  they disagree with each other entirely, so neither's silence means a dark hall.
- DNA Lounge: `coverage: partial`, `checked`, `omits` naming the club, film and variety
  nights, and a two-address `fallback:` (Songkick, then JamBase — both, because they
  differ). The note records that the club's own calendar answers a browser and refuses the
  unattended run, so it is partial *for that run*; a session that can read the calendar
  has all of it.
- The file's header defines `season_ends`, `coverage`, `omits`, `checked` and `fallback`.

`prompts/weekly-research.md` tells the run what the three keys mean and that every
`coverage: partial` entry gets a standing line under "What could not be reached" each
week, naming what is omitted and not estimating how much, with an example line for each
venue. `prompts/weekly-run.md` is unchanged, so no paste is owed (§3).

`python3 scripts/drift.py`, before (on `main`) and after:

```
check 3 · declared, not producing: 60 tier-1 entries, 60 ever matched a listing, 0 out of season — 5 with nothing in the last 4 weeks
check 3 · declared, not producing: 60 tier-1 entries, 60 ever matched a listing, 2 out of season — 3 with nothing in the last 4 weeks
```

Self-test 43/43, exit 0. The gate's last lines (`bash scripts/verify.sh`, exit 0):

```
passed 10   failed 0   skipped 0   warnings 3
note: 3 warning(s) — repeat each one in the report; a warning does not block.
  WARN  Filoli is declared tier 1 and has produced no listing in 4 weeks
  WARN  Felton Music Hall is declared tier 1 and has produced no listing in 4 weeks
  WARN  Sweetwater Music Hall is declared tier 1 and has produced no listing in 4 weeks
VERIFICATION PASSED — safe to merge.
```

The three left are step 7's. Rehearsed against next week as well — `data/` and `digests/`
copied to a scratch directory with a 12 October week added — self-test 45/45, exit 0.

**Not proven, and not provable here:** that the unattended run writes the standing lines.
`coverage` is read by no check (§9), so the first evidence is Monday's digest.

### Step 6 — the DICE route for Kilowatt and The Knockout · 9 October 2026

Neither venue's page carries a date a fetch can read; each draws its calendar with a DICE
ticketing widget. New `scripts/dice.py` does what a visitor's browser does — reads the
widget's settings off the venue's page, asks DICE for that venue's events, and prints
them with times on the venue's clock. Read on 9 October, for 9–18 October:

| Venue | Page | The command gave | Published before, per week |
|---|---|---|---|
| Kilowatt | `kilowattbar.com/events` | 16 events, all "Kilowatt, San Francisco" | 0 in five of nine weeks, 1 in four |
| The Knockout | `theknockoutsf.com/` | 18 events, all "The Knockout, San Francisco" | 0 in six of nine weeks, 1–2 in three |

`sf.funcheap.com/venue/the-knockout/`, read the same day, listed one event in that span —
a free film night on 12 October that DICE does not carry. So neither is the whole
calendar, and The Knockout's entry says to read both.

**The key.** It is read from the venue's page on each run, sent in the one request, and
written nowhere. The script has no option that prints or accepts one. Proof:

- Live, both venues: the key (40 and 48 characters) was compared in memory with
  everything the script printed — `key in output: False`, over 72 and 69 lines.
- Offline self-test, 9/9, run by the gate and by CI. Planted (`plant matched: 1`): the key
  moved from the request's header into its address → `7/9`, exit 2, naming both cases;
  restored → 9/9.
- An error names only the address and the status, never the request.

**Could-not-read is its own outcome.** A page with no widget (`dnalounge.com`) and a host
that does not exist both exit 2 with `COULD NOT READ`; the run prompt says that means
unreached, never "nothing on". A machine with no timezone data exits 3 rather than print
a time it cannot vouch for; the gate reads that as SKIPPED.

**Differs from §2 in one way.** §2 calls this a fallback. For both venues it is the
primary route — there is nothing else to fall back *from* — so the entries carry a new
key, `how:`, giving the command, and The Knockout's Funcheap page becomes its `fallback:`.

**Not proven, and not provable from here:** that the unattended run's machine can reach
`partners-endpoint.dice.fm`. If it cannot, the run is told to report both venues as
unreached and carry on as before, and check 2 will name them once they have a history.
Monday's digest is the evidence. Also unproven beyond today: DICE lists from the current
day forward, so a run late in a window would miss the days already gone.

The gate (`bash scripts/verify.sh`, exit 0): `passed 11   failed 0   skipped 0
warnings 3` — the eleventh check is the self-test.

### Step 7 — known-wrong entries and three quiet venues · 9 October 2026

Every address below was read on 9 October **with the fetch tool the unattended run uses**.
The 8 October route research measured pages with `curl` and judged several unreadable
past 100 KB; the fetch tool read all of them to the end, so those judgements did not hold.

| Entry | Was | Now | What the page gave |
|---|---|---|---|
| ODC Theater | absent | added, `odc.dance/calendar` | 4 dated performances 16–29 Oct, with times |
| Smuin Contemporary Ballet | absent | added, homepage; answers for "Cowell Theater" | 5 productions with ranges and links; `/events/french-kiss/` gave six dated Cowell performances |
| American Conservatory Theater | absent | added, season page; answers for "Toni Rembe Theater" | six runs with dates; no curtain times; *Oh, Mary!* is at the Curran |
| Fort Mason Center | `/calendar/` — navigation only | `/events/` | 12 exhibitions and series, none at the Cowell |
| Chronicle Datebook | a redirect the fetch tool will not follow | `fetchable: false` | the redirect's target and `/datebook-picks/` both return an error page |
| Thee Stork Club | right URL, note saying it fetched empty | note rewritten | 17 dated events 9–31 Oct, with times |
| Z Space | homepage, note naming old shows | note rewritten, "Z Below" declared | eight show links without dates; `/lear` gave dates, times and room |
| 924 Gilman | landing page with no shows | the ticketing page its TICKETS button opens | 13 dated shows to 6 Dec, with prices |
| SFJAZZ | stale August note | done in step 5 | — |
| Felton Music Hall | homepage, empty to a fetch | `/events` | 15 shows, 10 Oct – 17 Dec |
| Sweetwater Music Hall | homepage, next four dates only | `/events/?view=list` | 16 shows, 9–25 Oct |
| Filoli | a Fever page with one price card | `filoli.org/events/`; "Filoli Summer Stage" declared | Nightfall and Autumn Days, 26 Sep – 1 Nov, among tours and tastings |

**The three quiet venues each get a route fix. None is removed and none has a season
that has ended, so nothing here went to the owner.** Felton and Sweetwater are `outer`
venues, where the brief admits only what would be a top-three event of the week — so some
quiet weeks there are a decision. Their notes say so. Whether check 3 should go on warning
about an outer venue that is quiet by decision is not settled here; it needs a few weeks
of the fixed routes first.

Seat counts on the three new entries are `null`: none was read that day.

`python3 scripts/drift.py`: self-test 43/43, exit 0, `63 tier-1 entries, 62 ever matched a
listing, 2 out of season — 4 with nothing in the last 4 weeks`. The four: Filoli, Felton
and Sweetwater, which stay until a run lists them through the new routes, and **ODC
Theater, new** — declared today, never listed, with performances on 16–18 October for
Monday's run to find. Gate: `passed 11   failed 0   skipped 0   warnings 4`, exit 0.

**Not proven:** that the run follows the links the notes tell it to (Z Space, Smuin). No
check reads that; the digests will show it.

### Closing — the owner's check, and what was left for the backlog · 9 October 2026

**The behavioural check (§8) is a page and a script.**
[`handoff/rot-checks-walk.html`](../handoff/rot-checks-walk.html) gives the owner four
commands; each runs `handoff/rot-checks-walk.sh <1–4>`. Steps 1–3 clone the repository to
a temporary directory, check out `ac372e5` (`main` when step 7 went live), damage the
clone, and run the real `scripts/verify.sh` inside it; step 4 runs the gate on the
checkout as it stands. The script prints the gate's own FAIL, BLOCK, WARN and summary
lines unaltered, then a verdict worked out from the gate's exit code and its text.

All four, run on 9 October:

| Step | Changed in the clone | Gate said | Exit | Verdict |
|---|---|---|---|---|
| 1 | "The Fillmore" → "Fillmore", 5 listings | `BLOCK  “Fillmore” (San Francisco, 5 listing(s)) is a new spelling of “The Fillmore”` · `passed 10   failed 1` | 1 | YES |
| 2, first half | The Regency's "Thin this week" line deleted (1 match) | `BLOCK  Regency Ballroom: 1 listing(s) after 2, 2, 4, 5. 2026-10-05.md does not account for it` | 1 | — |
| 2, second half | The line restored | `ok     Regency Ballroom … accounted for` · `passed 11   failed 0` | 0 | YES |
| 3 | Oakland Arena's entry renamed in `sources.yml` (1 match) | the four standing warnings and `WARN  Oakland Arena (Oakland) has been listed in 4 weeks and is not in sources.yml` · `warnings 5` | 0 | YES |
| 4 | nothing | `passed 11   failed 0   skipped 0   warnings 4` · `VERIFICATION PASSED` | 0 | YES |

**The walk is proven able to say NO.** Pinned instead to the commit before `drift.py`
existed, step 1's planted spelling passes the gate and the walk prints `MATCHES WHAT THIS
STEP SHOULD SHOW: NO`. With the planted spelling pointed at a room that is not in the
week, it stops with `THE CHANGE MATCHED NOTHING … nothing was tested`, exit 2, before the
gate runs.

**The owner walked it; his notes came back on 10 October.** All four steps ticked, each
with the script's last line reading YES: the misspelled venue refused with both spellings
named; the thin venue refused without its line and let through with it; five warnings
shown and the week still passing; the live week passing. The page asked him to judge the
wording and the strength of each safeguard, since the script already reports whether a
step matched. He left one note, on step 2 — whether the Regency's line is a good enough
answer and whether naming the digest as `2026-10-05.md` is clear: "seems fine". No change
was asked for on any step. He ran it in Ghostty rather than Terminal.

**What went to `BACKLOG.md`,** as §7 decision 2 and the handoffs promised: the owner's
check; a record of the first unattended run (12 October) and the three things only it can
prove; the two questions waiting on evidence (outer venues quiet by decision, and check
4's whole-history count); the mark on uncertain listings, decided 9 October; and the
per-source run log.
