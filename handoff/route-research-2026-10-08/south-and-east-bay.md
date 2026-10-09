# South and East Bay route research, 2026-10-08

Method: every URL below was fetched with `curl -sL -A "Mozilla/5.0"` and the response parsed locally. "FOUND VIA" says whether the URL came from a search result or from a link on a fetched page. Where a URL was named only inside a search answer's prose (not as a result link) that is said plainly. Byte counts are raw HTML as downloaded. The fetcher truncates at ~100 KB, so "position" notes say where in the raw bytes the dated content starts.

---

ITEM: Rooster T. Feathers, Sunnyvale
STATUS: works
URL: https://rooster-t-feathers.seatengine-sites.com/events
FOUND VIA: WebSearch "Rooster T. Feathers Sunnyvale comedy club shows calendar". The search answer text said Silicon Valley Voice links to this address; it was not itself a result link. Page then fetched directly. It also links to /calendar (200, 170,316 bytes, same data).
HTTP / SIZE: 200, 306,211 bytes (over 100 KB; see note)
PROOF: Page header "Rooster T. Feathers Comedy Club, 157 W. El Camino Real, Sunnyvale CA 94087". Dated events: "Cam Bertrand with Mike Stevens and Jide Okonkwo ... Fri, Oct 9, 2026 8:00 PM" and "Sat, Oct 10, 2026 7:00 PM"; "Joey Bragg with Terrell 'Big-T' Butler and Jide Okonkwo" Oct 11; "Jim Perry 'The Cop Comic'" Oct 15-18; "Helen Hong" Nov 5-8.
ALSO TRIED: n/a
NOTE: Over 100 KB, but each show block is ~2.4 KB (mostly repeated policy boilerplate), so the first 100,000 bytes still hold ~35 JSON-LD Event records, from Oct 8 through Dec 3, 2026 (Luke Severeid, Dec 3, is the last one under the cut; Dec 4 onward is lost). JSON-LD `startDate` is UTC: Cam Bertrand's Fri Oct 9 8 PM Pacific appears as `2026-10-10T03:00:00Z`. A fetcher that reads those strings naively will date every show one day late; use the visible "Fri, Oct 9, 2026 8:00 PM" text or convert to America/Los_Angeles. Multi-night runs show as separate Event records per show. "Guest List for:" records are duplicates; ignore. Cam Bertrand is on now, so the known listing is confirmed.

---

ITEM: San Jose Improv, San Jose
STATUS: works
URL: https://improv.com/sanjose/calendar/
FOUND VIA: WebSearch "San Jose Improv shows tickets calendar" / "improv.com San Jose Improv ... 62 S Second St" returned a 2017 City of San Jose fact sheet (sanjose.org PDF) naming www.sanjose.improv.com. That host redirected (HTTP 200 after redirect) to https://improv.com/sanjose/ . The /sanjose/calendar/ URL is linked from that page.
HTTP / SIZE: 200, 111,595 bytes (over 100 KB, but all content is under the cut)
PROOF: Page title "San Jose Improv". Dated events: "Oct 9 Fri Bingo Loco 6:45pm", "Oct 10 Sat Kira Soltanovich 7:00pm 9:30pm", "Oct 23-25 Fri-Sun Marlon Wayans 5 shows", "Oct 30 - Nov 1 Pablo Francisco", "Nov 6-7 Mark Normand", through Feb 2027 and beyond.
ALSO TRIED: https://improv.com/sanjose/ (200, 56,305 bytes) shows only the next 12 shows (to Oct 28); use the /calendar/ page for the full list. Songkick venue page 11558-san-jose-improv returns HTTP 406 to plain curl. La Mole is not in the current list (past or unscheduled).
NOTE: Event list starts at byte 35,962 and the last event link is at byte 87,707, so the whole list survives the 100 KB cut. Dates are written "Oct 17-18 Sat-Sun Dustin Nickerson 3 shows" with no year; the year must be inferred. Multi-night runs are one row. Status words appear on rows ("Buy Now", "Wait List", "Almost Sold Out").

