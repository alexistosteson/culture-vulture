#!/usr/bin/env python3
"""
dice.py — read a venue's calendar when the venue's page draws it with a DICE
widget, which a plain fetch sees as an empty page.

    python3 scripts/dice.py https://www.kilowattbar.com/events
    python3 scripts/dice.py https://theknockoutsf.com/ --from 2026-10-12 --to 2026-10-18
    python3 scripts/dice.py --self-test

Kilowatt and The Knockout publish no dates in their HTML. Each page carries a
small widget configuration instead — which venue, and a key — and the visitor's
browser uses it to ask DICE for the listings. This script does what the browser
does: reads the configuration off the page, asks the same question, and prints
the answer with every time converted to the venue's own clock.

THE KEY IS THE VENUE'S, AND THIS REPOSITORY IS PUBLIC. It is read from the
venue's page on every run, held in memory for the one request, and never
printed, logged or written anywhere — not here, not in config/sources.yml, not
in a digest. Do not add an option that prints it or accepts it as an argument;
a key typed on a command line ends up in a transcript. If the venue rotates it,
the next run reads the new one and nothing here changes.

Exit 0 — the calendar was read. Zero events is a real answer and is printed as
         a zero, with what it was a zero over.
Exit 2 — could not read: the page would not load, carries no widget, or DICE
         refused. That is "unreached", never "nothing on". Report it.
Exit 3 — this machine has no timezone data, so no time could be trusted. Fix
         with `pip install tzdata` and run again. The gate reads a 3 from the
         self-test as SKIPPED, not failed.

Every line names the venue and city DICE returned. The venue filter matches by
name, so a second "Kilowatt" somewhere else would arrive looking just like the
right one — check the city before listing anything.
"""
import argparse
import datetime
import json
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

API = "https://partners-endpoint.dice.fm/api/v2/events"
PAGE_SIZE = 24
MAX_PAGES = 6          # 144 events; a neighbourhood bar books about 24 a fortnight
TIMEOUT = 30
# The venues' own sites answer a browser and refuse a bare script.
BROWSER = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
           "(KHTML, like Gecko) Version/17.5 Safari/605.1.15")


class CannotRead(Exception):
    pass


def _trust():
    # python.org's macOS build ships without a certificate bundle and fails every
    # https request until one is installed; certifi's is used when it is there.
    # Verification is never switched off.
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def get(url, headers):
    req = urllib.request.Request(url, headers={"User-Agent": BROWSER, **headers})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=_trust()) as r:
            return r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        # Only the status: the request's headers carry the key and must not be echoed.
        raise CannotRead(f"{url.split('?')[0]} answered {e.code}") from None
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        why = getattr(e, "reason", None) or type(e).__name__
        raise CannotRead(f"{url.split('?')[0]} did not answer — {why}") from None


def widget_config(html):
    """(key, [venue names]) from the page's DiceEventListWidget.create({...}) call."""
    at = html.find("DiceEventListWidget.create")
    if at < 0:
        raise CannotRead("the page carries no DICE widget — has the venue changed ticketing?")
    block = html[at:at + 4000]
    key = re.search(r"""apiKey["']?\s*:\s*["']([^"']+)["']""", block)
    venues = re.search(r"""venues["']?\s*:\s*\[([^\]]*)\]""", block)
    if not key or not venues:
        raise CannotRead("the DICE widget is on the page but its key or venue could not be read")
    names = re.findall(r"""["']([^"']+)["']""", venues.group(1))
    if not names:
        raise CannotRead("the DICE widget names no venue")
    return key.group(1), names


def local(event):
    """An event's start on the venue's own clock. DICE sends UTC."""
    when = datetime.datetime.fromisoformat(event["date"].replace("Z", "+00:00"))
    return when.astimezone(ZoneInfo(event.get("timezone") or "America/Los_Angeles"))


def row(event):
    when = local(event)
    place = event.get("venue") or "?"
    city = (event.get("location") or {}).get("city") or event.get("address") or "?"
    sold = "  SOLD OUT" if event.get("sold_out") else ""
    return when.date(), (f"{when:%a %Y-%m-%d %H:%M}  {event.get('name', '?').strip()}"
                         f"  |  {place}, {city}{sold}  |  {event.get('url', '')}")


def read_calendar(page_url, fetch=get, end=None):
    """Every upcoming event, soonest first — or only as far as `end`, if given."""
    key, names = widget_config(fetch(page_url, {}))
    events, pages = [], 0
    for number in range(1, MAX_PAGES + 1):
        query = [("page[size]", PAGE_SIZE), ("page[number]", number), ("types", "linkout,event")]
        query += [("filter[venues][]", n) for n in names]
        body = fetch(f"{API}?{urllib.parse.urlencode(query)}", {"x-api-key": key})
        try:
            doc = json.loads(body)
            batch = doc["data"]
        except (ValueError, KeyError, TypeError):
            raise CannotRead("DICE answered, but not with a list of events") from None
        pages += 1
        events += batch
        if len(batch) < PAGE_SIZE or not (doc.get("links") or {}).get("next"):
            break
        if end and batch and local(batch[-1]).date() > end:
            break
    return names, events, pages


