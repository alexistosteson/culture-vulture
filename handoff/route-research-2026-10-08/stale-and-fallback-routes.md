# Route research, 8 October 2026

Read-only research. Two fetch paths were used and they disagree in places: `curl -A "Mozilla/5.0"` from this Mac, and the WebFetch tool (which returns a model summary, not raw HTML). Where a size is given it is curl's `size_download`. Where only WebFetch could read a page, that is stated. "Truncation" below means the ~100 KB limit in the brief: where the first dated event sits after byte 100,000 of the raw HTML, a truncating fetcher sees no events.

Two cross-cutting findings:

- JamBase 403s `curl` (a "Security Verification" bot challenge, ~18 KB) but WebFetch reads it. Whether the project's fetcher behaves like curl or like WebFetch is not known from here; test one JamBase URL with the real fetcher before trusting any JamBase row.
- Truncation, not dead sites, is the likeliest reason several venues look empty. Items 4, 10 (Felton, Sweetwater), 6 and the Smuin calendar all have their dated content past byte 100,000.

---

ITEM: 1 SFJAZZ (Miner Auditorium)
STATUS: partial (JamBase reads via WebFetch only; curl is bot-challenged; sfjazz.org still blocked)
URL: https://www.jambase.com/venue/miner-auditorium-sfjazz-center
FOUND VIA: already written in sources.yml
HTTP / SIZE: curl 403, 18,217 bytes (bot-challenge page "Security Verification"). WebFetch read it normally; raw size not measurable.
PROOF: "Miner Auditorium @ SFJAZZ Center, San Francisco, CA". Fri Oct 9, 2026 Kurt Elling; Thu Oct 15, 2026 Lila Downs; Fri Oct 30, 2026 John Scofield.
ALSO TRIED: https://www.sfjazz.org/ , /calendar/ , /calendar , /about — all 403 (Cloudflare "Just a moment", ~5.4 KB). Only https://www.sfjazz.org/robots.txt returns 200 (97 bytes, no events). So yes, sfjazz.org still 403s on every content path tried.
NOTE: Joe Henderson Lab (second hall):
  URL: https://www.jambase.com/venue/joe-henderson-lab-at-sfjazz-center
  FOUND VIA: web search result (query "jambase.com venue Joe Henderson Lab SFJAZZ Center upcoming concerts"); the same URL then fetched directly.
  HTTP / SIZE: curl 403, 18,229 bytes (same challenge); WebFetch read it.
  PROOF: "Joe Henderson Lab at SFJAZZ Center, San Francisco, CA". Fri Nov 13, 2026 Holly Bowling (7:00 pm and 8:30 pm); Sat Nov 14, 2026 Holly Bowling (7:00 pm and 8:30 pm); Sun Nov 15, 2026 Holly Bowling (6:00 pm and 7:30 pm).
  Gap: JamBase shows only the Holly Bowling run for the Lab. Songkick (https://www.songkick.com/venues/2588888-joe-henderson-lab-sfjazz-center, found by web search; WebFetch read it, curl got 406) showed different Lab dates: Fri 06 Nov 2026 Ben Wolfe; Sat 07 Nov and Sun 08 Nov 2026 Tamir Hendelman and Tierney Sutton. So the Lab is undercounted on JamBase.
  Nothing for the Lab before 6 Nov on either site. The Miner page shows no Lab listings. Add the Lab URL as a second SFJAZZ row.

---

ITEM: 2 ODC Theater
STATUS: works
URL: https://odc.dance/calendar
FOUND VIA: already written in the brief (odc.dance/calendar); page title "ODC Performance & Event Calendar"; also linked from the ODC Theater menu as "Full Performance Calendar"
HTTP / SIZE: 200, 58,212 bytes (under 100 KB)
PROOF: ODC Theater, address block shows San Francisco, CA 94110. Fri 10/16 7:30PM "Printz Dance Project Presents: Six Degrees of PDP"; Thu 10/29 7:00PM "ODC/Dance presents: Unplugged"; Sat 11/28 11:00AM "ODC/Dance presents: The Velveteen Rabbit".
ALSO TRIED: https://odc.dance/performances — 404, 21,743 bytes (confirmed).
NOTE: The page mixes in rentals and school events (e.g. Fri 10/2 Kadampa Meditation Center, ODC School workshops). Tabs "All / Performances / Special Events / Free" are client-side filters; the raw page carries all of them. Dates carry no year in the list view; the month grid says "October 2026".

---

ITEM: 3 Smuin Contemporary Ballet
STATUS: works (per-production pages); the obvious calendar page is truncated
URL: https://www.smuinballet.org/events/french-kiss/ (current run). For later runs use the production page linked from the homepage, e.g. https://www.smuinballet.org/events/christmas-ballet-2026/ and https://www.smuinballet.org/events/after-hours/
FOUND VIA: links on the fetched homepage https://www.smuinballet.org/ (a "performing-now" page, /calendar/, and three /events/ pages are all linked there)
HTTP / SIZE: /events/french-kiss/ 200, 223,360 bytes, but the dated performance rows start at byte ~8,700 so they are inside the 100 KB window. /events/after-hours/ 200, 199,799 bytes, first Cowell row at byte ~8,600. /events/christmas-ballet-2026/ 200, 251,013 bytes (run summary lines near the top; the day grid starts ~byte 150,000 and would be cut).
PROOF: "Cowell Theater - Fort Mason Center for Arts & Culture, 2 Marina Blvd, San Francisco, CA". French Kiss: Fri Oct 9 7:30pm; Sat Oct 10 7:30pm; Thu Oct 15 7:30pm; Fri Oct 16 7:30pm (ASL); Sat Oct 17 2:00pm (audio described); Sun Oct 18 2:00pm. Run summary: Sept 11-13 Mountain View, Sept 18-19 Walnut Creek, Oct 9-18 San Francisco. Christmas Ballet: Nov 21-Dec 24 2026; page lists Walnut Creek's Lesher Center Nov 21-22 and Mountain View Dec 3-6 and San Francisco Dec 10-24.
ALSO TRIED:
  https://www.smuinballet.org/calendar/ — 200, 274,436 bytes; first performance row at byte ~134,000, so a truncating fetcher sees only the filter menu and no performances. Also mixes in children's classes at "Smuin Center for Dance, San Francisco".
  https://www.smuinballet.org/performing-now/ — 200, 199,130 bytes; run date ranges ("French Kiss September 11 - October 18, 2026", "After Hours October 17, 2026", "The Christmas Ballet November 21 - December 24, 2026", "LGBTQ+ Night! December 22, 2026") sit at bytes ~98,000-104,000, right on the truncation line. No venues or times.
  https://www.smuinballet.org/ — 200, 319,182 bytes; same run ranges at ~101,000-102,000, just past the line.
NOTE: Smuin plays three cities (Mountain View, Walnut Creek, San Francisco at Cowell Theater, Fort Mason). A fetcher must keep the venue field and drop non-Bay-Area-core rows by brief rules. The Cowell Theater performances show up here, not on Fort Mason's own site (see item 5). The event-page slugs change each production, so a fixed URL cannot cover the season; the homepage links must be followed.

---

ITEM: 4 A.C.T. (American Conservatory Theater)
STATUS: partial (run dates readable but beyond the truncation line; per-date curtain times not available)
URL: https://www.act-sf.org/whats-on/2026-27-season
FOUND VIA: link on the fetched homepage https://www.act-sf.org/
HTTP / SIZE: 200, 199,622 bytes. The six run dates start at byte ~191,700, so a truncating fetcher sees none of them. Homepage: 200, 236,664 bytes, dates at ~220,000. /whats-on: 200, 210,923 bytes, dates at ~191,700. Production page /whats-on/2026-27-season/john-proctor-is-the-villain: 200, 227,098 bytes, run line at ~195,400.
PROOF (full fetch, not truncated): "American Conservatory Theater"; venues The Toni Rembe Theater, 415 Geary Street, San Francisco CA 94102 and The Strand Theater, 1127 Market Street, San Francisco CA 94103. Runs: Alfred Hitchcock's North by Northwest SEP 22-OCT 18, 2026; Oh, Mary! OCT 13-NOV 1, 2026; John Proctor Is the Villain NOV 12-DEC 6, 2026 (Toni Rembe Theater); The Bad News Bears: A Musical FEB 26-APR 4, 2027; The Comeuppance APR 20-MAY 16, 2027; Iraq, But Funny MAY 13-JUN 13, 2027.
ALSO TRIED:
  Per-date curtain times: none on the production page. It carries run range, venue, running time (1 h 45 min, no intermission) and a list of free InterACT events with times (e.g. "Thu, Nov 12 at 7:30pm" Teacher Preview). Those are side events, not the performance schedule. The "Get Tickets" button goes to secure.act-sf.org, which renders only a login-linked shell (200, 215,316 bytes, no events).
  /sitemap.xml — 404.
NOTE: A truncating fetcher will read this site as "no shows". If the fetcher cannot read past 100 KB, treat the six run ranges above as the season, entered by hand, and refresh the list each September. Limited engagements (e.g. /whats-on/limited-engagements/every-saturday-night, /the-big-picture) are linked from the homepage and were not fetched.

---

ITEM: 5 Fort Mason Center
STATUS: partial (no single page with Cowell Theater performances)
URL: https://fortmason.org/events/
FOUND VIA: already known to the brief; confirmed by WebFetch. Links on it: /events/list/, /events/month/, /events/category/theater/
HTTP / SIZE: curl 403, 5,518 bytes (Cloudflare "Attention Required") on /calendar/ and /events/. WebFetch read /events/ and /events/list/ and /tag/performance/. So the read depends on the fetcher, as with JamBase.
PROOF: "Fort Mason Center for Arts & Culture" San Francisco. /events/ lists, with no times, "Haines Gallery: 250 Years, Indigenous Futures: Through November 7", "FOR-SITE ... At The Guardhouse: Attentive Earth: Through January 24, 2027", "Points Of Departure Fall 2026: October 13 and November 12". Header reads "Events from October 9 - October 11".
ALSO TRIED:
  https://fortmason.org/calendar/ — WebFetch: navigation only, no events. Curl 403.
  https://fortmason.org/events/category/theater/ — WebFetch: "There were no results found." (empty even though Smuin performs at Cowell).
  https://fortmason.org/tag/performance/ — found as a search result. WebFetch read it: 220,233 characters, and events run from July 2026 so the page opens with past events; the first 100,000 characters include "October 13, 2026, 7:00-8:30 pm, Fort Mason Art Points Of Departure Fall 2026 (Program 2: CIRCUS BY THE BAY), Cowell Theater, Pier 2/Gateway Pavilion", Nov 12 Program 3 at the Bayfront Theatre, and Sept 10-27 "African Stew" at Magic Theatre. This is the only Fort Mason page seen that names a Cowell performance, and it is mostly stale and long.
NOTE: Cowell Theater's programme comes from the renters, not Fort Mason: Smuin plays Cowell Oct 9-18 and in December (item 3). Magic Theatre and Bayfront Theatre events appear on Fort Mason pages. The best readable route for Cowell is the renters' own pages. A search result also showed https://san-francisco.events/venue/cowell-theater-at-fort-mason-center-for-arts-and-culture/ with one event dated July 24, 2027; it is not a usable calendar and was not fetched.

---

ITEM: 6 SF Chronicle Datebook
STATUS: no readable route found
URL: none to write. `https://datebook.sfchronicle.com/` is a 301 to a different host.
FOUND VIA: n/a
HTTP / SIZE: https://datebook.sfchronicle.com/ -> 301 to https://www.sfchronicle.com/entertainment/ ; curl followed it: 200, 837,037 bytes (title "Arts & Entertainment"). WebFetch refused to follow the cross-host redirect, and the project note on The Foundry says the project fetcher does not follow cross-host redirects, so the fetcher gets nothing from the current entry. https://datebook.sfchronicle.com/music — 410, 282 bytes (confirmed).
PROOF: none accepted. The pages below read under curl but their dated content is past the truncation line or blocked.
ALSO TRIED:
  https://www.sfchronicle.com/datebook-picks/ ("Critics' picks for best upcoming arts and entertainment events in the Bay Area") — found as a link on the fetched root. Curl 200, 670,695 bytes; dated captions ("Saturday, Oct. 17 ... Market Street Arts and Theater Festival", "T-Pain ... Golden Gate Park on Saturday, Oct. 17") first appear at byte ~201,000. WebFetch of the same URL returned a "Client Challenge" page with no events.
  https://www.sfchronicle.com/entertainment/events/ ("Events Calendar") — curl 200, 549,432 bytes, same Oct. 17 captions at ~203,000 and content in embedded JSON, not readable text.
  https://www.sfchronicle.com/entertainment/music/ — curl 200, 785,622 bytes, not examined further.
NOTE: Pages are 0.5-0.8 MB with the listings content after byte 200,000 and a bot challenge on the WebFetch path. Dropping Datebook from the fetch list and keeping it only as a manual source is the honest position.

---

ITEM: 7 Thee Stork Club (Oakland)
STATUS: works (own calendar); JamBase is the one that is blocked for curl
URL: https://theestorkclub.com/calendar/
FOUND VIA: already in sources.yml
HTTP / SIZE: 200, 157,714 bytes. First event at byte ~34,000; "Thu Oct 15" at ~53,300. About 54 events in total, so roughly the first third of the month list fits in 100 KB; later events would be cut.
PROOF: page title "Calendar - Thee Stork Club", venue lines "at Thee Stork Club" and Oakland event names in the text. Thu Oct 8, 8:00PM "somesurprises, Ilyas Ahmed, Chuck Johnson"; Fri Oct 9, 8:00PM "Mala Greña, Pecado de Juana, DJ La Femme Papi"; Sun Oct 11, 9:00PM "Bussdown Baddies"; Wed Oct 14, 8:00PM "Rip Room, Quattracenta, Fog Lamp".
ALSO TRIED: https://www.jambase.com/venue/thee-stork-club — curl 403 (bot challenge, 18,151 bytes); WebFetch read it: "Thee Stork Club, Oakland, CA": Thu Oct 8, 2026 somesurprises; Fri Oct 9, 2026 El Pecado de Juana; Wed Oct 14, 2026 Rip Room; Thu Oct 15, 2026 Copeathetic; Sun Oct 18, 2026 Jesse Detor.
NOTE: The note in sources.yml ("/calendar/ renders client-side and fetches empty") is out of date: the events are in the raw HTML. The JamBase page has slightly mangled titles ("Copeathetic" vs "Copathetic"), so prefer the venue's own page.

---

ITEM: 8 Z Space (San Francisco)
STATUS: partial (no central calendar; one production readable)
URL: https://www.zspace.org/wordforword
FOUND VIA: link on the fetched homepage https://www.zspace.org/ (menu "WORD FOR WORD")
HTTP / SIZE: 200, 189,893 bytes; the "Up Next" block is at byte ~71,900 (inside the 100 KB window). Homepage 200, 183,434 bytes.
PROOF: "Z Space" with "PHYSICAL: 450 Florida St., San Francisco, CA 94110". "Up Next - Assimilation - Stories by E.L. Doctorow & Tatyana Tolstaya - Directed by Rotimi Agbabiaka - Oct 14 - Nov 8, 2026 - in Z Below". Run range only; no per-date rows or times.
ALSO TRIED:
  https://www.zspace.org/ — the "Coming Up at Z Space:" heading is present but the list under it is empty in the raw HTML (client-side or embed).
  https://www.zspace.org/mainstage — Steindler Stage rental page, no current productions.
  https://www.zspace.org/ticketing — 200, 128,733 bytes, a policies page (not read for events).
  Web search for Z Space Oct/Nov 2026 productions returned no other dated Z Space production beyond an Aug 19, 2026 San Francisco Mime Troupe listing on sf.funcheap.com (past).
NOTE: Only Word for Word's season is visible. Other Z Space presentations are not listed anywhere readable.

---

ITEM: 9 924 Gilman (Berkeley)
STATUS: works (ticketing page); the venue site is a landing page
URL: https://app.showslinger.com/e1/460/924-gilman/8c96699fd6
FOUND VIA: link on the fetched homepage https://924gilman.org/ (redirects to https://www.924gilman.org/), the "TICKETS" button
HTTP / SIZE: 200, 95,803 bytes (just under 100 KB)
PROOF: heading "Alternative Music Foundation (924 Gilman) - Events". Oct 9, 7:00 PM "Apricot Court, A French Project, Total Joke and Something Wicked", $5; Oct 23, 7:30 PM "Antioch Arrow, The Pine, Allure, Nuzzle", $5; Oct 24, 7:30 PM "Ho99o9 & N8NOFACE - Sincerely___ The Void", $5; 13 events through Dec 6.
ALSO TRIED:
  https://www.924gilman.org/ — 200, 466,461 bytes; shows "UPCOMING SHOWS!" and "TICKETS!" headings with no events in the raw HTML.
  https://www.924gilman.org/tickets — 200, 440,237 bytes; no events (buttons only).
NOTE: The showslinger page names "924 Gilman" but gives no city, and dates carry no year. Berkeley is only on the main site (mailing address "BERKELEY, CA"). The page also contains one stale old row ("Blind Beggar Presents: Steve McQueen Band, Sat, Mar 17") near the end; ignore rows without the Oct-Dec pattern.

---

ITEM: 10a Felton Music Hall (Felton)
STATUS: works (but the homepage URL in sources.yml shows nothing)
URL: https://feltonmusichall.com/events
FOUND VIA: link on the fetched homepage (href "/events", "EVENT CALENDAR")
HTTP / SIZE: 200, 243,666 bytes. Events are listed oldest first from 9 July 2026. First October event at byte ~164,700 and the last at ~234,900. A fetcher that stops at 100 KB reads only July-September, all past.
PROOF: "Felton Music Hall", Felton. Oct 10, 2026 8:00 PM "Damien Jurado"; Oct 12, 2026 8:00 PM "Nekrogoblikon"; Oct 23, 2026 8:00 PM "Black Flag". Also Oct 19 "She Wants Revenge", Nov 14 "Nick Shoulders", Nov 20 "An evening with Andrew McMahon and his piano". 17 events Oct 1-Nov 20.
ALSO TRIED: https://feltonmusichall.com/ (the sources.yml URL) — 200, 14,904 bytes; the "featured UPCOMING shows" block is empty in the raw HTML, so the URL as written yields zero events. The only text is a stale COVID banner.
NOTE: This explains the near-empty data: homepage empty, and /events spills 100 KB before October. The venue is open and programming a full autumn.

---

ITEM: 10b Sweetwater Music Hall (Mill Valley)
STATUS: works (but all events sit past the 100 KB line)
URL: https://sweetwatermusichall.org/events/?view=list
FOUND VIA: link on the fetched homepage (href "https://sweetwatermusichall.org/events/?view=list")
HTTP / SIZE: 200, 508,201 bytes. First event ("Oct 09, 2026") at byte ~125,400. Homepage (the sources.yml URL): 200, 249,658 bytes, first event at byte ~137,600. /events/ 200, 912,233 bytes, first event ~125,300.
PROOF: "Sweetwater Music Hall | Live Music | Mill Valley, CA", 19 Corte Madera Avenue, Mill Valley, CA 94941. Fri, Oct 09, 2026 "Zepparella" (doors 7 pm, show 8 pm); Sun, Oct 11, 2026 "Moonalice Sunday Matinee" (show 1 pm); Tue, Oct 13, 2026 "Live Dead & Brothers: An All-Star Celebration of Grateful Dead & Allman Brothers". List view carries 65 dated entries.
ALSO TRIED: none failed; the homepage read fine but shows only the next four dates.
NOTE: Cause of the near-empty data is the truncation: no event is inside the first 100 KB on any Sweetwater page. The venue is open ("booking into 2028"). A fetcher with a higher limit, or a source that carries Sweetwater events, is needed; the brief did not cover a mirror and none was searched.

---

ITEM: 10c Filoli (Woodside)
STATUS: works (venue's own site now reads; the Fever page in sources.yml is the weaker source)
URL: https://www.filoli.org/events/
FOUND VIA: curl of filoli.org linked from the Fever page text, then the "Events Calendar" page title confirmed; the URL is the sources.yml note's own domain with /events/
HTTP / SIZE: 200, 103,726 bytes (just over 100 KB; the first dated rows are at byte ~78,000 so the first page of results is inside the window). Five pages of results; only page 1 was read. https://www.filoli.org/ returns 200, 157,304 bytes. The note in sources.yml says "filoli.org 403s": that no longer holds from this Mac.
PROOF: title "Events Calendar | Filoli". Taste of Filoli Tour, Oct 10th 2026 1pm-2:30pm (also Oct 14, Oct 17 ...); Upstairs Downstairs Tour, Oct 11th 2026 11am-12:30pm; Filoli Reserve: A Legacy Wine Tasting, Oct 9th 2026 12pm-1pm (and 1:30pm, 3pm); Autumn Days at Filoli, Sep 26th - Nov 1st 2026; Nightfall, Sep 26th - Nov 1st 2026 (Halloween experience). Woodside appears on the Fever page: "Filoli is a breathtaking estate in Woodside, California ... 86 Cañada Road, Woodside" (https://feverup.com/en/san-francisco/venue/filoli-historic-house-garden: 200, 522,721 bytes, shows "9 Oct - 13 Nov, From $39.00" only).
ALSO TRIED: Fever page — a single price card with a date range; no event list. https://filoli.org/calendar/ — 404.
NOTE: Filoli is open and busy, but its calendar is tours, wine tastings and garden days with multiple dates per card ("More dates" block). Almost none of it is a performance, so a low count from this venue is plausible for editorial reasons, not a fetch failure. Date blocks are not repeated per event, so a parser has to read the "More dates" lines.

---

ITEM: 11 DNA Lounge (San Francisco)
STATUS: works
URL: https://www.dnalounge.com/calendar/2026/10.html
FOUND VIA: already in sources.yml (monthly pattern); the ICS and RSS feeds and the next-month page were found as links on that fetched page
HTTP / SIZE: 200, 18,319 bytes today. The 503s are not reproduced. Next month https://www.dnalounge.com/calendar/2026/11.html: 200, 6,559 bytes. https://www.dnalounge.com/calendar/ : 200, 4,142 bytes (year index).
PROOF: "DNA Lounge Calendar: October 2026". Fri Oct 9 "Mortified", "Last Friday Night: Y2K-2010s Throwbacks", "Club Antonio"; Sun Oct 11 "The Egyptian Lover + Love Supreme"; Thu Oct 15 "Rocky Horror Picture Show"; Oct 16 "Gorilla T" and "Light City"; Thu Oct 29 "The Crow 1994: Movie Screening + Dance Party". The page does not print "San Francisco"; the .ics header says "375 Eleventh Street, San Francisco".
ALSO TRIED:
  https://cdn.dnalounge.com/calendar/dnalounge.ics — 200, 296,471 bytes (linked from the monthly page as webcal://); larger than 100 KB, so truncated.
  https://cdn.dnalounge.com/calendar/dnalounge.rss — 200, 1,631,372 bytes.
MIRROR: https://www.jambase.com/venue/dna-lounge — found by web search; WebFetch read it: "DNA Lounge, San Francisco, CA": Thu Oct 8, 2026 Parrotfish; Sun Oct 11, 2026 Egyptian Lover; Tue Oct 13, 2026 Echos. (A search summary said the JamBase page was cached from late September; the live fetch showed current dates.) Curl 403.
MIRROR 2: https://app.songkick.com/venues/7516-dna-lounge — found by web search; WebFetch: Thu 08 Oct 2026 Parrotfish Indigo Elephant; Sun 11 Oct 2026 The Egyptian Lover and The Love Supreme; Tue 13 Oct 2026 Echos Lana Del Rabies; Fri 16 Oct 2026 GorillaT.
WHAT THE MIRRORS OMIT (compared with the venue's own October list): JamBase showed 3 events and Songkick 4, against roughly 37 listings (counted by hand) on the venue's page. Absent from both: Mortified (Oct 9), Last Friday Night, Club Antonio, Ravefurrest, Secret Psychedelica, Death Guild (Mondays), Monday Night Hubba, Hubba Hubba Revue, Rocky Horror Picture Show (Oct 15), Project X, The Crow 1994 screening, Why 2K, All Hallow's Eve. Both carry live bands and touring acts only, as expected. Both were read through WebFetch summaries, which may drop rows, so the exact omission list is a lower bound on what a mirror misses.
NOTE: Use the venue's own page; the mirrors are a fallback for live shows only.

---

ITEM: 12a Kilowatt (San Francisco)
STATUS: works through the DICE endpoint; the page itself shows no events
URL: https://www.kilowattbar.com/events (page that holds the widget). Data endpoint: https://partners-endpoint.dice.fm/api/v2/events?page[size]=24&types=linkout,event&filter[venues][]=Kilowatt
FOUND VIA: the "upcoming shows" button on the fetched homepage https://www.kilowattbar.com/ (redirects to https://kilowattbar.com/) links to /events; the widget script https://widgets.dice.fm/dice-event-list-widget.js was fetched and its code read for the endpoint and parameters
HTTP / SIZE: homepage 200, 128,570 bytes, no widget on it. /events 200, 104,264 bytes; widget config at byte ~82,400 (inside the window). The widget script: 200, 381,581 bytes. Endpoint call: 200, 76,302 bytes, 24 events.
PROOF: Raw HTML of /events has zero dated events (page title "Calendar - Kilowatt"; address "3160 16th Street, San Francisco, CA 94103"). Endpoint returned 24 events, venue "Kilowatt", city San Francisco, 3160 16th Street. Dates in the response are in UTC and must be converted to America/Los_Angeles: 2026-10-09T05:00:00Z (Oct 8, 10 pm PT) "DJ Ceejay"; 2026-10-10T02:00:00Z (Oct 9, 7 pm PT) "LottoRPG, Hazy Portraits, Misandrist and Pillowgirl"; 2026-10-10T20:00:00Z (Oct 10, 1 pm PT) "The Contraptions, Rose Lyon and Everything but the Everything".
HOW A SCRIPT READS IT: (1) GET /events and find the inline `DiceEventListWidget.create({...})` call in the HTML; it is a JSON object with fields partnerId, apiKey, venues (["Kilowatt"]), version 2. (2) The widget script sets its API base to https://partners-endpoint.dice.fm and appends /api/v2. (3) GET /api/v2/events with query `page[size]`, `types=linkout,event`, and `filter[venues][]=<value of "venues">`, and a request header `x-api-key` carrying the apiKey from step 1. (4) Response JSON has `data` (list of events with date in UTC, name, venue, timezone, url, sold_out) and `links.next` (page 2: add `page[number]=2`; the API reports the base as https://events-api.dice.fm/api/v2/events). No other credential was needed.
KEY: the key is 40 characters, sits in the inline script on /events (not the homepage). Value not recorded here.
NOTE: Fetch the key fresh from the page each run rather than storing it (it is the venue's partner key). The venue filter matches by name; all 24 events returned were Kilowatt, San Francisco.

---

ITEM: 12b The Knockout (San Francisco)
STATUS: works through the DICE endpoint; the page itself shows no current events
URL: https://theknockoutsf.com/ (homepage holds the widget; https://www.theknockoutsf.com/ redirects here). Data endpoint: https://partners-endpoint.dice.fm/api/v2/events?page[size]=24&types=linkout,event&filter[venues][]=The%20Knockout
FOUND VIA: PROCESS DEVIATION, rule 1. The Knockout has no row in sources.yml, and I fetched `https://www.theknockoutsf.com/` by guessing the domain from the venue name before searching. Afterwards a web search ("The Knockout San Francisco Mission Street bar live music calendar official site") returned a result naming "theknockoutsf.com" as the venue's website at 3223 Mission St., and the fetched page and the DICE response (3223 Mission Street, San Francisco) both match, so the provenance is now corroborated. The earlier guess was not a mirror slug, but it was a guess; say so if this goes in config.
HTTP / SIZE: 200, 240,594 bytes. The widget config sits at byte ~166,100, past the 100 KB line, so a truncating fetcher cannot even see the configuration. Endpoint call: 200, 92,156 bytes, 24 events.
PROOF: Raw HTML has only stale Squarespace sample events from September 2023 ("stufed", "COPY NITE") and a "DICE EMBED EVENTS" caption; none current. Endpoint returned 24 events, venue "The Knockout", San Francisco, 3223 Mission Street. 2026-10-10T01:00:00Z (Oct 9, 6 pm PT) "FREE STAND UP OPEN MIC COMEDY AT THE KNOCKOUT!"; 2026-10-11T00:00:00Z (Oct 10, 5 pm PT) "MATINEE SHOW : JUNKYARD CAT (HOUSTON) PLUS SPECIAL GUESTS AMERICAN WOMAN"; 2026-10-12T04:00:00Z (Oct 11, 9 pm PT) "REGGAE SUNDAY : CHAMPION REGGAE DANCE PARTY!".
HOW A SCRIPT READS IT: same four steps as Kilowatt; the widget call on this page has venues ["The Knockout"], a different partnerId, and a different apiKey (48 characters).
KEY: 48 characters, sits in the inline script on the homepage. Value not recorded here.
NOTE: The widget list is open-ended; the first page ran to Oct 24 (2026-10-25T03:00:00Z last), so a script wanting four weeks needs `page[number]=2`.

---

COUNT: 10 works (2, 3, 7, 9, 10a, 10b, 10c, 11, 12a, 12b) / 4 partial (1, 4, 5, 8) / 1 none (6). Caveats: items 1, 5, 6 and the JamBase mirrors depend on which fetcher is used (curl is bot-challenged, WebFetch is not); items 3, 4, 10a, 10b depend on the 100 KB truncation limit.
