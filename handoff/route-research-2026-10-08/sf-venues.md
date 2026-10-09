# SF venue routes, checked 8 Oct 2026

Method: every URL below was fetched with curl. "Found via" says how it surfaced. Two kinds of provenance appear:
- search = returned by a web search result.
- linked = found as an href on a page I fetched. A few site root domains (madroneartbar.com, cafedunord.com, sfopera.com, 4-star-movies.com, sfwarmemorial.org) were opened as probes because search results named them; the calendar URLs reported come from links on those pages.
- Nothing was constructed. No Songkick/JamBase/Live Nation ids were guessed.

Cross-cutting facts a fetcher must know:
- **Songkick rejects any User-Agent that starts with "Mozilla"** (HTTP 406, 0 bytes). curl/python-requests/Go UAs and no UA at all return 200. Funcheap is the opposite: "Mozilla/5.0" gets 403, no UA or a curl UA gets 200. Test the real fetcher's UA before trusting either.
- Songkick venue pages show only ~5 upcoming events. The venue page links "View all upcoming concerts" to a `/calendar` sub-page, which is the one to use. Those sub-pages run 92-210 KB, but the dated lists come early (JSON-LD starts at byte ~36 KB), so the first 100 KB still holds 20+ dated entries per venue (Midway to 31 Oct, BGCA to 17 Dec, Masonic to 14 Nov, Davies to Jun 2027, 4 Star to Feb 2027).
- Songkick is third-party and lags. It misses some shows (see Swedish American Hall). JamBase show pages return 403 to curl and search surfaced no JamBase venue pages at all, so JamBase was not usable anywhere.
- Marlon Magnée (4 Star known listing), Dhruv Sangari (Swedish American Hall known listing) and Mary, Queen of Scots (past, ended 4 Oct) were not found on any fetched page. Probably past or not yet listed. Not a sign of a wrong room: venue names and cities match.

---

VENUE: The Midway
STATUS: works
URL: https://www.songkick.com/venues/3013529-midway/calendar
FOUND VIA: linked from https://songkick.com/venues/3013529-midway (that URL came from search "The Midway San Francisco calendar upcoming events"); the page's "View all upcoming concerts" href is /venues/3013529-midway/calendar
HTTP / SIZE: 200, 175,539 bytes (over 100 KB; first 100 KB holds dated entries through 31 Oct 2026). Venue page itself: 200, 92,686 bytes. Needs a non-"Mozilla" UA.
PROOF: page shows "The Midway", "San Francisco, CA, US", "900 Marin St." Events: Fri 09 Oct 2026 Audien (and Whipped Cream); Sat 10 Oct 2026 POLO & PAN and Dabeull, and Tinlicker (the known listing); Sun 11 Oct 2026 Sandy Rivera and John Morales; Fri 23 Oct 2026 Chief Keef; Sat 24 Oct 2026 Marc Rebillet.
ALSO TRIED: https://themidwaysf.com/ (and www) - 403, 73,907 bytes, Cloudflare managed-challenge page. JamBase show pages for the Midway surfaced by search (jambase.com/show/...) - not fetched individually; the same host returned 403 on a Davies show page. axs.com/nz/venues/127188 - 403. san-francisco.events/venue/the-midway-ca/ - 200 but 224,861 bytes (not evaluated for dates).
NOTE: Songkick says 26 upcoming at the Midway. Songkick may omit shows that are not ticketed through its partners. The venue's own domain is not readable by a plain GET.

