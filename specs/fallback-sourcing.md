# Spec — Deliberate fallback sourcing

**Tier: probe.** Short-form spec, a behavioural check the owner can run, and the
fetch evidence below. No plan, no audit, no tier registry, no merge ritual owed.
The deliverable of this branch is the decision and the table, not a pipeline.

**Status, 7 October 2026.** The two false Davies Symphony Hall listings this spec
uses as its worked example were removed from the published week in `53ceb79`, and
`digests/2026-10-05.md` carries a dated correction notice. The Fleming dates were
confirmed three ways before removal: `data/2026-09-28.json` carries all three real
performances (1, 3 and 4 October), a fresh JamBase fetch shows Davies dark 5-11
October, and a review of the run was already published. Nothing else proposed here
has been implemented — `config/`, `prompts/` and `scripts/` are untouched.

## What

A hard core of venues fail to fetch week after week. The run currently does one
of two things, unsystematically: finds the listing some other way (usually a
JamBase per-venue mirror or a Songkick sweep), or reports the venue unreachable.
This spec makes that choice deliberate: **a declared per-venue route, a declared
plausibility floor, and a rule for when a fallback listing may be published at
all.**

It is not a framework. It is four changes: routes and floors into
`config/sources.yml`, a two-paragraph discipline into
`prompts/weekly-research.md`, one mechanical check into `scripts/verify.sh`, and
a convention for `confidence` and `note` that needs no schema change.

The thing that forced it: on 2026-10-07 I fetch-tested the repeat offenders. The
result is not "fallbacks are risky." It is that **the current fallback practice
is already publishing false listings and already hiding large holes**, and that
most of the holes have a working route nobody wrote down.

---

## Evidence — per-venue fetch test, all probed 2026-10-07

Window references are the published week `2026-10-05`–`2026-10-11` and the next
window `2026-10-12`–`2026-10-18`. "Published" = listings in
`data/2026-10-05.json`.