def report(names, events, pages, start, end):
    rows = sorted(row(e) for e in events)
    kept = [text for day, text in rows if (not start or day >= start) and (not end or day <= end)]
    for text in kept:
        print(text)
    span = f"{rows[0][0]} … {rows[-1][0]}" if rows else "nothing"
    window = f" between {start or 'the start'} and {end or 'the end'}" if start or end else ""
    print(f"dice: {len(kept)} event(s){window}, of {len(rows)} read for "
          f"{', '.join(names)} over {pages} page(s) covering {span}")
    if rows and end and rows[-1][0] < end and pages == MAX_PAGES:
        print(f"dice: WARNING — stopped at {MAX_PAGES} pages before reaching {end}; "
              "the window is not fully covered")


# --- self-test ----------------------------------------------------------------
# Made-up page and made-up answer; the key is a placeholder, not anybody's.

_PAGE = """<script>DiceEventListWidget.create({"information":"simple","partnerId":"0",
"apiKey":"PLACEHOLDER-NOT-A-KEY","version":2,"venues":["Foo Bar"]});</script>"""
_ANSWER = {"data": [
    {"name": "Late Show", "date": "2026-10-10T05:00:00Z", "timezone": "America/Los_Angeles",
     "venue": "Foo Bar", "location": {"city": "San Francisco"}, "url": "https://x/1"},
    {"name": "Matinee", "date": "2026-10-10T20:00:00Z", "timezone": "America/Los_Angeles",
     "venue": "Foo Bar", "location": {"city": "San Francisco"}, "url": "https://x/2",
     "sold_out": True}],
    "links": {}}


def self_test():
    seen = []

    def fake(url, headers):
        seen.append((url, headers))
        return _PAGE if "dice.fm" not in url else json.dumps(_ANSWER)

    try:
        ZoneInfo("America/Los_Angeles")
    except ZoneInfoNotFoundError:
        print("dice self-test: NOT RUN — no timezone data here (pip install tzdata)")
        return 3
    names, events, pages = read_calendar("https://venue.example/", fake)
    days = sorted(str(row(e)[0]) for e in events)
    lines = " ".join(row(e)[1] for e in events)
    checks = {
        "the venue is read off the page": names == ["Foo Bar"],
        "the key goes in the request header": seen[1][1] == {"x-api-key": "PLACEHOLDER-NOT-A-KEY"},
        "the key is not in the address": "PLACEHOLDER" not in seen[1][0],
        "the key is not in what is printed": "PLACEHOLDER" not in lines,
        "05:00 UTC lands on the evening before": days == ["2026-10-09", "2026-10-10"],
        "a sold-out show says so": "SOLD OUT" in lines,
        "one short page ends the reading": pages == 1,
    }
    for answer, why in (("<html>no widget</html>", "a page with no widget"),
                        ("<html>", "a non-answer")):
        def bad(url, _headers, answer=answer, why=why):
            return _PAGE if "dice.fm" not in url and why == "a non-answer" else answer
        try:
            read_calendar("https://venue.example/", bad)
            checks[f"{why} is could-not-read"] = False
        except CannotRead:
            checks[f"{why} is could-not-read"] = True
    for name, passed in checks.items():
        if not passed:
            print(f"  self-test FAILED: {name}")
    print(f"dice self-test: {sum(checks.values())}/{len(checks)} cases")
    return 0 if all(checks.values()) else 2


def main():
    ap = argparse.ArgumentParser(description="Read a venue's DICE-drawn calendar.")
    ap.add_argument("page", nargs="?", help="the venue page that carries the widget")
    ap.add_argument("--from", dest="start", type=datetime.date.fromisoformat, metavar="YYYY-MM-DD")
    ap.add_argument("--to", dest="end", type=datetime.date.fromisoformat, metavar="YYYY-MM-DD")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.page:
        ap.error("give the venue page, or --self-test")
    try:
        names, events, pages = read_calendar(args.page, end=args.end)
        report(names, events, pages, args.start, args.end)
    except CannotRead as e:
        print(f"dice: COULD NOT READ — {e}")
        return 2
    except ZoneInfoNotFoundError:
        print("dice: COULD NOT READ — no timezone data on this machine, so no time "
              "can be trusted. Run `pip install tzdata` and try again.")
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