---

ITEM: PURE Nightclub, Sunnyvale
STATUS: works
URL: https://www.purenightclub408.com/calendar
FOUND VIA: WebSearch "PURE Nightclub Sunnyvale events calendar"; the search answer said Songkick lists the venue site as purenightclub408.com (domain named in prose, not a result link). Homepage fetched; /calendar is a nav link on it.
HTTP / SIZE: 200, 33,063 bytes
PROOF: Homepage title "Pure Nightclub | Sunnyvale South Bay | 21+ only"; JSON-LD location "Pure Nightclub, 146 S Murphy Ave, Sunnyvale, CA 94086". Calendar rows: "RELOAD Fri Oct 9 10:00 pm", "Twin Diplomacy Sat Oct 10 10:00 pm", "Johnny Chay Fri Oct 16", "Krewella Sat Oct 24", "W&W Fri Dec 4", "BRYCE ALAKAI Sat Dec 19".
ALSO TRIED: homepage https://www.purenightclub408.com (200, 71,075 bytes) carries the same list with year ("Oct 9, 2026 10:00 PM") plus JSON-LD per event. Songkick PURE page returns 406 to plain curl.
NOTE: Title comes BEFORE the date in the homepage markup ("RELOAD ... Oct 9, 2026 10:00 PM"); reading date-then-title mis-pairs every row by one. The /calendar page gives "Fri Oct October 9" with weekday and no year. "Third Party" (known listing) is not in the current window of 19 shows (Oct 9 to Dec 19). Each row has a tixr.com/e/<id> ticket link.

---

ITEM: Tech CU Arena / San Jose Barracuda home schedule, San Jose
STATUS: partial (12 home games, Oct 9 to Dec 4, 2026; the arena list needs a "Load More" click for the rest, so the last home game of the season is not on the page)
URL: https://www.techcuarena.com/events
FOUND VIA: WebSearch "sanjose.events Tech CU Arena San Jose Barracuda" returned this exact URL as a result.
HTTP / SIZE: 200, 55,574 bytes
PROOF: Footer "Tech CU Arena, 1500 South 10th St, San Jose, CA 95112". Rows: "Oct 9, 2026 San Jose Barracuda vs. Tucson Roadrunners", "Oct 10, 2026 San Jose Barracuda vs. Tucson Roadrunners", "Oct 14 ... vs. Calgary Wranglers", "Nov 25 ... vs. Coachella Valley Firebirds", "Dec 4 ... vs. Texas Stars". 12 games.
ALSO TRIED:
- https://www.ticketmaster.com/san-jose-barracuda-tickets/artist/2148253?home_away=home (linked from the Buy Tickets button on sjbarracuda.com's schedule-release article). 200, 745,545 bytes. First 46 KB holds JSON-LD for 20 home games, e.g. "San Jose Barracuda vs. Tucson Roadrunners 2026-10-09T19:00:00", "vs. Chicago Wolves 2027-02-05T19:00:00"; but the visible schedule text starts at byte 148,196 (past the cut) and the JSON-LD stops at Feb 5, 2027. Local times, no timezone suffix, in the first block; a second block is UTC ("Z").
- https://sjbarracuda.com/schedule/home (linked from sjbarracuda.com nav): 200, 1,361,419 bytes. Inline base64 images push the game rows to byte ~150,000; unreadable under the cut. Times on the full-schedule page appear to be Eastern ("10/9 - 10:00 PM" for a 7 PM Pacific game).
- https://www.axs.com/venues/130939 and hellotickets.com p-5995: 403 (bot challenge). san-francisco.events/venue/tech-cu-arena/: redirects to a generic venues index, no Tech CU rows.
NOTE: Last regular-season home game: Saturday, April 10, 2027. Source: the club's schedule release (Jul 9, 2026), fetched at https://www.oursportscentral.com/services/releases/san-jose-barracuda-announce-2026-27-regular-season-schedule/n-6386004 (200, 48,097 bytes; a WebSearch result link): "The regular season concludes with a three-game homestand as the Barracuda host Coachella Valley on April 7 before closing the campaign with back-to-back games against Abbotsford on April 9 and 10." The release gives no year (2027 is implied by the 2026-27 season) and no April 10 start time. A 6:00 PM start comes from a search snippet of a resale listing and was not fetched. The same release says 36 home games, opener Oct 3, 2026. A weekly fetcher gets only the next 12 games from the arena page; use the Ticketmaster JSON-LD for ~20 games as a supplement.