| Venue | Failure mode (weeks seen) | Route tested 2026-10-07 | Result | Gives | Omits | Trust |
|---|---|---|---|---|---|---|
| **SFJAZZ — Miner Aud.** | `sfjazz.org` 403 every path incl. `/sitemap.xml` (8 wks) | `jambase.com/venue/miner-auditorium-sfjazz-center` (in `sources.yml`) | **works** — 33 shows, Oct 9 2026 → May 29 2027 | date, artist, support billing, occasional time | **the whole second hall**; price; door time | High *for Miner only* |
| **SFJAZZ — Joe Henderson Lab** | not sourced at all; no entry exists | `jambase.com/venue/joe-henderson-lab-sfjazz-center` | **404** | — | — | — |
| " | " | `songkick.com/venues/2588888-joe-henderson-lab-sfjazz-center` | **works but near-empty** — 3 shows, all Nov 6–8 | date, artist | **all October programming** | Low — silent zero |
| **SF Symphony / Davies** | `sfsymphony.org` 302 → `waitingroom.sfsymphony.org` on *every* path, incl. the season-calendar PDF under `/media/` (5 wks) | `jambase.com/venue/davies-symphony-hall` | **works** — Oct 12 Einaudi, Oct 17 SFS, Oct 19 Lage, Oct 23–24 Hisaishi; **nothing Oct 5–11** | date, artist | programme detail, times, Henderson-style small-hall dates | **High — and it was right** |
| " | " | ticketing/resale sweep (what the run used) | **works and is wrong for the window** — *Renée Fleming Sings Strauss* is **Oct 1 (2pm), Oct 3 (7:30pm), Oct 4 (2pm)**, confirmed via the 26/27 season listing and two resale pages | date, time | — | **Low for existence** — date-shifted a closed run into the live window |
| **DNA Lounge** | `/calendar/{YYYY}/{MM}.html` 503 to WebFetch; raw `curl` is **connection-reset by the host after ~12s** (proxy log: 39 B received) — not a transient 503 (4 wks) | `jambase.com/venue/dna-lounge` | **works** — 3 in Oct (8, 11, 13) | date, artist, support | club nights (Bootie, Death Guild, Hubba Hubba), times, prices | Medium, partial |
| " | " | `songkick.com/venues/7516-dna-lounge/calendar` | **works** — 4 in Oct (8, 11, 13, 16) | date, artist | same club nights | Medium, partial |
| " | " | `sf.funcheap.com/venue/dna-lounge/` | **works** — 1 (Oct 9 *Mortified*, 7:30–9:30pm, $15) — **a show neither mirror has** | date, time, price | music bookings | Medium, orthogonal |
| " | " | `web.archive.org/web/…/calendar/2026/10.html` (snapshot 2026-09-19 exists per `archive.org/wayback/available`) | **blocked by egress policy** from this environment | — | — | **unavailable here** |
| **Kilowatt** | own site is Squarespace; `/events` is an **empty page with an embedded `widgets.dice.fm` widget** (5 wks) | `partners-endpoint.dice.fm/api/v2/events?page[size]=50&filter[venues][]=Kilowatt`, header `x-api-key:` the widget key in the venue's own page source | **works — 50 events**; **8 in Oct 5–11** vs **1 published** | date+time (UTC), full lineup, `status: cancelled`, genre tags, link | price (`null`) | High on content, **low on durability** |
| " | " | same endpoint, `filter[venues][]=The Knockout` / `Bottom of the Hill` | **works — key is not venue-scoped** (10 each); `DNA Lounge`, `Thee Stork Club` → 0 | " | " | " |
| **Thee Stork Club** | `theestorkclub.com/calendar/` renders client-side, empty (per its own `note:`) | `jambase.com/venue/thee-stork-club` | **works** — 10 Oct shows (7, 8, 9, 14, 15, 18, 21, 22, 23, 25) | date, artist, support | times, prices | High |
| **The Masonic** | client-side / no dated listings (4 wks) | `jambase.com/venue/the-masonic` | **works** — 4 Oct shows with support acts | date, artist, support | times, prices | High |
| **The Midway** | `themidwaysf.com` **403** to both WebFetch and `curl`; `/calendar` 403 (5 wks) | `jambase.com/venue/the-midway-sf` | **404** | — | — | — |
| " | " | `songkick.com/venues/3013529-midway/calendar` | **works** — 26 shows; correctly shows **two rooms** on Oct 10 (Polo & Pan + Tinlicker) | date, artist, room implied by paired entries | times, prices, room names | Medium — 1 entry for Oct 17 at a 2-room Fri/Sat venue is thin |
| **A.C.T. (Toni Rembe / Strand)** | `act-sf.org/whats-on/` **fetches fine** — it genuinely has no per-date times (5 wks) | `act-sf.org/whats-on/` | **works** — 11 productions with date ranges; *Oh, Mary!* Oct 13–Nov 1, *Every Saturday Night* Oct 10–Nov 1 | date ranges, titles | **curtain times, by design** | High for runs, nil for times |
| " | " | `tickets.act-sf.org` | **503** | — | — | — |
| " | " | `sfstation.com/theater-performance-arts/calendar/bay-area/MM-DD-YYYY` | **works** — per-date grid; A.C.T. Toni Rembe shows **`"tba"`**, but A.C.T.'s **Strand** show gives `7:30pm`, and Curran *Oh, Mary!* gives `7pm` | date + time for most houses | times for Toni Rembe specifically | High for date, **honest about the missing time** |
| **San Francisco Playhouse** | `/calendar/` fetches fine — season ranges only, no per-date times (7 wks) | `sfplayhouse.org/calendar/` | **works** — *Peter Pan Goes Wrong* Sep 26–Nov 28 | date range | times (box office only) | High for run, nil for times |
| " | " | `ci.ovationtix.com/35293` | **shell only** — "AudienceView Professional", no listings server-side | — | — | — |
| **Z Space** | no central calendar; `/calendar` 404 (5 wks) | `zspace.org/` → enumerate slugs → fetch each | **works** — homepage lists **8** production slugs (`/lear`, `/iphigenia`, `/sfdanceworks-season-9`, `/sketch-on-speed`, `/wfwassimilation`, `/word-for-wordplay-spooky-fam-jam`, `/salt-and-spirit`, `/fall-of-freedom`); `/lear` gives **Thu/Fri/Sat 7pm, Sun 2pm, to Oct 11** | per-date curtain times, run end | price; **no dates on the index itself** | High — costs 1 + N fetches |
| **ODC Theater** | `odc.dance/performances` **404** (7 wks, 0 listings ever) | `odc.dance/calendar` | **works** — 11 performances Oct 2 → Dec 13 **with times**; Printz Dance Project **Oct 16 7:30pm, Oct 17 7:30pm, Oct 18 4pm** | date, time, title, presenter | price | High — **one URL fixes a 7-week hole** |
| **Smuin Contemporary Ballet** | reported "unreadable"; `/performances/` 404 | `smuinballet.org/` (bare domain) | **works** — *French Kiss* at **Cowell Theater, Fort Mason, Oct 9–18**; *After Hours* Oct 17 | date ranges, venues, season | per-date times | High — **it was never unreachable** |
| **Dance Mission Theater** | `dancemission.com` returns **HTTP 202, 168 bytes** (bot interstitial) (3 wks) | `sf.funcheap.com/venue/dance-mission-theater/` | **works** — Oct 9 *Tubong to Living Ancestors* 8–11pm, $30 adv | date, time, price | the rest of the calendar | Medium, one-event-deep |
| " | " | `sfstation.com/dance-performance/calendar/bay-area/MM-DD-YYYY` | **works** — Oct 16: 4 dance events with times across Cowell/ODC | date, time, venue | price, support | **High — best single route for the dance gap** |
| **Mill Valley Film Festival** | own site reported unreadable for a dated programme (2 wks) | `mvff.com/wp-content/uploads/2026/09/MVFF49_Schedule_digital.pdf` | **works** — 6-page **dated grid, every day Oct 1→11**, 8 screens (Sequoia 1/2, Rafael 1/2/3, Lark, BAMPFA, OAC), hour-by-hour | date, **time**, film, screen | price | **High — needs `pdftotext`, not WebFetch** |
| **Roxie Theater** | partial fetch, stopped after Friday (7 wks; `sources.yml` url is the bare domain) | `roxie.com/calendar/` | **works** — **Oct 1 → Dec 19, ~180 screenings with showtimes** (page is 101 KB; WebFetch truncates at 100 K — use `offset`) | date, time, title, series, both screens | price | High — **truncation, not a fetch failure** |
| **Fort Mason Center** | `fortmason.org/calendar/` fails; `sources.yml` still points there (6 wks) | `fortmason.org/events/` | **works, wrong thing** — 12 entries, mostly ongoing exhibitions, **no times**, and **no Cowell Theater performances** (misses Smuin, which is in the building) | exhibition runs | the performance calendar entirely | Medium for galleries, **nil for the halls** |
| **924 Gilman** | landing page only; shows behind a ticketing link; `/shows/` 404 (6 wks, intermittent) | `songkick.com/venues/31164-924-gilman/calendar` | **works and says "0 Upcoming"** — only past dates | — | **everything**, silently | **Low — the dangerous kind of zero** |
| " | " | web search | Ho99o9 + N8noface + Slay Squad, **Oct 24, 8pm, from $27** — exists, is on resale sites, is in no mirror | date, time, price | reliability, repeatability | Low — not a route, a one-off |
| **The New Parkway** | full client-side SPA; `/` is 9.6 KB, `/events/` renders "Loading…", no `ld+json` Event, no ticketing host in source (6 wks, 0 listings ever) | `moviefone.com/showtimes/theater/the-new-parkway-theater-oakland/…` | **works and is empty** — "No showtimes for this date" | — | everything | **none — dead end** |
| **1015 Folsom** | `1015.com` returns **HTTP 202, 168 bytes** (bot interstitial) (6 wks) | `tixr.com/groups/1015folsom` | **403** | — | — | — |
| **Chase Center** | `/events` renders empty (6 wks) | `chasecenter.com/events` | **empty** — title only | — | — | none (deprioritised by the brief anyway) |
| **Visit Oakland** | calendar shell, `### Results` then nothing (8 wks) | `visitoakland.com/events/` | **empty** | — | — | none |
| **ArtSpan SF Open Studios** | `artspan.org/sf-open-studios` returns **1.4 KB, no content**; `sf.funcheap.com/venue/artspan/` 404 | both above | **empty / 404** | — | — | none found |
| **Bandsintown** | 403 domain-wide (`fetchable: false`) | `bandsintown.com/v/…-sfjazz-center` | **403 — `sources.yml` is correct** | — | — | — |