VENUE: Madrone Art Bar
STATUS: works
URL: https://madroneartbar.com/calendar/
FOUND VIA: linked from https://madroneartbar.com/ (homepage nav href="/calendar/"); the domain was named in search results for "Madrone Art Bar San Francisco Divisadero calendar events"
HTTP / SIZE: 200, 251,545 bytes (over 100 KB). It still reads under truncation: the visible month grid starts at byte ~28 KB and the JSON-LD block with all 64 events runs bytes 19.7 KB-91 KB, so it ends before the cut.
PROOF: page title "Events for October 2026 – Madrone Art Bar"; JSON-LD location "Madrone Art Bar", San Francisco. Events: 2026-10-09 Hella Cheese; 2026-10-16 Lester T. Raww – FALLING OUT: Music from Fallout; 2026-10-17 FRINGE: THE INDIE ROCK DANCE PARTY; 2026-10-21 MADRONE IS 22!; 2026-10-31 THE NO THEME SUPER SPOOKY DANCE JAM.
ALSO TRIED: https://madroneartbar.com/wp-json/tribe/events/v1/ (linked from the homepage) - 200, 28,631 bytes, only the API route index, no events; I did not construct the /events sub-route.
NOTE: WordPress "The Events Calendar" month view. Shows one month at a time (Sept 26 - Oct 31 here, because the grid pads adjacent weeks). The page links the next month as https://madroneartbar.com/calendar/2026-11/ (href on the page), so a weekly run needs this month's URL plus the next month's, built as /calendar/YYYY-MM/ from that observed pattern. I only fetched the base page, not 2026-11. Includes recurring nights (Karaoke, Motown on Mondays), so expect many low-signal rows.

