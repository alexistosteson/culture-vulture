# The unattended run's closing report — week of 12 October 2026

Saved 12 October from the owner's paste, because the report otherwise exists only in the
session that wrote it. Verbatim, except that two fragments of app interface text that the
paste picked up mid-sentence are removed. This is the raw material for both builds in
[`session-2026-10-12-proposals-and-notes.md`](session-2026-10-12-proposals-and-notes.md).

---

Published. `verify.sh` exit 0 — `passed 11, failed 0, skipped 0, warnings 8`, "VERIFICATION PASSED — safe to merge." Merged `week/2026-10-12` into `main` with `--no-ff` and pushed. `origin/main` is now `18051f6`; `docs/events.json` on main reads window 2026-10-12 → 2026-10-18, 415 events, 8 featured, five regions from `brief.yml`. No notification sent — the week published cleanly and nothing needs you.

One note on the gate: the first run reported `SKIP jsonschema not installed`. `pip` installs to Python 3.13 while `python3` here is 3.11, so `pip install jsonschema` silently did nothing. Installing via `/usr/local/bin/python3 -m pip` made the check binding, and it then failed — two of my event ids had capital letters. Fixed, re-ran, clean. That skip was hiding a real error.

## The two or three things most worth doing

1. heavens to betsy at Bottom of the Hill, Sat 17 & Sun 18, $35. Corin Tucker and Tracy Sawyer's pre-Sleater-Kinney band, two records of riot grrrl at its least compromised, two nights in a 350-cap room. Hasn't happened in thirty years and won't again.
2. Market Street Arts & Theater Festival, Sat 17, 4–11pm, free. First year: six blocks of mid-Market, three plazas, 104 partners, 50+ performances, nearly all free — BANDALOOP down a building, Dear San Francisco, D'Arcy Drollinger. The largest free programming that street has had in a decade, and it collides with everything.
3. Friday Nights at OMCA, Fri 16, 5–9pm, free. Sixty years since the Black Panther Party was founded in Oakland; OMCA holds the archive, so the anniversary falls to it. MacArthur Maze on the Garden Stage, galleries open.

Honourable mention: Joe Bataan free in Yerba Buena Gardens, Sat 17 at 2pm — the man who invented Latin soul in 1967, still fronting the band at 84, for nothing.

## Sources I could not reach

* Litquake — the biggest gap. Mid-run (8–24 Oct, 27th year), schedule hosted on sched.com, which 403s on every path including per-day views. Six listings recovered from search indexes and venue pages; a festival of 80+ events is represented by six.
* DNA Lounge — `/calendar/2026/10.html` and `/calendar/` both HTTP 503. Both mirrors read; both agree on two concerts. Two is a floor. Third week running.
* SFJAZZ — partial as always: Miner Auditorium only, sfjazz.org 403s, no start times published anywhere. Joe Henderson Lab checked on both mirrors — nothing before November, and the two mirrors share no dates, exactly the disagreement `sources.yml` warns about.
* A.C.T. — publishes no curtain times at all. Rather than guess, each production is listed once on a date the source states; under-counts A.C.T. by ~8.
* UNAFF (`unaff.org/2026/` returned title only), Green Film Festival (503), SF Playhouse (`/get-tickets/` 503 — resolved via the production page), Chase Center, 1015 Folsom, The Great Northern, The Midway (all client-side), Stanford Live and Cal Performances (both served unfilled `{{event.Title}}` templates), Dance Mission (empty), Visit Oakland and SF Station (empty calendars), DoTheBay/Bandsintown/Chronicle (403 domain-wide, no fetch spent).
* Roxie — reached, but only on the second attempt. A plain fetch returned Sunday the 18th and silently omitted Saturday the 17th. Re-reading from a character offset produced nine Saturday screenings. Nine of the 36 Roxie listings exist only because the page was read twice. Same class as the 7 October truncation; worth making routine.
* Genuine zeros, reached and confirmed: Berkeley Rep (Liberation opens the 23rd), 924 Gilman (next show the 23rd), Paramount, Hammer Theatre, Shoreline. Mill Valley Film Festival resolved — the 49th ran 1–11 Oct and closed on the 11th, so it doesn't touch this window; aggregators claiming it runs to the 16th are wrong.