### Route families, tested rather than brainstormed

| Family | Verdict 2026-10-07 |
|---|---|
| **JamBase per-venue** | Best single family. Carries **support billing**, which is why `sources.yml` already promotes it to de-facto tier 1. Slugs are **not constructible** — `the-midway-sf`, `kilowatt`, `joe-henderson-lab-sfjazz-center` all 404. Must be discovered once and written down. |
| **Songkick per-venue** | Works, but the venue page shows a **truncated preview** (Miner showed 5 of 14); append **`/calendar`**. IDs are not guessable — a guessed ID returned *Armagh City Hotel, Northern Ireland*, which would have been published as SFJAZZ. **Never construct a Songkick ID.** |
| **DICE partner endpoint** | Highest fidelity found anywhere, including `status: cancelled` which no venue page gave. Reached by lifting a public widget key out of the venue's own page source. Covers the DIY/small-room tier the project under-covers worst. **Most likely of all routes to break, and the one I would least want load-bearing.** |
| **Venue `sitemap.xml`** | 403 wherever the site 403s (SFJAZZ). Useless against the actual failure mode. |
| **JSON-LD `Event` blocks** | Tested on five client-side venues. Kilowatt had `LocalBusiness`/`Organization`/`WebSite` only; New Parkway one non-Event block; the rest none. **No venue tested exposed an `Event` block.** |
| **ICS / Squarespace `?format=ical`** | `kilowattbar.com/events?format=ical` returns **HTTP 200 with HTML** — a false positive that looks like success by status code alone. 0 VEVENTs. |
| **Funcheap per-venue `/venue/<slug>/`** | **Real and undocumented** — works for `dance-mission-theater`, `dna-lounge`; 404 for `the-midway`, `artspan`. Shallow (1 event) but **orthogonal** to the music mirrors. Consistent with the file's existing warning not to construct Funcheap URLs. |
| **SF Station per-date, per-section** | **Real and undocumented**: `/theater-performance-arts/calendar/bay-area/MM-DD-YYYY` and `/dance-performance/calendar/bay-area/MM-DD-YYYY`. Gives date **and** time, prints `"tba"` where the time is genuinely unpublished. `sources.yml` lists only `sfstation.com/` with strength "clubs and galleries". |
| **Festival schedule PDFs** | MVFF's is a complete dated grid. **WebFetch returns undecoded PDF bytes**; `pdftotext` reads it immediately. A whole class of route the run has been treating as unreachable. |
| **Wayback Machine** | `archive.org/wayback/available` answers, but `web.archive.org` is **blocked by egress policy** in this environment. Not a route here. |
| **Ticketing hosts for theatre times** | Tested Ovationtix/AudienceView (shell only), `tickets.act-sf.org` (503), Tixr (403). **The hypothesis that a ticketing host publishes per-performance times where the venue does not did not hold for any theatre tested.** The only route that produced a theatre curtain time was SF Station. |
| **Generic ticketing/resale sweep** | The route that produced the **two false Davies listings**. It is good at "a ticket exists for this show" and bad at "that show is in this window." |

---

## Q2 — How a fallback listing surfaces itself

Three audiences, three different wants. No schema change is needed for any of
them, and `additionalProperties: false` means a new field is a real cost — so
reuse what exists, but **pin down conventions that are currently prose-freedom**.