VENUE: Swedish American Hall
STATUS: partial (Songkick is readable but incomplete; the complete calendar is truncated)
URL: https://www.songkick.com/venues/4543956-swedish-american-hall
FOUND VIA: search "Swedish American Hall San Francisco upcoming events calendar" (result developer.songkick.com/venues/4543956-swedish-american-hall; same id on www.songkick.com)
HTTP / SIZE: 200, 73,148 bytes (under 100 KB). Needs a non-"Mozilla" UA.
PROOF: title "Swedish American Hall San Francisco, Tickets for Concerts & Music Events 2026"; JSON-LD location "Swedish American Hall", San Francisco. Upcoming: 2026-10-19 Spencer Krug; 2026-12-08 WHY? Past rows also on page (Lenka 2026-09-02, Amelie Farren 2026-05-22).
ALSO TRIED:
- https://cafedunord.com/calendar - 200, 374,398 bytes, linked from the Swedish American Hall site. This is the building's own calendar covering both rooms, each row labelled "Cafe Du Nord" or "Swedish American Hall". It lists Allan Rayman 16 Oct 8:30 pm and Spencer Krug 19 Oct, 8:00 pm at the Hall. It cannot be read in full: rows start at byte ~81 KB, so only 4 rows (8-9 Oct) fall inside 100 KB. Also private-event rows ("Private Event") appear.
- https://www.swedishamericanhall.com/ - 200, 234 KB, wedding/rental site with no events calendar; its only event-related link is event-partners.html.
- san-francisco.events/venue/swedish-american-hall/ - 200 but 184,211 bytes.
NOTE: Songkick MISSES Allan Rayman, 16 Oct 2026 (shown on Cafe du Nord's calendar and in a search result), so treat Songkick as a floor. Songkick has a second, separate entry "Swedish American Music Hall" (venue 3960749, from search) - not fetched. The Songkick calendar sub-page link was not present on this page.

VENUE: The Knockout
STATUS: no readable route found
URL: none
FOUND VIA: n/a (own site https://theknockoutsf.com/ opened as a probe; search found only Funcheap pages)
HTTP / SIZE: 200 on every own-site page, but no usable events
PROOF: n/a
ALSO TRIED:
- https://theknockoutsf.com/ and /calendar - 200, 240,594 and 186,490 bytes. Squarespace page with a stale event list: the newest event is September 2023 (e.g. "stufed", Saturday, September 16, 2023). Venue and address (3223 Mission Street) match, but nothing is upcoming.
- https://theknockoutsf.com/calendar2 - 200, 120,926 bytes, empty shell; no event text, no iframe or embed in the HTML, so the calendar is script-loaded (the homepage block is labelled "DICE EMBED EVENTS").
- https://theknockoutsf.com/home-1 - 200, 283,436 bytes, no dated events.
- https://sf.funcheap.com/venue/the-knockout/ - 403 (with Mozilla UA; not retried without UA).
NOTE: The own site is a stale placeholder and the live calendar looks like a Dice widget loaded by JavaScript. Ticketing fallback is being handled separately, per the brief.

VENUE: 4 Star Theater
STATUS: partial (live music only on the readable route; film listings missing or truncated)
URL: https://www.songkick.com/venues/4549153-4-star-theater/calendar
FOUND VIA: linked from https://songkick.com/venues/4549153-4-star-theater ("View all upcoming concerts"), which came from search "4 Star Theater San Francisco Clement St events"
HTTP / SIZE: 200, 92,172 bytes (under 100 KB). Needs a non-"Mozilla" UA.
PROOF: JSON-LD location "4 Star Theater", San Francisco. Upcoming: 2026-10-25 Reservoir; 2026-11-04 Greenhouse; 2026-11-12 goldenstar; 2026-11-16 Elanor Moss; 2026-11-20 Babehoven.
ALSO TRIED:
- https://www.4-star-movies.com/ (named as the venue site in search results) - 200, 271,601 bytes. Server-rendered list of films AND live music with full dates (e.g. "October 8, 2026 ... LIVE MUSIC: Freight Train Lady (Record Release), Indianna Hale, Forest Floor"; "October 9, 2026 ... LIVE MUSIC: Towhead, imy3, Mox"; "October 10, 2026 ... A Chinese Ghost Story"). But the event list starts at byte ~82 KB, so a 100 KB truncation shows only 8-10 Oct. It reaches 31 Oct+ beyond the cut.
- https://www.4-star-movies.com/calendar - 200, 76,145 bytes; empty shell, events not in HTML.
- https://www.sfstation.com/four-star-theatre-the-4-star-b781 - 200, 66,698 bytes, undated listing text, no useful upcoming events found.
- ma.to/venue/4startheater - 200, 228,673 bytes; search described its listings as undated.
NOTE: The room is mostly films (CinemaSFBay) plus music. Songkick covers music only. Marlon Magnée (known listing) is on none of these pages. To cover films the fetcher would need the own homepage, and that gives only ~3 days after truncation.

VENUE: Bill Graham Civic Auditorium
STATUS: works (main hall only)
URL: https://www.songkick.com/venues/65-bill-graham-civic-auditorium/calendar
FOUND VIA: linked from https://www.songkick.com/venues/65-bill-graham-civic-auditorium (that URL came from search "Bill Graham Civic Auditorium San Francisco upcoming events")
HTTP / SIZE: 200, 139,868 bytes (over 100 KB; first 100 KB covers dated entries through 17 Dec 2026). Venue page: 200, 96,000 bytes. Needs a non-"Mozilla" UA.
PROOF: page title names "Bill Graham Civic Auditorium", San Francisco. Fri 09 Oct 2026 Holy Priest and Junkie Kid; Sat 10 Oct 2026 Bonnie Raitt and Jon Cleary (known listing); Thu 15 Oct 2026 Rawayana; Sat 24 Oct 2026 Dermot Kennedy, Jonah Kagen, and Aaron Rowe; Thu 05 Nov 2026 Moby.
ALSO TRIED: https://billgrahamcivic.com/ - 403, 4,546 bytes. https://www.stereoboard.com/venues/san-francisco/bill-graham-civic-auditorium - 200 but only a 2 KB "Are You Human?" Cloudflare Turnstile page. JamBase: search surfaced only past show pages, no venue page.
NOTE: "The Theater at Bill Graham Civic Auditorium" (the smaller room, shows like Wave To Earth, Sara Bareilles) is a separate Songkick venue, https://www.songkick.com/venues/4611767-theater-at-bill-graham-civic-auditorium (from search, not fetched). Add it if the Theater room counts.

VENUE: The Masonic
STATUS: works
URL: https://www.songkick.com/venues/5614-masonic/calendar
FOUND VIA: linked from https://songkick.com/venues/5614-masonic (from search "The Masonic San Francisco Nob Hill upcoming events")
HTTP / SIZE: 200, 210,542 bytes (over 100 KB; first 100 KB covers dated entries through 14 Nov 2026). Venue page: 200, 91,991 bytes. Needs a non-"Mozilla" UA.
PROOF: JSON-LD location "The Masonic", San Francisco. Tue 13 Oct 2026 Loathe, Fleshwater, and Prostitute; Sat 17 Oct 2026 Daniel Sloss; Thu 22 Oct 2026 Rise Against and Alkaline Trio; Fri 23 Oct 2026 Shabooze¥ and Angel White; Sat 24 Oct 2026 Jodeci. EsDeeKid (known listing) is on the venue page as 2026-10-05, already past.
ALSO TRIED: https://www.sfmasonic.com/shows (own site; found as a link on the sfmasonic.com homepage) - 200, 503,914 bytes. Lists Loathe 13 Oct, Laura Ramoso 15-16 Oct, Rise Against 22 Oct etc. with ticket links, but the first event appears at byte ~133 KB, so a 100 KB truncation sees none. Fails. The sfmasonic.com homepage is 596 KB, same problem (first event at ~114 KB). stereoboard.com masonic page - Turnstile challenge, fails.
NOTE: One Songkick row reads "Tuesday 27 October 2026 : Canceled" - the page includes cancelled shows labelled in the title. The own site is more complete (comedy, Ticketmaster links) but unreadable under the size cap.

VENUE: Davies Symphony Hall
STATUS: partial (readable, but misses most of the San Francisco Symphony's own programming)
URL: https://www.songkick.com/venues/505-davies-symphony-hall/calendar
FOUND VIA: linked from https://songkick.com/venues/505-davies-symphony-hall (from search "Davies Symphony Hall songkick venue upcoming concerts San Francisco Symphony")
HTTP / SIZE: 200, 121,885 bytes (over 100 KB; the first 100 KB covers dated entries to June 2027). Venue page: 200, 93,748 bytes. Needs a non-"Mozilla" UA.
PROOF: JSON-LD location "Davies Symphony Hall", San Francisco. Mon 12 Oct 2026 Ludovico Einaudi; Thu 15 Oct 2026 Gautier Capuçon, Lisa Batiashvili, and Jean-Yves Thibaudet; Sat 17 Oct 2026 San Francisco Symphony; Mon 19 Oct 2026 Julian Lage; Wed 02 Dec 2026 Pink Martini. Venue page also shows Lang Lang 2026-10-04 (past). Nothing is listed 5-11 Oct, consistent with the hall being dark.
ALSO TRIED:
- https://sfsymphony.org/ and https://www.sfsymphony.org/Buy-Tickets/2026-27/Avatar - both redirect to waitingroom.sfsymphony.org (~2.6 KB queue page). Fails.
- https://www.jambase.com/show/ludovico-einaudi-davies-symphony-hall-20261012 (from search) - 403. Search returned JamBase show pages for Davies but no JamBase venue page.
- https://sfwarmemorial.org/calendar/ (linked from sfwarmemorial.org) - 200, 831,512 bytes. The official all-venue calendar. Its "Up Next" container is empty in the HTML; the event data is a JSON blob starting at byte ~743 KB, rendered by JavaScript. Fails for the fetcher. The homepage (413 KB) lists a few dated events but they start at byte ~237 KB.
NOTE: Songkick shows only a few Symphony nights (17 Oct, 15 Dec with Bernadette Peters) - the regular subscription season is largely absent, so this is a floor for touring and guest acts. For the Symphony's own program, no readable route was found: the queue blocks sfsymphony.org and the War Memorial calendar needs JavaScript.

VENUE: War Memorial Opera House (San Francisco Opera)
STATUS: partial (no single readable calendar page; per-production pages work)
URL: https://www.sfopera.com/operas/manon/ (one of several; also https://www.sfopera.com/operas/the-marriage-of-figaro/)
FOUND VIA: linked from https://www.sfopera.com/operas/ (the production index) and from the sfopera.com homepage (href="/operas/manon/#performances"); sfopera.com URLs were also returned by search "San Francisco Opera 2026-27 season performance calendar War Memorial Opera House"
HTTP / SIZE: Manon: 200, 113,636 bytes; Marriage of Figaro: 200, 129,342 bytes. Both put the dated performance list at byte ~29 KB, so they survive truncation.
PROOF: Manon page lists THU, OCT 15, 2026; SUN, OCT 18, 2026; WED, OCT 21, 2026; SAT, OCT 24, 2026; TUE, OCT 27; FRI, OCT 30; SUN, NOV 1, 2026 (7:30PM for the first). Figaro page lists SAT, OCT 31, 2026; TUE, NOV 3; SAT, NOV 7; TUE, NOV 10; FRI, NOV 13, 2026 and later. The page and site name the War Memorial Opera House, 301 Van Ness Avenue, San Francisco (footer of https://www.sfopera.com/calendar/).
ALSO TRIED:
- https://www.sfopera.com/calendar/ - 200, 34,180 bytes; the page shell only, no performances (script-rendered).
- https://www.sfopera.com/buy-tickets/ - 200, 51,991 bytes; no dates.
- https://www.sfopera.com/operas/ - 200, 88,470 bytes; lists productions and only season-opening dates ("Opens October 15" Manon, "Opens October 31" Figaro, "Opens May 29, 2027" Das Rheingold, "Opens June 4, 2027" Tosca), not per-performance dates.
- https://sfwarmemorial.org/calendar/ - JavaScript, 831 KB, see Davies.
- https://www.songkick.com/venues/33203-war-memorial-opera-house - 200, 63 KB, but only three May 2026 rows (Mere Mortals), no upcoming opera or ballet. Useless.
NOTE: A weekly fetcher needs one URL per production (links on /operas/ and the homepage); other linked event pages are /seasons/fall-concert/, /seasons/opera-ball/, /seasons/pride-concert-2027/ (not fetched). Mary, Queen of Scots (20 Sep - 4 Oct) is over, so its page is not needed. Remaining 2026-27 season from the page and press search: Manon 15 Oct - 1 Nov, The Marriage of Figaro from 31 Oct, Das Rheingold from 29 May 2027, Tosca 4 Jun - 2 Jul 2027.
SF BALLET IS NOT COVERED by sfopera.com: the company runs a separate site (https://sfballet.org/ returned 200, 369,680 bytes; I did not evaluate it). Search results (third-party, sfciviccenter.org) put the Ballet at the Opera House: Nutcracker 4-27 Dec 2026, Sleeping Beauty 29 Jan - 7 Feb 2027, Jewels 27 Feb - 7 Mar, etc. A Ballet route would be a separate item.

VENUE: San Francisco Neo-Futurists
STATUS: works (via an aggregator; the company's own site could not be reached)
URL: https://sf.funcheap.com/event-series/sf-neofuturists-presents-infinite-wrench-30-plays-60-minutes/
FOUND VIA: linked from the Funcheap event page https://sf.funcheap.com/sf-neo-futurists-the-infinite-wrench-30-plays-in-60-minutes-every-fri-sat-75/ (that page came from search "San Francisco Neo-Futurists calendar upcoming shows Infinite Wrench")
HTTP / SIZE: 200, 183,719 bytes (over 100 KB). Event rows begin at byte ~81 KB, and the first 100 KB still contains Oct 9, 10, 16, 17, 23, 24, 30 and 31. Works only with no UA or a curl-style UA; "Mozilla/5.0" gets 403.
PROOF: page names "SF Neo-Futurists 'The Infinite Wrench' (30 Plays in 60 Minutes, every Fri & Sat)", 447 Minna St., SF, "San Francisco Neo-Futurists". Rows: Friday, October 9 - 9:00 pm, $18.60, 447 Minna St.; Saturday, October 10 - 9:00 pm; Friday, October 16; Saturday, October 17.
ALSO TRIED: https://www.sfneofuturists.com/tickets (from search) and https://sfneofuturists.com/ - connection timeout (curl 000 after 30 s; the host resolves to 66.81.203.198) and WebFetch got "connection refused" on the same IP. Could not be evaluated from this network; it might work elsewhere. A non-Funcheap-per-event route was not found. Funcheap venue page for the Knockout shows the same 403-with-Mozilla behaviour.
NOTE: Show is "Fridays & Saturdays | 9p". Funcheap's rows are per-night, listed in date order, but the page is ads-heavy so the useful rows start late in the file. If the own site is reachable from the production fetcher, prefer https://www.sfneofuturists.com/tickets (search result) and fall back to this.

---
Count: 5 works (Midway, Madrone, Bill Graham, Masonic, Neo-Futurists) / 4 partial (Swedish American Hall, 4 Star, Davies, Opera House) / 1 none (Knockout)