Low confidence (7): R-Evolution sculpture final day (listing's own text contradicts the date); Makenzie at Yoshi's (sweep only, venue calendar disagrees); three UNAFF umbrella listings (no programme readable); Lil Darkie at Neck of the Woods (sweep only, undeclared venue); Judy Collins — the hall is unconfirmed, the sweep names Cal Performances as presenter, not the room.

Medium confidence (14): five Litquake listings with unconfirmed times; Love Spells (August Hall's own page and the sweep say August Hall, the Café du Nord calendar also carries it); Movies at Mechanics' (no title or price); Pedro Fernandez at San Jose Civic (sweep only); the Knockout's Saturday 9pm party (two names, one hour, one room per the venue's own guidance); Sam Grisman Project, Rainbow Girls, Diplo's Run Club (listings disagree on whether the set is 9am or 9pm). Also flagged in the digest: Shovels & Rope at the Guild — the listing says the 16th, the ticket link says 17 Oct.

## Warnings — all eight, verbatim

```
WARN  Felton Music Hall is declared tier 1 and has produced no listing in 4 weeks
WARN  Sweetwater Music Hall is declared tier 1 and has produced no listing in 4 weeks
WARN  California Theatre (San Jose) has been listed in 3 weeks and is not in sources.yml
WARN  Curran Theatre (San Francisco) has been listed in 3 weeks and is not in sources.yml
WARN  Eclectic Box (San Francisco) has been listed in 3 weeks and is not in sources.yml
WARN  Ferry Building (San Francisco) has been listed in 3 weeks and is not in sources.yml
WARN  Frost Amphitheater (Stanford) has been listed in 3 weeks and is not in sources.yml
WARN  Neck of the Woods (San Francisco) has been listed in 3 weeks and is not in sources.yml
```

Causes: Felton (6 shows read) and Sweetwater (7 shows read) are editorial zeros under `coverage.outer_threshold`, not reachability failures — both calendars read in full. The six undeclared rooms are reached via sanjose.events, A.C.T., the ticketing sweep, Downtown SF and the sweep respectively. All repeated in the digest with their causes.

No skipped checks after the jsonschema fix.

## Proposals (nothing in `config/` or `prompts/` was touched)

1. Add six `observed_venues` entries with the routes above: California Theatre (San Jose — `sanjosetheaters.org/theaters/california-theatre/` now 301s to `sanjose.org/listings/california-theatre`, which carries no events; the working route is sanjose.events), Curran Theatre, Eclectic Box, Ferry Building (via Downtown SF), Frost Amphitheater (Stanford Live's calendar is template-only), Neck of the Woods.
2. Add Montalvo Arts Center (Saratoga) as tier 1 south_bay — the Carriage House books real concerts and it was absent; `montalvoarts.org/events/` gives dates but no times, `my.montalvoarts.org/events` is the full calendar.
3. Add a `coverage: partial` + `omits:` block to the A.C.T. entry — "no curtain times anywhere on the site" is exactly the standing-line case, and it would put A.C.T. in What could not be reached every week automatically.
4. Note on the Roxie entry that its calendar must be read twice (second read from an offset), because a truncated fetch drops a whole day and looks like a dark one.
5. Litquake needs its own `fetchable: false` tier-2 entry pointing at Funcheap and 7x7 as the reachable routes, since sched.com will 403 every October.
6. Starline Social Club — the sweep returned an 18 Oct show at "Starline", Oakland; `sources.yml` records it closed since 11 June. I did not publish it and did not resolve the conflict. Worth checking whether the room reopened.
7. No vocabulary or region additions needed. But five listings are filed by proximity to cities absent from `regions[].includes`, all flagged in their notes: Half Moon Bay and Daly City → peninsula, Stanford → peninsula, Pleasant Hill, El Cerrito, Orinda and Richmond → east-bay. Half Moon Bay recurs every October (pumpkin festival + weigh-off) and Stanford recurs most weeks; both are candidates for the `includes` lists.
8. One editorial call to flag: the SF Opera Costume Treasure Hunt & Sale (Sat 17, Burlingame) matches `exclusions.hard` on the keyword sale, but that filter's stated reason is "commerce wearing a culture costume" and this is the literal inverse. I included it on the rationale rather than the keyword. Reverse it if you disagree.

## Busy or quiet

Unusually busy — the largest week this digest has covered: 415 listings against 359 last week, and Saturday alone has 94, the heaviest single day recorded. Four drivers: a fully switched-on autumn theatre season (Phantom and Dracula both mid-run with weekend doubles, Peter Pan Goes Wrong at 8 performances, Manon opening, Assimilation opening, two A.C.T. runs); four multi-night residencies (Lila Downs ×3, Neurosis ×2, Jessie Ware ×2, Rush ×2) which is the deepest the digest has seen; three outdoor festivals stacked on one Saturday (Market Street, Day Trip, Half Moon Bay) plus T-Pain in Golden Gate Park; and 101 free listings, buoyed by Autumn Lights, Sunday Streets' season finale and the de Young/Legion free day.

Counter-signal worth noting: Monday's 18 listings are the thinnest night recorded, and that is real, not a research failure — the week front-loads nothing and everything arrives from Thursday. The outer region has just two listings (Bonnie Raitt, Alborosie) because nothing else cleared the drive threshold; the Peninsula has 18, with every summer series finished for the year.