**The reader** wants to know whether to trust the time before driving there.
They are already served, and better than I expected: every `low`/`medium` note
in `data/2026-10-05.json` says in plain words what is unverified ("Curtain time
is not published per date — confirm when booking"; "the Chapel's own calendar
shows nothing on the 5th. One of the two is wrong"). **Nothing new is owed to
the reader.** Do not add a "sourced from a mirror" badge: the reader cannot act
on provenance, only on *what specifically might be wrong*, and the note already
carries that. A badge would also need a non-colour encoding and a legend, and
would spend the page's scarce attention on the project's bookkeeping.

**Split `confidence`, because it is currently two things wearing one word.** In
the published week it means both *"this event may not exist"* (Davies) and
*"this event certainly exists, one field is missing"* (A.C.T.). Those want
opposite reader behaviour. Proposed convention, no schema change:

- `low` — **existence or date is in doubt.** One source only and it is a
  mirror, or two sources disagree. The note must name the doubt and the
  disagreement.
- `medium` — **event is certain, a field is not.** Time, price or billing
  missing or house-default. The note must name which field.
- unset (= high) — venue's own calendar, or a mirror that carries the detail.

That single split is worth more than any new field: it restores the signal that
23 `medium` + 12 `low` in one week was dissolving.

**The compiler of next week's run** wants the route, not the prose. Give it
`url` — which `schema/events.schema.json` already declares, which
`BACKLOG.md` row *"Venue / ticket link on the event drawer"* already wants, and
which has **collapsed**: 132/132 populated in `2026-08-24`, 45/305 in
`2026-09-28`, **0/329 in `2026-10-05`**. Populating `url` with the URL actually
read makes provenance a machine-readable fact (`jambase.com` in the host is the
whole signal) and is the cheapest thing on this list. It is also the only part
of the proposal that is checkable by a script.

**The maintainer** wants to know whether a route still earns its place. That
belongs in `sources.yml` — `note:` and `fetchable: false` already exist — plus
the digest's "What could not be reached", which is already the right instrument
and already written well. The gap is that it reports *this week* and never
accumulates, so DNA Lounge's 503 has been rediscovered four times and ODC's
404 seven times without either reaching the source file.

---

## Q3 — The risks, sorted into real and theoretical

**Real, and already happening.**

1. **The silent partial is the whole problem.** A fallback that returns nothing
   fails loudly; one that returns *some* data looks like success and converts a
   visible hole into an invisible one. This is not a hypothetical — it is
   measured three ways on 2026-10-07. Kilowatt: **8 events in the window, 1
   published.** DNA Lounge: three mirrors agree on Oct 8/11/13 and **all three
   miss the club nights**; union of three sources is still roughly half the
   venue. SFJAZZ: the mirror reported one concert and **was correct** — it
   mirrors one of two halls, and the second hall has no route at all. In every
   case the fallback returned data, nothing flagged a shortfall, and the week
   published as complete. **This is the 2026-08-17 failure mode with better
   manners**, and it is the risk the plan must answer.

2. **A fallback already published two false listings.** `data/2026-10-05.json`
   carries *Renée Fleming Sings Strauss* on Oct 9 and *Rachmaninoff Symphonic
   Dances* on Oct 10 at Davies, both `confidence: low`, both with an invented
   `19:30`. The Fleming run was **Oct 1, 3 and 4**. The ticketing sweep was
   showing a closed run; the JamBase mirror correctly showed the hall dark; the
   digest called the mirror the doubtful one. So the current practice does not
   merely risk false positives — it has shipped two, and it resolved a
   two-source contradiction **the wrong way** because it had no tiebreak rule.

3. **No tiebreak rule.** Two readable sources disagreed and the run's response
   was to publish both halves of the contradiction at `low`. That is not
   honesty, it is passing the problem to the reader with a 19:30 attached.

4. **Reporting pressure.** The digest's phrasing is already drifting: SFJAZZ
   went from "**dark, and legitimately so**… an empty week here is the venue's
   calendar, not a gap" (2026-08-17) to "assume SFJAZZ has more on than this
   digest shows" (2026-10-05) — but the *first* framing is still what
   `sources.yml` tells the compiler, in a `note:` written for August and read in
   October. A fallback that returns something makes "I could not reach this"
   feel untrue, and the sentence quietly leaves the report.

5. **The source file rots, and `weekly-run.md` step 8 already permits the fix.**
   `sources.yml` points Roxie at the bare domain when `/calendar/` carries 180
   dated screenings; points Fort Mason at `/calendar/` which fails, while the
   runs have silently used `/events/` for six weeks; points Thee Stork Club's
   machine-readable `url:` at the path its own `note:` calls empty. Seven weeks
   of ODC 404s never became a one-character URL fix (`/performances` →
   `/calendar`). **The rot is not hypothetical and a fallback table would rot
   the same way** — which is the argument for a short table of declared routes
   with a dated last-verified stamp, not a long one.

6. **Confidence laundering.** 23 `medium` + 12 `low` out of 329 is ~11% marked
   in one week, up from 3 marked in `2026-09-07`. Still readable, but the trend
   is the wrong way, and the `medium` bucket is doing two incompatible jobs
   (see Q2). Systematising fallbacks without splitting the enum would push
   everything fallback-sourced to `medium` and kill the mark.

7. **Support billing and attribution.** `sources.yml` already notes JamBase
   "carries support billing" and treats that as a reason to prefer it. The real
   consequence runs the other way for `url`: routing a reader to
   `jambase.com/venue/…` instead of the venue sends the click, and any ticket
   fee, to an aggregator. For a 150-cap volunteer room this matters. **Rule:
   `url` records the route the compiler read; where a venue has a working
   public page at all, the reader-facing link should be the venue's.**

**Real but smaller.**

8. **Hallucination surface.** `sources.yml` already warns tier-3 snippets omit
   the artist name, and the 2026-09-14 run caught Songkick placing Laurie
   Anderson 10 days off and dropped the listing — so the existing discipline
   works. But my own testing produced the clean illustration: a *guessed*
   Songkick venue ID returned a hotel in Northern Ireland, formatted exactly
   like a correct result. **Constructed URLs are the hallucination surface, not
   constructed prose.**

9. **Stale mirrors.** Tested, and milder than feared: the mirrors were
   *current*. Wayback — the genuinely stale route — is egress-blocked here, so
   the question is moot. Keep the rule (publish the snapshot date or do not
   publish) but do not build for it.

10. **Route durability.** The DICE endpoint depends on a client key in a venue's
    page source. It is the best data found and the most likely to break.

**Theoretical — do not build for these.**

11. *Legal/ToS exposure from reading mirrors.* Everything tested is a public
    page or a public widget endpoint, read at human volume, with the venue's
    own site preferred wherever it answers.
12. *Readers stop trusting the digest because of visible marks.* The opposite
    risk is the live one; the marks are the only reason the Davies error is
    survivable.
13. *Fallback sourcing slows the run below the Monday window.* The expensive
    venues are a short list; Z Space's 1 + N fetches is the worst case and it is
    eight extra fetches.

---

## Q4 — The plan

Five load-bearing changes. Two of them are URL corrections that pay for the
whole spec.

### 1. `config/sources.yml` — declared routes, and an honest `expect`

The shape already supports per-source `note:` and `fetchable: false`. Add two
fields and nothing else:

- **`fallback:`** — an *ordered, literal* list of URLs, each with what it gives.
  Literal because every slug family tested is unconstructible. Keep it to the
  venues in the table; a long chain is the thing that rots.
- **`expect:`** — a one-number weekly floor, e.g. `expect: 6` for Kilowatt,
  `expect: 5` for DNA Lounge, `expect: 8` for Roxie. This is the plausibility
  check's input and the single most valuable new field, because it is what makes
  a silent partial detectable.

Cost, stated honestly: `expect` is a human judgement that will go stale, and a
wrong `expect` either cries wolf or licenses a thin week. Mitigation: it is
advisory to the *report*, not to the gate (see 3), and the digest is expected to
say when it was missed and why.

**URL corrections, provable today, already permitted by `weekly-run.md` step 8:**

| Entry | From | To |
|---|---|---|
| Roxie Theater | `https://roxie.com/` | `https://roxie.com/calendar/` — and note the 100 KB WebFetch truncation; re-read with `offset` |
| Fort Mason Center | `fortmason.org/calendar/` | `fortmason.org/events/` — and note it is the **gallery** index; the halls (Cowell, Southside) are **not** on it |
| Thee Stork Club | `theestorkclub.com/calendar/` | `jambase.com/venue/thee-stork-club` (its own `note:` already says so) |
| **ODC Theater** | *not in the file* | add `https://odc.dance/calendar` — `/performances` 404s; **7 weeks, 0 listings, one URL** |
| **Smuin** | *not in the file* | add `https://www.smuinballet.org/` — reported "unreadable"; the bare domain works |
| **A.C.T.** | *not in the file* | add `act-sf.org/whats-on/`, `fetchable: true`, `note:` **no per-date curtain times, ever — this is the venue's choice, not a fetch failure** |
| Davies / SF Symphony | a code comment, and a stale one ("an empty August is expected") | a real entry: `jambase.com/venue/davies-symphony-hall`, `note:` the waiting-room 302 covers **every** path incl. the season PDF; **the mirror outranks the ticketing sweep on existence** |
| SF Station | bare domain, "clubs and galleries" | document the per-date, per-section shapes `/{theater-performance-arts,dance-performance}/calendar/bay-area/MM-DD-YYYY` |
| SF Funcheap | `/YYYY/MM/DD/`, `/region/<slug>/` | add `/venue/<slug>/`, **discovered not constructed** (`dance-mission-theater`, `dna-lounge` exist; `the-midway`, `artspan` 404) |
| **SFJAZZ** | `note:` says an empty week here is "real, not a fetch failure" | **rewrite it.** That sentence was true for August and is now the single most dangerous line in the file. Replace with: the mirror covers **Miner Auditorium only**; the Joe Henderson Lab has **no working route**; SFJAZZ is **permanently partial**. |
| Mark `fetchable: false` | — | Visit Oakland, Chase Center, 1015 Folsom, The New Parkway, ArtSpan, `themidwaysf.com`, `dancemission.com`, `artspan.org` — all tested empty or bot-walled 2026-10-07 |

Also fix while in the file: `Music on the Square` is listed **twice** (tier-1
peninsula *and* `recurring`), its `redwoodcity.org` URL 403s, and its 2026 season
closed 4 September per the 2026-09-21 digest — the `recurring` entry has no
`season_ends:` though the file's own header says that is what the field is for.
`Sips & Sounds of Summer` (Aug–Sep) and `Colma Summer Concert Series` (August)
are likewise past with no `season_ends:`.

### 2. `prompts/weekly-research.md` — two paragraphs, not a procedure

- **A route is read, not constructed.** Never build a JamBase slug, a Songkick
  venue ID, or a Funcheap venue path. Use the literal URL in `sources.yml` or
  find the page by search first. A guessed Songkick ID returned a hotel in
  Northern Ireland formatted exactly like a correct answer.
- **Check the shortfall before you believe the silence.** Compare what a
  fallback returned against `expect:`. A fallback that returns one concert for a
  venue that programmes five nights a week is a failure, not a quiet week — say
  so in "What could not be reached" **even though something came back**. The
  sentence "I could not reach this" stays in the report when the venue is
  partially reached; "reached, partial, N of about M" is the honest form.
- **Two sources disagree → the venue-scoped source wins on existence.** A
  venue-scoped mirror (JamBase/Songkick venue page) outranks a generic ticketing
  or resale sweep on *whether a date exists*. Where they still conflict, publish
  **neither** rather than both: the Davies case shipped two false listings
  because both halves went in at `low`.
- **Never invent a time.** A house-default or absent time is `medium` with the
  field named in the note. A time attached to a date that only one generic
  source asserts is the Davies error.
- **Populate `url`** with the page actually read, and prefer the venue's own
  public page for the reader-facing link where one exists.
- **The `confidence` split** from Q2, stated as the convention.
- Add to the **Verification pass** checklist: *every venue with an `expect:`
  either met it or is named in "What could not be reached"*.

### 3. `validate.py` / `verify.sh` — exactly one new mechanical check

The two scripts are split along "checks the file against itself" vs. "checks the
week against the world," and the split should hold.

**What is mechanically checkable (and belongs in `verify.sh`):**

- **An `expect:` shortfall is named.** For each `sources.yml` venue with
  `expect: N`, count that venue's listings in the newest data file; if the count
  is below `N`, require the venue's name to appear in the digest's "What could
  not be reached" section. Pure text-and-JSON, no network, same shape as the
  existing check #5 (digest/data featured agreement). **This is the check that
  would have caught SFJAZZ** — 1 listing against `expect: 6`, venue not listed
  as a shortfall, FAIL.
- A **`low`-confidence listing must carry a `note`** (already true in practice;
  trivially assertable) — and, worth considering, **must not carry a `start`**,
  which is precisely the Davies 19:30.
- A **`url` coverage floor** on the newest week, as a soft warning in
  `validate.py`. 0/329 is a regression the gate noticed nothing about.

**What can only ever be a reported judgement (and must not be scripted):**

- Whether the fallback's data is *true*. Nothing local can tell that a mirror's
  Oct 9 is a date-shift of a closed Oct 1–4 run.
- Whether a route covers the whole venue. The SFJAZZ one-hall-of-two problem is
  invisible to any count.
- Whether `expect:` is still the right number.
- Whether a contradiction was resolved correctly.

So: **one new required check** (`expect` shortfall named), one small assertion
(`low` ⇒ note, and probably no invented `start`), one warning in `validate.py`
(`url` coverage). No network calls in the gate, ever — a gate that fetches is a
gate that fails on someone else's 503.

### 4. The publication rule

A fallback-sourced listing may be published when **all** hold:

1. The route is **declared in `sources.yml`** for that venue, or the report says
   plainly that it was ad hoc.
2. The route gives a **specific date** for a **specific venue**. A generic sweep
   that asserts a date no venue-scoped source corroborates is **held back**.
3. Any missing field is **absent, not defaulted** — no invented `start`.
4. `confidence` follows the Q2 split and the `note` names what is unverified.
5. The venue's **shortfall against `expect:`** is in the digest, even when the
   listing is published.

And it is **held back** when: two sources conflict on existence or date and the
venue-scoped source does not settle it; the only source is a resale/aggregator
snippet with no artist name; or the only route is a Wayback snapshot (which is
egress-blocked here in any case).

### 5. Venues I recommend **not** fallback-sourcing

Being reported unreachable is the better outcome for these, because every
available route returns a *confident fraction* and nothing marks the fraction.

- **SFJAZZ — the Joe Henderson Lab.** No route exists. JamBase 404s; Songkick
  shows 3 November dates and nothing in October. Keep the Miner mirror; declare
  SFJAZZ **permanently partial** in `sources.yml` and in every digest, and
  delete the note that says an empty SFJAZZ week is real.
- **San Francisco Symphony / Davies, for anything the mirror does not show.**
  The mirror is trustworthy for *existence* and has already been proven right
  against the sweep. Everything the mirror does not carry — programme detail,
  times, small-hall dates — should be **unreported**, not reconstructed. The two
  Oct 9/10 listings now in `data/2026-10-05.json` are the argument.
- **The New Parkway.** SPA with no server-rendered data, no `Event` JSON-LD, no
  ticketing host in source, and Moviefone empty. Six weeks, zero listings.
  Report it unreachable and stop spending fetches.
- **1015 Folsom, Visit Oakland, Chase Center, ArtSpan.** Bot-walled (HTTP 202 /
  168-byte interstitials) or genuinely empty. `fetchable: false` and move on.
- **924 Gilman.** The dangerous case. Songkick says **"0 Upcoming concerts"**
  while a show is on sale for Oct 24. A mirror that confidently returns zero is
  worse than no mirror: it reads as a quiet week. Keep Gilman as a **declared
  known hole** — the 2026-09-28 digest already called it "the week's biggest
  known hole," which is the right treatment — and do not let a zero from
  Songkick stand in for it.
- **Theatre curtain times generally.** A.C.T. and SF Playhouse genuinely do not
  publish per-date times, and no ticketing host tested exposes them. Publish the
  dates with **no `start`** and `confidence: medium`. SF Station is the one route
  that sometimes has a time, and it is honest enough to print `"tba"` — which is
  exactly the behaviour to copy.

### Net effect, counted

Against the published week `2026-10-05`, the declared routes above recover, at a
minimum: **+7 Kilowatt** (8 vs 1), **+3 ODC** in the next window, **Smuin's
Cowell run** (currently 0 listings for a show in SF all week), **the Roxie's
Saturday and Sunday** (the week's partial fetch stopped at Friday), **MVFF's
dated grid** (11 days × 8 screens, currently one umbrella listing), **+9 Thee
Stork Club** and **+4 Masonic** in October, and the **removal of two false
Davies listings**. That is a clear net positive to the listings, and it is
mostly URL corrections rather than new machinery.

---

## Constraints carried

- Short-form spec in root-level **`specs/`**, never `docs/` — `docs/` is the
  Pages web root.
- **Nothing proposed here changes `docs/index.html`.** No new visual encoding,
  so no colour-as-sole-encoding question, no `prefers-color-scheme` block, no
  Bay Area geography in the page.
- **No schema change.** `schema/events.schema.json` sets
  `additionalProperties: false`; the proposal reuses `confidence`, `note`
  (≤400 chars) and `url`, all already declared. If a later spec wants a
  machine-readable provenance field, that is a schema change and owes its own
  spec.
- **`docs/events.json` stays derived**; nothing here edits it.
- **The validate/verify split holds**: `validate.py` checks a file against
  itself, `verify.sh` checks the week's internal agreement. Neither fetches.
- `config/brief.yml` remains the source of truth for geography; untouched.
- Tooling floor unchanged — no new rule families, so no `ruff.toml` or
  `.github/workflows/validate.yml` edit.

## Behavioural check (owner)

1. Open `specs/fallback-sourcing.md` and read the table. Pick any three rows and
   fetch the "route tested" URL yourself — `https://odc.dance/calendar`,
   `https://roxie.com/calendar/` and `https://www.smuinballet.org/` are the
   quickest. Confirm they return dated listings, and that the URLs currently in
   `config/sources.yml` for those venues do not.
2. Open `data/2026-10-05.json` and find the two Davies Symphony Hall listings on
   9 and 10 October. Confirm they are there, at `confidence: low`, with
   `start: "19:30"`. Then confirm against any ticketing page that *Renée Fleming
   Sings Strauss* ran **1, 3 and 4 October**. That is the published error this
   spec exists to prevent, and seeing it is the check.
3. Count Kilowatt's listings in `data/2026-10-05.json` — there is one. Decide
   whether `expect: 6` for Kilowatt is a number you would stand behind, because
   that judgement is the part of the plan that cannot be automated.
4. Decide the one open call this spec deliberately leaves to you: **whether the
   DICE partner endpoint is a route this project should depend on.** It is the
   best data found and the most fragile, and it is reached with a key read out of
   a venue's page source. I have recommended declaring it in `sources.yml` with
   that caveat rather than using it ad hoc; declining it entirely is a defensible
   answer and costs Kilowatt and The Knockout.
5. Confirm nothing was changed: `git status` should show exactly one untracked
   file, `specs/fallback-sourcing.md`, and no modifications to `config/`,
   `prompts/`, `scripts/`, `docs/`, `data/` or `digests/`.

## Evidence

- `grep -n -A40 'What could not be reached' digests/*.md` — plus the variant
  headings `## What I could not reach` (2026-09-14) and `## What this week could
  not reach` (2026-09-21); `2026-08-13` through `2026-09-07` have **no such
  section at all**, which is why the offender history starts at 2026-09-14.
- Per-venue listing counts per week, computed over all nine `data/*.json`:
  SFJAZZ 2/–/–/–/3/1/1/2/1 · DNA Lounge –/3/2/–/1/4/9/2/1 · Kilowatt
  –/–/1/–/–/1/–/1/1 · ODC 0 throughout · Smuin 0 throughout · New Parkway 0
  throughout · Roxie –/9/5/10/10/6/27/10/13. Compare Bottom of the Hill
  3/6/6/7/6/7/5/7/7 — a 350-cap room reporting consistently, which is what a
  working route looks like.
- `confidence` distribution per week: `2026-09-07` 3 marked of 189 →
  `2026-10-05` 35 marked of 329 (23 `medium`, 12 `low`).
- `url` population per week: 132/132 (`2026-08-24`) → 45/305 (`2026-09-28`) →
  **0/329** (`2026-10-05`).
- All fetch tests in the table above, run 2026-10-07 via WebFetch, WebSearch and
  `curl` through the session proxy. `pdftotext` on the MVFF PDF; `pdfinfo`
  reports 6 pages and the day headers run `THURSDAY OCTOBER 1` → `SUNDAY OCTOBER
  11`. The proxy's own `recentRelayFailures` log confirms `www.dnalounge.com:443`
  resets the connection host-side after ~12 s, 39 bytes received — so DNA's own
  calendar is not a transient 503 from this environment.

---

## Draft BACKLOG.md row — not inserted, for the owner to move

> Paste into the table under `## Utility now` → the `| Item | Context | Do it
> when |` table in `BACKLOG.md`. Left here deliberately; this spec does not edit
> the backlog.

| Item | Context | Do it when |
|---|---|---|
| Deliberate fallback sourcing for the venues that never fetch [bug/s3/v2] → spec at [specs/fallback-sourcing.md](specs/fallback-sourcing.md) | **The current practice already publishes false listings and already hides large holes.** `data/2026-10-05.json` carries two Davies Symphony Hall listings (9 and 10 Oct, `confidence: low`, invented `start: 19:30`) for a *Renée Fleming Sings Strauss* run that actually played **1, 3 and 4 October** — the generic ticketing sweep date-shifted a closed run into the live window, the JamBase mirror correctly showed the hall dark, and the digest called the mirror the doubtful one. Meanwhile the fetch test of 2026-10-07 found working routes for holes the run has reported for weeks: **`odc.dance/calendar`** (`/performances` 404s — 7 weeks, 0 listings), **`smuinballet.org`** bare domain (reported "unreadable"; *French Kiss* was at Cowell Theater 9–18 Oct and went unlisted), **`roxie.com/calendar/`** (180 dated screenings; the file points at the bare domain and the week's fetch stopped at Friday), **MVFF's schedule PDF** (a complete dated grid, needs `pdftotext` — WebFetch returns raw bytes), and a **DICE partner endpoint** showing **8 Kilowatt events in the window against 1 published**. `sources.yml` is also actively misleading in two places: its SFJAZZ `note:` still says an empty week there is "real, not a fetch failure" (written for the August off-season, read in October), and the JamBase mirror it names covers **Miner Auditorium only** — the Joe Henderson Lab has no route at all, which is why that venue reports 1–3 listings a week. Also stale: Fort Mason points at `/calendar/` while the runs have silently used `/events/` for six weeks, Thee Stork Club's `url:` points at the path its own `note:` calls empty, `Music on the Square` is listed twice with a 403 URL and a closed season, and three `recurring` series are past their season with no `season_ends:`. **The proposal is small:** per-venue `fallback:` chains (literal URLs — every slug family tested is unconstructible, and a guessed Songkick ID returned a hotel in Northern Ireland) plus a one-number `expect:` floor; a `confidence` split (`low` = existence in doubt, `medium` = event certain / field missing) that needs no schema change since `additionalProperties: false` makes a new field a real cost; restoring `url` (0/329 in the newest week, down from 132/132); and **one** new `verify.sh` check — an `expect:` shortfall must be named in "What could not be reached", which is the check that would have caught SFJAZZ. It also recommends **not** fallback-sourcing six venues (Joe Henderson Lab, Davies beyond the mirror, The New Parkway, 1015 Folsom, Visit Oakland/Chase Center/ArtSpan, and 924 Gilman — where Songkick confidently returns "0 Upcoming" while a show is on sale). | **The two false Davies listings were removed in `53ceb79` (7 Oct), after this spec was drafted** — so the standing argument is the one that remains: the `sources.yml` URL corrections and the SFJAZZ `note:` rewrite are worth doing before the next weekly run — `prompts/weekly-run.md` step 8 already permits fixing a provably dead source URL. The `expect:` floors and the `verify.sh` check want the owner's judgement on the numbers first (see the spec's behavioural check), as does the one open call: whether the DICE endpoint — best data found, most fragile, reached with a key from a venue's page source — is a route this project should depend on at all. |

---

## Addendum, 7 October — the floors, derived; and a claim this falsifies

The owner approved drafting `expect:` floors with real numbers. Deriving them from the nine
weeks already in `data/` rather than authoring them by hand **partly falsifies the proposal
above**, so the numbers and the correction are recorded together.

Method: per declared `tier_1_venues` entry, reconcile canonicalized venue strings against
every `data/*.json`, take the median of the venue's non-zero weeks, and propose
`floor = max(1, 0.4 × median)`.

### What the derivation shows

**1. A floor is only meaningful for about seven venues.** For 31 of 53 tier-1 venues the
formula collapses to `floor: 1`, which detects total disappearance and nothing else — not the
Kilowatt-style partial the check exists for. Venues with a median of 3 or fewer cannot be
discriminated by a ratio.

| Venue | 9-week series | median (non-zero) | proposed floor |
|---|---|---|---|
| Roxie Theater | 0, 9, 5, 10, 10, 6, 27, 10, 34 | 10 | 4 |
| Yoshi's | 3, 7, 5, 7, 7, 4, 7, 7, 6 | 7 | 2 |
| BAMPFA | 0, 4, 5, 6, 7, 2, 8, 7, 10 | 6 | 2 |
| Bottom of the Hill | 3, 6, 6, 7, 6, 7, 5, 7, 7 | 6 | 2 |
| Berkeley Rep | 0, 0, 0, 3, 0, 0, 0, 7, 6 | 6 | 2 |
| Rickshaw Stop | 1, 6, 4, 2, 5, 5, 7, 6, 4 | 5 | 2 |
| Castro Theatre | 1, 1, 5, 6, 5, 4, 1, 6, 6 | 5 | 2 |

Everything below a median of 5 should get **no floor at all**. Use the relative
collapse-vs-trailing-median check on those instead, which needs no per-venue number and
therefore cannot rot.

**2. The floor would NOT have caught SFJAZZ.** This contradicts the claim made in §Q4 above
and in PR #3, and the claim is withdrawn. SFJAZZ's series is `2, 0, 0, 0, 3, 1, 1, 2, 1` — a
non-zero median of 2, so a derived floor of 1, which this week's single concert **passes**.

The reason is the important part: **deriving a threshold from history ratifies whatever
blindness the history contains.** SFJAZZ has been read through a mirror covering one of its
two halls for nine weeks, so its baseline is already suppressed to the level of the fault.
No statistic computed from that series can detect it. The same applies to any venue whose
route has always been partial.

**3. So known-partial routes need a declaration, not a number.** Replace the floor for these
with a `coverage: partial` field naming what the route omits, plus one mechanical rule:

> A source declared `coverage: partial` **must** appear in the digest's "What could not be
> reached" section every week, unconditionally, whatever its listing count.

That is what would actually have caught SFJAZZ — not a threshold, but a standing obligation
to keep saying the route is partial for as long as it is. It is text-and-JSON checkable and
needs no history.

**4. Two tier-1 venues have never produced a reconcilable listing in nine weeks:** The New
Parkway and Music on the Square. The declared-but-never-produced check is cheap and nearly
exhausted on tier 1, which is the argument for running it standing rather than once.

**5. Seven venues carry interior zeros** (Café du Nord, August Hall, The Warfield, SFJAZZ,
Fox Theater, The Greek Theatre, Shoreline) and almost all are real dark weeks. A naive
zero-after-non-zero check fires ~14 times a week across the corpus, mostly on seasonal
venues, and would be ignored inside a fortnight. It is only usable when suppressed by
`season_ends:`.

### Revised recommendation

Three checks that need no authored numbers, one declaration that does:

1. **Venue-string canonicalization** — prerequisite; 5 fragmentations found, 4 introduced by
   the 2026-10-05 run and repaired in `8599b96`.
2. **Collapse vs trailing median** — relative, self-updating, no per-venue config.
3. **Declared but never produced**, scoped to `tier_1_venues` only; aggregators legitimately
   never appear as a venue and a naive scope gives 18 false positives.
4. **`coverage: partial`** on routes known to omit part of a venue, with the standing
   obligation above. This is the only one of the four that carries hand-written state, and it
   is a sentence rather than a number, so it rots visibly rather than silently.

`expect:` floors survive only for the seven venues in the table, and are optional even there.

---

## Addendum 2, 7 October — editorial verification, silent dependencies, and a correction

Three additions, all from tests run after the main body was written.

### 1. A tier of editorial sources, for independence rather than coverage

The audit above tested venue calendars and ticketing mirrors. It did not test **editorial**
sources, and they fail differently in a way that matters: mirrors of a common upstream are
not independent of each other. Three DNA Lounge mirrors agreed and all missed half the
venue. Editorial coverage has a separate reporting chain, so it is the only thing available
that can adjudicate a Davies-class error — one where volume looks normal and the data is
false.

Tested 2026-10-07:

| Source | Result | Verdict |
|---|---|---|
| **BroadwayWorld San Francisco** | `broadwayworld.com/san-francisco/` — readable, no paywall, **dated listings with venue and run dates** | **Adopt.** Best editorial route found, and the only one that names venues this project does not declare |
| SF Standard | `sfstandard.com/arts-culture/` readable, but **teasers only** — no dates, no venues | Keep as described; not a verification route |
| SF Chronicle Datebook | `datebook.sfchronicle.com` **301s** to `sfchronicle.com/entertainment/`, which fails to render; the `/music` path is **410 Gone** | **The declared URL is a dead redirect.** Not the paywall — a dead path plus a JS wall |
| SF Classical Voice | **403** on `/calendar`, `/events-calendar` and the bare domain | Unavailable, and it is the natural check on the Davies error |
| 48 Hills · KQED Arts | **404** on the listing paths; both are declared as bare domains with no working path | Paths need finding or the entries are decorative |
| Bachtrack | Results render client-side; the listing page is a template | Reachable via search only |

**Role in the precedence rule.** As drafted, the rule says an irreconcilable conflict means
publishing *neither*, which loses true listings. An independent editorial source turns a
standoff into a decision, so the rule becomes: venue-scoped source outranks a generic sweep;
where they conflict, an independent editorial source breaks the tie; where none is available,
publish neither and say so.

### 2. Observed but never declared — 27 silent dependencies

The main body proposes a *declared but never produced* check. The mirror image yields far
more. Venues appearing in **3 or more of the 9 weeks**, with a room-like `venue_type`, that
match **no** entry in `config/sources.yml`:

| Weeks | Listings | Venue |
|---|---|---|
| 3 | 17 | San Jose Center for the Performing Arts |
| 6 | 12 | The Midway |
| 3 | 11 | Rooster T. Feathers |
| 5 | 10 | Bill Graham Civic Auditorium |
| 3 | 9 | Mountain View Center for the Performing Arts |
| 3 | 8 | **Davies Symphony Hall** — declared only as a code comment, which is why nothing matched it |
| 7 | 8 | de Young Museum |
| 7 | 8 | Madrone Art Bar |
| 3 | 7 | War Memorial Opera House |
| 3 | 7 | The Masonic |
| 5 | 6 | Legion of Honor |
| 3 | 6 | San Jose Improv |
| 5 | 5 | Solano 2 Drive In |
| 4 | 5 | Swedish American Hall |
| 4 | 5 | Oakland Arena |
| 3 | 5 | Tech CU Arena · Alameda County Fairgrounds · 447 Minna Street |
| 4 | 4 | Toyota Pavilion at Concord · PURE Nightclub · Noe Valley Town Square · Mechanics' Institute |
| 3 | 4 | The Knockout · Levi's Stadium |
| 3 | 3 | California Academy of Sciences · Habbas Law Epicenter at PayPal Park · Colma Community Center |

**27 venues, 172 listings across the corpus, no declared route.** Add the Curran Theatre,
found 2026-10-07 and below the 3-week threshold only because it has appeared once.

**Why this is the strongest single finding in this spec.** An undeclared venue is a *silent
dependency*: the weekly run reaches it through a sweep, it works until it doesn't, and when
it stops there is no declared route to check, no `note:` recording how it was reached, and no
baseline that makes its disappearance visible. The ODC class (declared, never produced) is
2 venues. This class is 27. **Any venue the digest has listed three times is a dependency and
should be written down**, even if the entry only records which sweep found it.

Proposed as a check in its own right: *observed in ≥3 weeks with a room-like `venue_type` and
no declared source* → must be added to `config/sources.yml` or explicitly waived. Pure
text-and-JSON, no network, and it closes the loop in the direction the existing proposal
does not cover.

### 3. Correction: the Joe Henderson Lab route exists

§Q1 and §5 record that SFJAZZ's second hall has no route and recommend declaring SFJAZZ
permanently partial. **The first half is wrong.**
`jambase.com/venue/joe-henderson-lab-at-sfjazz-center` loads and carries a calendar; the
earlier test recorded it as 404.

It shows **no October dates at all**, while independent listings put the Lab's October shows
on the 17th, 24th and 25th — so the page is itself incomplete and should be treated as
partial. But for the 5–11 October window, **no source indicates any Joe Henderson Lab
concert**, which means SFJAZZ's single concert that week was probably complete.

The digest's own note had told readers to assume more was on than was listed. That hedge was
withdrawn in `66046e4`. It is worth recording as its own failure mode, because this spec
committed it while documenting it: **a route being known-partial does not license guessing in
which direction the error runs.** An unverified hedge is an unverified claim with better
manners. The `coverage: partial` declaration proposed in Addendum 1 must therefore say what
the route omits, not how much.
