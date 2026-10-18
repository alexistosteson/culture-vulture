# Spec — Readers for DNA Lounge and SFJAZZ: not built, and why

**Tier: probe.** Short-form spec and the evidence below. No plan, no audit, no
tier registry, no merge ritual owed.

**Status, 18 October 2026.** Asked for: a way the unattended weekly run can read
DNA Lounge's and SFJAZZ's calendars in full, as `scripts/dice.py` does for the
DICE venues. **Not built.** Both venues refuse automated readers on purpose, and
the only route through either is to disguise the run as a person's browser. That
is defeating the venue's refusal, not working around an outage, so it is ruled
out at any tier. What shipped instead: the evidence in `config/sources.yml`, a
rule in `prompts/weekly-research.md` that the run never reads a refusing venue by
disguise, and this record.

## Evidence — read 18 October 2026

| Venue | What the site does | Plain request | Same request calling itself Safari |
|---|---|---|---|
| DNA Lounge, `/calendar/2026/10.html` | `robots.txt` disallows the whole site (`Disallow: /`) to about 400 named agents, among them **Claude, Claude-User, Claude-Code, Anthropic, anthropic-ai and Python**. A refused request gets a page reading *403 Robots Forbidden — NO ROBOTS*. The RSS and iCal feeds on `cdn.dnalounge.com` are served under the same `robots.txt`. | 403, *NO ROBOTS* | 200, the full month (titles and ages, no times) |
| SFJAZZ, `/calendar/` | Cloudflare managed challenge (`cf-mitigated: challenge`, *Just a moment…*). The calendar page draws its listings from `/ace-api/events/` on the same host, behind the same challenge. `robots.txt` allows all agents. | 403, challenge | 403, challenge — only a real browser that runs the challenge script gets through |

So the "sorts by who is asking" framing in the old `sources.yml` note was right
about the mechanism and wrong about what it permits. DNA Lounge has named this
run and said no. SFJAZZ's robots file says yes, but its bot challenge says no to
anything that is not a person's browser, and getting past a bot challenge
unattended means a headless browser built to look like a person — the thing the
challenge exists to stop.

`dice.py` is not a precedent for either: the DICE venues publish their listings
to any browser through a widget, and nothing on their pages refuses a script.

**Does SFJAZZ publish a feed? No (checked 18 October, in a person's browser).**
The calendar and event pages offer no calendar file to subscribe to, no RSS, no
add-to-calendar link, and no event data embedded for search engines. Tickets are
sold on sfjazz.org itself, so there is no outside ticket seller to read instead.
Even its sitemap sits behind the challenge, and the sitemap address its robots
file names is a dead test server. The only channel SFJAZZ sends outward is its
email newsletter (signup hosted by WordFly).

## What the run does now

- **DNA Lounge** — reads both fallbacks (JamBase, Songkick), takes the union, and
  reports the club nights as missing every week. Unchanged in effect; the note now
  says why, so no run retries the calendar or tries another disguise.
- **SFJAZZ** — reads the Miner Auditorium mirror and the two Joe Henderson Lab
  mirrors, and reports the omission every week. Unchanged in effect.
- **Any venue** — the new prompt rule: no browser identity, borrowed headers or
  headless browser to get past a refusal, and no hunting for an unguarded copy on
  the same site.

## Routes that are open, for the owner to choose

1. **SFJAZZ's newsletter.** Already subscribed to the act-now mailbox on 18
   October (`specs/act-now-alerts.md`). Once something reads that mailbox, the
   weekly run can take SFJAZZ listings from it — both halls, as the venue chose to
   send them. A newsletter promotes what still needs selling, so it adds to the
   mirrors rather than replacing them.
2. **Ask DNA Lounge.** It lists no email newsletter. Its owner publishes a
   contact page; a short request to read the monthly calendar once a week for a
   free, linked listings digest might be granted. Only a yes from the venue
   changes this record.
3. **Accept the mirrors.** The run already does; the cost is DNA's club nights and
   SFJAZZ's second hall, named in every week's report.

## Behavioural check

`bash scripts/verify.sh` exits 0 on the branch. Nothing new runs in the gate,
because nothing new reads anything.