---

ITEM: Solano 2 Drive-In, Concord
STATUS: no readable route found
URL: n/a
FOUND VIA: n/a
HTTP / SIZE: n/a
PROOF: n/a
ALSO TRIED:
- https://www.westwinddi.com/locations/solano (operator's own page; the host westwinddi.com was named in a search answer's prose, then found its Concord page via its nav): 200, 129,064 bytes. Showtimes are client-side templates ("{{film.Title}}", "No movies available"); no dated events in the HTML. Page does state admission: Adults $11.50, ages 5-11 $3, under 5 free, Discount Tuesdays $8.50 / $3.
- https://www.westwinddi.com/drive-in-events: 200, 88,613 bytes. Only text: "PJ Party Saturday, March 7th" (no year, already past) and "Family Fun Nights! Reduced adult and child pricing every Tuesday. Adults: $7.50 ... Kids: $2.00". No upcoming dated one-off nights.
- https://sf.funcheap.com/venue/solano-2-drive-in/ (WebSearch result): plain curl gets HTTP 403 (nginx, 146 bytes). A separate WebFetch call did read it and listed seven Tuesdays, Oct 13 to Nov 24, 2026, all titled "$6 Drive-In Movie Night in Concord & San Jose", 8:30 pm. That is the recurring discount night, not special nights, and the host blocks plain GET, so it fails the fetcher test.
- https://www.510families.com/calendar/free-drive-in-movies/ and onerichmondsf.com listing: 403 (Cloudflare). drive-ins.com Solano page: 200 but a history page with no events.
NOTE: Latest "special" night found anywhere: West Wind free movie night, April 23, 2026 (past); a search snippet mentioned a September 10, 2026 free night (not verifiable, past). Nothing dated and upcoming that a plain-GET fetcher can read. Special nights would have to come from the operator's social media or from funcheap by a route that is not plain GET.

---

ITEM: San Jose Center for the Performing Arts (Broadway San Jose is the resident presenter)
STATUS: partial (readable list covers 20 of 97 performances, Oct 9 to Nov 13, 2026; third-party aggregator, not the presenter or the venue)
URL: https://sanjose.events/venue/san-jose-center-for-the-performing-arts
FOUND VIA: WebSearch restricted to sanjose.events returned https://sanjose.events/venues/ ; that page links to this venue URL.
HTTP / SIZE: 200, 273,148 bytes (over 100 KB; the 20 rows start at byte 40,365, and 16 of them are under the cut, Oct 9 to Oct 31)
PROOF: Page title "San Jose Center For The Performing Arts Events & Tickets | San Jose"; rows show "San Jose Center For The Performing Arts • 3,036 seats, San Jose, CA". Dated events: "Oct 09 2026 7:30 PM Fri The Phantom of the Opera", "Oct 10 2026 2:00 PM Sat The Phantom of the Opera", "Oct 11 2026 6:30 PM Sun The Phantom of the Opera - Open Caption Performance", "Oct 22 2026 Hablando Huevadas", "Oct 30 2026 Bluey's Big Play", "Nov 13 2026 Jerry Seinfeld" (Nov 13 is outside the first 100 KB).
ALSO TRIED:
- https://broadwaysanjose.com (200, 179,811 bytes; domain named in a WebSearch answer's prose). Has no dated calendar; lists show titles: Phantom of the Opera, Bluey's Big Play, The Who's Tommy, The Carpenters Songbook, Hip Hop Nutcracker, A Magical Cirque Christmas, Love Actually In Concert, The Legend of Korra in Concert, The Bodyguard, Mrs. Doubtfire, Simon & Garfunkel Story, Riverdance 30, Waitress, The Notebook, Mamma Mia!, Hamilton.
- Per-show pages state run dates, e.g. https://broadwaysanjose.com/shows/phantom-of-the-opera/ (linked from the home page; 200, 127,274 bytes) says "Phantom of the Opera October 7 - 18, 2026" (at byte 91,759, just under the cut). Run ranges only, no per-performance times. The Who's Tommy page (200, 116,220 bytes) gives "November 17" as the start; its end date was not read.
- https://www.broadway.org/theatres/san-jose-center-for-the-perf-arts-san-jose: 403 (Cloudflare).
NOTE: The aggregator is a resale-ticket feed: it carries Broadway San Jose shows but also non-Broadway acts (Seinfeld, Hablando Huevadas). It shows 20 rows server-side out of "Upcoming Events: 97"; the rest load by script. For the full season, the practical route is one broadwaysanjose.com/shows/<slug>/ page per show (each linked from the home page), which gives run ranges, not performance times. Phantom ends Oct 18, 2026.

---

ITEM: Mountain View Center for the Performing Arts
STATUS: partial (aggregator shows 20 performances of one production only, Oct 13 to Oct 30, 2026; the city's own calendar is blocked)
URL: https://sanjose.events/venue/mountain-view-center-for-the-performing-arts
FOUND VIA: linked from https://sanjose.events/venues/ (itself a WebSearch result).
HTTP / SIZE: 200, 267,055 bytes (rows start at byte 40,608; 16 of 20 are under the 100 KB cut, through Oct 25)
PROOF: Title "Mountain View Center For The Performing Arts Events & Tickets | San Jose"; rows show "Mountain View, CA". Dated events: "Oct 13 2026 7:30 PM Tue Dracula - The Musical", "Oct 14 2026 7:30 PM Wed Dracula - The Musical", "Oct 17 2026 2:00 PM Sat ... Dracula - The Musical", "Oct 18 2026 6:00 PM Sun ... Dracula - The Musical".
ALSO TRIED:
- https://www.mountainview.gov/whats-happening/events (search result): 403 (442 bytes). Same for /depts/cs/mvcpa/default.asp, the Civic Center Plaza page and https://www.mvcpa.com: all 403.
NOTE: The aggregator header says "Upcoming Events: 34" but only the first 20 rows (all Dracula) are in the HTML. Other companies using the building (Peninsula Youth Theatre, Western Ballet, Upstage) do not appear. The aggregator names the show "Dracula - The Musical"; the project's known listing is TheatreWorks' Dracula. I could not confirm they are the same production from the page (a search snippet of the city calendar mentions "Dracula: A Dance Between Love and Darkness" with no year). Opening on Oct 13 matches "opened this week" only loosely. Verify title before matching.

---

ITEM: Montgomery Theater, San Jose
STATUS: partial (aggregator carries 4 performances; building's own calendar is a script-only page)
URL: https://sanjose.events/venue/montgomery-theatre-san-jose/
FOUND VIA: WebSearch restricted to sanjose.events ("San Jose events calendar Montgomery Theater Center for the Performing Arts") returned this exact URL as the top result.
HTTP / SIZE: 200, 201,418 bytes (upcoming rows start at byte ~28,000 and are under the 100 KB cut)
PROOF: Title "Montgomery Theatre - San Jose Events & Tickets | San Jose"; address "271 South Market St, San Jose, CA 95113". Dated events: "Oct 17 2026 5:30 PM Sat Candlelight: Tribute to Michael Jackson", "Oct 17 2026 7:45 PM Sat Candlelight: The Best of Hans Zimmer", "Dec 27 2026 5:30 PM Sun Candlelight: Tribute to Michael Jackson", "Dec 27 2026 7:45 PM Sun Candlelight: Tribute to Adele".
ALSO TRIED:
- https://sanjosetheaters.org/?p=38343 (search result): redirects to https://www.sanjose.org/theaters ; 200, 166,004 bytes. The show calendar is an Angular template ("{[{item.title}]}"); no event data in the HTML. (It does not 403 any more from curl, but it is empty.)
- https://www.sanjose.org/theaters/venue-gallery/montgomery-theater: 200, a photo gallery, no events. https://www.sanjose.org/theaters/events/candlelight-tribute-mana: 404 (event removed).
- https://songkick.com/venues/48359-montgomery-theatre (search result): HTTP 406 to plain GET. A search snippet of it listed "Britishmania" Oct 23-25 (8 PM Oct 23; 2 and 8 PM Oct 24; 2 and 7 PM Oct 25) and OMEGA X; neither appears on sanjose.events, and the Songkick page could not be read, so those are unverified.
NOTE: The Candlelight: Tribute to Maná (known listing) was Sep 26, 2026 and is no longer listed. The aggregator is resale-feed based, so it misses shows by local presenters (Britishmania, CMT, Lyric Theatre) that sell through other channels. Treat it as a floor, not the full calendar.

---

ITEM: de Young Museum free Saturdays
STATUS: no readable route found
URL: n/a
FOUND VIA: n/a
HTTP / SIZE: n/a
PROOF: n/a
ALSO TRIED:
- https://deyoung.famsf.org/education/free-saturdays (WebSearch result): redirects to https://www.famsf.org/events/free-saturdays-de-young ; HTTP 403, ~5.8 KB Cloudflare "Just a moment..." challenge. Also 403: famsf.org/visit/de-young, /free-saturdays, /events/free-saturdays-legion-honor, legionofhonor.famsf.org. Retried with a full Chrome user-agent and Accept headers: same 403. A separate WebFetch also got 403.
- sf.funcheap.com listings (many WebSearch results): 403 to plain curl.
- https://www.thebolditalic.com/free-de-young-museum-day-for-bay-area-residents-every-saturday-2026-03-07/ : 200, 135,624 bytes, redirects to events.thebolditalic.com, a JavaScript shell with no article text.
- onerichmondsf.com listing: 403 (Cloudflare).
NOTE: Schedule as seen only in search-answer text, NOT confirmed on any page I could fetch: free general admission to the permanent collection every Saturday for residents of Alameda, Contra Costa, Marin, Napa, San Francisco, San Mateo, Santa Clara, Solano and Sonoma counties; ID or postmarked envelope; timed tickets (listings differ on hours: 9:30-4:30 vs 9:30-5:15); special exhibitions are not free; "could be changed or canceled at any time"; no end date seen. Because the official source blocks plain GET, the weekly fetcher cannot verify this; treat it as a standing rule to be re-confirmed by a person or a browser-based tool.

---

ITEM: Legion of Honor free Saturdays
STATUS: no readable route found
URL: n/a
FOUND VIA: n/a
HTTP / SIZE: n/a
PROOF: n/a
ALSO TRIED: Same host and same result as the de Young item: famsf.org pages return 403 (Cloudflare challenge); legionofhonor.famsf.org redirects into famsf.org and is also 403; sf.funcheap.com/?p=1255106 ("Free Legion of Honor Museum Day for Bay Area Residents | Every Saturday", a WebSearch result) returns 403 to plain curl.
NOTE: Unverified, from search-answer text only: same program as the de Young (every Saturday, permanent collection, nine Bay Area counties, ID or postmarked envelope, timed tickets, listed as 9:30 am-5:15 pm). No season end date seen. The fetcher cannot confirm it.

---

ITEM: California Academy of Sciences NightLife
STATUS: works
URL: https://www.calacademy.org/nightlife
FOUND VIA: WebSearch "California Academy of Sciences NightLife Thursday 21+ schedule 2026" returned calacademy.org/nightlife as a result link (the bare host form calacademy.org/nightlife redirects here).
HTTP / SIZE: 200, 98,881 bytes (about 1.1 KB under the 100 KB cut; any growth will truncate the FAQ)
PROOF: Page text: "NightLife is Thursdays* from 6-10 p.m. Last entry into the building is 9 p.m. All guests must be 21+ with valid, physical photo ID. *Well...most Thursdays: There is usually one Thursday per month when no NightLife event is scheduled. We also hibernate for the holidays from mid-December through early-January." "Tickets are $26. If you have an EBT card, you can purchase a discounted $5 ticket at the ticket window." Planetarium passes are $7 extra. Listed upcoming events: "NightLife: Buggin' Out", "NightLife: October 15", "NightLife: Día de los Muertos", "Fright NightLife", "NightLife: Pajammy Jam", "NightLife: Naughty or Nice". Venue is California Academy of Sciences (San Francisco; city is not spelled out in the quoted text).
ALSO TRIED: calendar.calacademy.org and docent.calacademy.org were search results but I did not fetch them.
NOTE: Schedule rules sit at byte ~73,000 and the event cards at ~62,000, both under the cut. The upcoming-event cards show titles only, with no dates in the extracted text (only "October 15" is in a title); individual dates are on the card links. No season end date is stated; recurring year-round except the mid-December to early-January break. Stated price ($26) is higher than the $12 on an older fact sheet seen in search snippets; the page governs.

---

ITEM: Mechanics' Institute, San Francisco: Movies at Mechanics' (formerly CinemaLit)
STATUS: no readable route found (page is readable in a browser but every dated line sits past byte 150,000, beyond the fetcher's cut)
URL: n/a (best page, not usable under the cut: https://www.milibrary.org/cultural-programs/movies)
FOUND VIA: WebSearch "Mechanics' Institute San Francisco Movies at Mechanics' CinemaLit film night schedule" returned this URL as a result link.
HTTP / SIZE: 200, 223,635 bytes; "My Man Godfrey" first appears at byte 158,565, "Remember the Night" later.
PROOF (if read in full): Page says "Movies at Mechanics' has welcomed film enthusiasts for classic cinema screenings and salons on Friday evenings for over 20 years ... the first three Fridays of the month." Address "57 Post Street San Francisco, CA 94104". Rows: "Oct 9 Movies at Mechanics' Presents: My Man Godfrey (1936) October 9, 2026 6:00 PM - 8:00 PM", "Oct 16 ... It Happened One Night (1934) ... 6:00 PM - 8:00 PM", "Oct 30 Steel Magnolias: Dolly Parton Tribute Screening with Costume Contest 6:00 PM - 8:00 PM" (a fifth Friday, so the "first three Fridays" rule has exceptions), "Nov 6 Forbidden (1932)", "Nov 13 Baby Face (1933)", "Nov 20 Ladies They Talk About (1933)", "Dec 4 ... December Finale: Remember the Night (1940)".
ALSO TRIED:
- https://www.milibrary.org/events : 200, 354,560 bytes; "Godfrey" at byte 197,378.
- Single-event pages https://www.milibrary.org/events/38204 and /events/36277 (linked from the movies page): 200, ~236 KB each, text at byte ~154,800.
- https://downtownsf.org/do/movies-at-mechanics-presents (WebSearch result): 200, 33,379 bytes, but unfilled script templates ("{{event.title}}"), no events.
NOTE: Cost is not on the fetched movies page or the event page text I read. A search snippet gave $5 members / $10 non-members, 6:00 pm, unverified. No season end date; the series is shown through Dec 4, 2026. "CinemaLit" is the older name and appears only in old third-party listings (kpfa.org event, SF Examiner); the current series is "Movies at Mechanics'". All milibrary.org pages carry ~150 KB of header and script ahead of the content.

---

ITEM: Noe Valley Town Square: night market and regular events
STATUS: works
URL: https://noevalleytownsquare.com/events
FOUND VIA: Linked from https://www.sfstation.com/noe-valley-town-square-b38998308 (a WebSearch result), which names noevalleytownsquare.com; the home page then links to /events.
HTTP / SIZE: 200, 131,643 bytes (over 100 KB, but dated content sits at bytes 75,000 to 91,000, under the cut)
PROOF: Home page: "Noe Valley Town Square community events listed on this site are sponsored by the Noe Valley Association in coordination with the San Francisco Recreation and Parks Department"; address "4104 24th Street, San Francisco, CA 94114". Events page: "Free Sunday Morning Yoga ... Sundays, October 11, 25 (no yoga 10/18) ... Yoga classes will resume 4/11/27 11:00 AM - noon"; "S.T.E.A.M. in the Square ... Sunday, October 18 10:00 AM - 12:00 PM"; "Fridays at 5: Noe Music in the Square: Le Jazz Hot ... Friday, October 23 5:00 PM - 6:00 PM"; "NVTS 10th Anniversary & NVA 20th Anniversary Disco Party ... Saturday, October 24 6:30 PM - 8:30 PM"; "Noe Valley Night Market ... Tuesday, October 27 4:30 PM - 8:30 PM ... 40+ booths ... street closure".
ALSO TRIED: sf.funcheap.com/event-series/noe-valley-monthly-night-market/ and sfs-noe-valley-night-market-2026/ : 403 to plain curl. https://www.heylo.com/event/-ODc5gJI_UUnCyp02Y7f (200): only a past Dec 31 market and "every month with the Noe Valley Merchants Association".
NOTE: The official page states the market only as the single next date, Oct 27 at 4:30-8:30 PM, and no recurrence rule. The "last Tuesday of most months, through December 29, 5-8 PM" rule comes from funcheap search-answer text (403 to a plain fetcher), and its 5-8 PM conflicts with the official 4:30-8:30. Treat the official page as authoritative for times. Page also lists "Fridays at 5" music (weekly) and Sunday yoga (paused after Oct 25 until Apr 11, 2027). No dates are shown with a year; infer 2026.

---

ITEM: Colma Summer Concert Series, Colma Community Center (2026 dates; has the season ended)
STATUS: works
URL: https://www.colma.ca.gov/livewire-june-2026/
FOUND VIA: WebSearch restricted to colma.ca.gov ("Colma Summer Concert Series 2026 August Thursday colma.ca.gov") returned this URL as a result link. The two event pages below were also result links.
HTTP / SIZE: 200, 79,116 bytes
PROOF: Town of Colma newsletter "LiveWire June 2026": "Summer Concerts - August 13, 20 and 27". Official event pages fetched: https://www.colma.ca.gov/event/summer-concert-series-native-elements-2026/ (200, 82,136 bytes): "...1520 Hillside Blvd. from 6:00pm - 8:00pm ... August 20 - Native Elements ALL AGES FREE"; https://www.colma.ca.gov/event/summer-concert-series-smokin-slice-of-mojo-2026/ (200, 82,301 bytes): "August 27 - Smokin Slice of Mojo ALL AGES FREE".
ALSO TRIED: Aug 13 ("Carnaval 2026" per a search snippet) was not fetched on its own page; Aug 13 is confirmed only by the LiveWire line. sf.funcheap.com Colma pages: 403 to plain curl.
NOTE: The 2026 season was three Thursdays, Aug 13, 20 and 27, 6:00-8:00 PM, free, all ages, on the lawn at 1520 Hillside Blvd. It ended Aug 27, 2026; nothing remains for 2026. The Town's /events page (200, 104,891 bytes) now lists autumn events (Cinema at the Cemetery Oct 10, Candidate Forum Oct 13, Veterans Card Making Oct 14) and no concerts. The 2025 series was Aug 7, 14, 21 (a different year; do not confuse). Next season would be announced around June 2027.

---

COUNT: 6 works / 4 partial / 4 no readable route found
