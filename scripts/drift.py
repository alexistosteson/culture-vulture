#!/usr/bin/env python3
"""
drift.py — rot checks: the ways a week goes thin without anything failing.

    python3 scripts/drift.py                    # self-test, then the newest week
    python3 scripts/drift.py --as-of 2026-09-14 # treat an earlier week as newest

validate.py checks a data file against itself. This checks the newest week
against the weeks before it and against config/sources.yml, which is where rot
shows. Four checks; two can stop a week, two only report:

    1  spelling split          a venue spelled a new way          BLOCKS
    2  thin venue              far below its own recent normal    BLOCKS until the
                               digest's "Thin this week" section accounts for it
    3  declared, not producing a tier-1 venue gone quiet          WARN
    4  observed, not declared  a relied-on room never written down WARN

Exit codes — and callers must read all three:

    0  checked, and nothing blocking was found (WARN lines may have printed)
    1  checked, and a blocking check fired
    2  COULD NOT CHECK — no data, unreadable data or config, or the self-test
       failed. This is a failure, not a skip. A detector's failure mode is
       silence: a check that has gone blind prints nothing, and nothing looks
       exactly like a healthy week. So the script proves it can still see
       before it reports that it saw nothing.

A check that needs more history than exists is neither: it prints a WARN line
saying it was not evaluated, with the weeks it had and the weeks it needs.

The self-test replays cases whose answers are already known — planted ones, and
the recorded history in KNOWN_SPLITS and KNOWN_THIN below, measured 8 October
2026 and written up in specs/fallback-sourcing.md, Addendum 3. If a listed
week's file is gone or its answer has changed, that is exit 2, not a quiet
pass. A fork that replaces data/ wholesale must empty both tables; the planted
cases still run.

Every threshold here is the owner's decision and is recorded in that addendum.
specs/rot-checks-build.md is the build record.
"""
import argparse
import collections
import datetime
import json
import re
import statistics
import sys
import traceback
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class CannotCheck(Exception):
    """The check could not be run. Never caught and turned into a pass."""


def canon(s):
    # Verbatim from Addendum 3. Do not reconstruct it: an earlier, unrecorded
    # version did not merge theatre/theater or hyphens, and its counts differ.
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    s = s.replace('&', ' and ').replace('theatre', 'theater')
    s = re.sub(r"[^a-z0-9 ]", ' ', s)
    s = re.sub(r'^the\s+', '', s.strip())
    return re.sub(r'\s+', ' ', s).strip()


def venue_key(event):
    # City is part of the key: Fox Theater in Oakland and Fox Theatre in
    # Redwood City are two rooms, and canon() alone calls them one.
    return (canon(event["venue"]), event["city"])


def load_weeks(data_dir):
    """Every data file, oldest first, as (window_start, events)."""
    files = sorted(Path(data_dir).glob("*.json"))
    if not files:
        raise CannotCheck(f"no data files in {data_dir}")
    weeks = []
    for f in files:
        try:
            datetime.date.fromisoformat(f.stem)
        except ValueError as e:
            raise CannotCheck(f"{f.name} is not named for a window start") from e
        try:
            doc = json.loads(f.read_text())
        except json.JSONDecodeError as e:
            raise CannotCheck(f"{f.name} is not valid JSON — {e}") from e
        events = doc.get("events") if isinstance(doc, dict) else None
        if not events:
            raise CannotCheck(f"{f.name} has no events")
        for e in events:
            if not e.get("venue") or not e.get("city"):
                raise CannotCheck(f"{f.name}: event {e.get('id', '?')} has no venue or city")
        weeks.append((f.stem, events))
    return weeks


def as_of(weeks, week):
    """The history as it stood when `week` was the newest."""
    if week not in [w for w, _ in weeks]:
        raise CannotCheck(f"no data file for the week of {week}")
    return [(w, evs) for w, evs in weeks if w <= week]


# --- check 1 · spelling splits ---------------------------------------------

def spelling_splits(weeks):
    """
    Spellings new in the newest week that collide with an earlier week's
    spelling of the same (canon(venue), city). Blocking.

    With no earlier week there is nothing to collide with, and that is a
    legitimate clean result — it is the first week of a fork — so it is
    reported as zero-over-zero, with the zero visible, not hidden.
    """
    *earlier, (newest, events) = weeks
    seen = collections.defaultdict(collections.Counter)
    for _, evs in earlier:
        for e in evs:
            seen[venue_key(e)][e["venue"]] += 1
    now = collections.defaultdict(collections.Counter)
    for e in events:
        now[venue_key(e)][e["venue"]] += 1

    findings = []
    for key in sorted(now):
        if key not in seen:
            continue
        for spelling in sorted(now[key]):
            if spelling not in seen[key]:
                findings.append({
                    "key": key,
                    "new": spelling,
                    "listings": now[key][spelling],
                    "established": seen[key].most_common(1)[0][0],
                })
    stats = {
        "newest": newest,
        "venues": len(now),
        "earlier_weeks": len(earlier),
        "earlier_venues": len(seen),
        "overlap": sum(1 for k in now if k in seen),
    }
    # Yield, not just structure: if earlier weeks exist and not one venue in
    # the newest week appears in any of them, the comparison is not finding
    # its own subject. Every real week here shares most of its venues with
    # the weeks before it.
    if earlier and len(now) >= 10 and stats["overlap"] == 0:
        raise CannotCheck(
            f"none of the {len(now)} venues in {newest} appears in any earlier week — "
            "the comparison is not matching anything, so its silence means nothing")
    return findings, stats


# --- config/sources.yml -----------------------------------------------------

def load_sources(path):
    """
    Every declared entry, as {name, kind, region, keys, season_ends}. `keys`
    is the canon() of the entry's name and of each string in its `venues:`
    list — the list exists because an entry's name is often not the venue
    string (SFJAZZ plays in "Miner Auditorium, SFJAZZ"; Music on the Square
    happens in "Courthouse Square"), and matching by name alone called those
    venues silent when they were not.
    """
    try:
        import yaml
    except ImportError as e:
        raise CannotCheck("PyYAML is not installed (pip install pyyaml)") from e
    try:
        doc = yaml.safe_load(Path(path).read_text())
    except (OSError, yaml.YAMLError) as e:
        raise CannotCheck(f"{path} cannot be read — {e}") from e
    tier1 = doc.get("tier_1_venues") if isinstance(doc, dict) else None
    if not isinstance(tier1, dict) or not any(tier1.values()):
        raise CannotCheck(f"{path} has no tier_1_venues — checks 3 and 4 have nothing to read")

    entries = []
    for region, items in tier1.items():
        for it in items or []:
            entries.append(_entry(it, "tier 1", region.replace("_", "-")))
    for it in doc.get("recurring") or []:
        entries.append(_entry(it, "recurring", None))
    for it in doc.get("observed_venues") or []:
        entries.append(_entry(it, "observed", None))
    return entries


def _entry(it, kind, region):
    if not isinstance(it, dict) or not it.get("name"):
        raise CannotCheck(f"a {kind} entry in sources.yml has no name: {it!r}")
    ends = it.get("season_ends")
    if ends is not None and not isinstance(ends, datetime.date):
        try:
            ends = datetime.date.fromisoformat(str(ends))
        except ValueError as e:
            raise CannotCheck(f"{it['name']}: season_ends is not a date — {ends!r}") from e
    names = [it["name"], *(it.get("venues") or [])]
    return {"name": it["name"], "kind": kind, "region": region,
            "keys": {canon(n) for n in names}, "season_ends": ends}


def covers(entry, event):
    # A tier-1 entry sits under a region, and the region must agree: the Fox
    # Theater entry is Oakland's and must not claim the Fox in Redwood City.
    return (canon(event["venue"]) in entry["keys"]
            and (entry["region"] is None or event.get("geo") in (None, entry["region"])))


def identity(entries):
    """event -> the thing being counted: its declaring entry, else (canon, city)."""
    def of(event):
        for entry in entries:
            if covers(entry, event):
                return ("entry", entry["name"])
        return venue_key(event)
    return of


def in_season(entry, window_start):
    return entry["season_ends"] is None or entry["season_ends"] >= window_start


# --- check 2 · thin venue ---------------------------------------------------

THIN_PRIOR_WEEKS = 4     # the newest week is compared with this many before it
THIN_RATIO = 0.40        # flagged below this share of their median
THIN_MIN_MEDIAN = 3      # a venue that usually has one or two listings is noise


def thin_venues(weeks, entries=()):
    """
    Venues whose newest-week count is below THIN_RATIO of the median of the
    prior THIN_PRIOR_WEEKS weeks, where that median is at least
    THIN_MIN_MEDIAN. Entries past their season_ends are exempt. Returns None
    for findings when there is too little history to evaluate.
    """
    stats = {"weeks": len(weeks), "needs": THIN_PRIOR_WEEKS + 1}
    if len(weeks) < THIN_PRIOR_WEEKS + 1:
        return None, stats
    window = weeks[-(THIN_PRIOR_WEEKS + 1):]
    newest = datetime.date.fromisoformat(window[-1][0])
    of = identity(entries)
    counts = collections.defaultdict(lambda: [0] * len(window))
    spellings = collections.defaultdict(set)
    for i, (_, events) in enumerate(window):
        for e in events:
            counts[of(e)][i] += 1
            spellings[of(e)].add(e["venue"])
    by_name = {e["name"]: e for e in entries}

    findings, watched, exempt = [], 0, 0
    for ident in sorted(counts, key=str):
        *prior, now = counts[ident]
        median = statistics.median(prior)
        if median < THIN_MIN_MEDIAN:
            continue
        entry = by_name.get(ident[1]) if ident[0] == "entry" else None
        if entry and not in_season(entry, newest):
            exempt += 1
            continue
        watched += 1
        if now < THIN_RATIO * median:
            label = entry["name"] if entry else sorted(spellings[ident])[0]
            names = spellings[ident] | ({entry["name"]} if entry else set())
            findings.append({"ident": ident, "label": label, "names": names,
                             "prior": prior, "now": now})
    stats.update(venues=len(counts), watched=watched, exempt=exempt)
    return findings, stats


def thin_lines(digest_path):
    """
    The items of the digest's "Thin this week" section, each as one string.
    None if the digest has no such section; the caller decides what that means.
    """
    try:
        text = Path(digest_path).read_text()
    except OSError:
        return None
    m = re.search(r"^##\s+Thin this week\s*$(.*?)(?=^##\s|\Z)", text, re.S | re.M | re.I)
    if not m:
        return None
    items, current = [], None
    for line in m.group(1).splitlines():
        if re.match(r"\s*[-*]\s+", line):
            if current:
                items.append(current)
            current = line
        elif current is not None and line.strip():
            current += " " + line.strip()
        elif current is not None:
            items.append(current)
            current = None
    if current:
        items.append(current)
    return items


def accounted_for(finding, lines):
    """
    A flagged venue is accounted for by a line that names it, says whether it
    was `reached` or `unreached`, and says something about what was checked.
    Naming the venue alone is not an account of anything.
    """
    for line in lines or ():
        text = f" {canon(line)} "
        names = [n for n in (canon(x) for x in finding["names"]) if n and f" {n} " in text]
        if not names:
            continue
        if not re.search(r"\b(un)?reached\b", text):
            continue
        rest = re.sub(r"\b(un)?reached\b", " ", text.replace(f" {max(names, key=len)} ", " "))
        if len(rest.split()) >= 4:
            return True
    return False


# --- check 3 · declared, not producing --------------------------------------

QUIET_WEEKS = 4


def quiet_tier1(weeks, entries):
    """Tier-1 entries, in season, with no listing in the last QUIET_WEEKS weeks."""
    tier1 = [e for e in entries if e["kind"] == "tier 1"]
    stats = {"weeks": len(weeks), "needs": QUIET_WEEKS, "tier1": len(tier1)}
    if len(weeks) < QUIET_WEEKS:
        return None, stats
    newest = datetime.date.fromisoformat(weeks[-1][0])
    recent = [e for _, events in weeks[-QUIET_WEEKS:] for e in events]
    everything = [e for _, events in weeks for e in events]
    findings, exempt, matched = [], 0, 0
    for entry in tier1:
        if any(covers(entry, e) for e in everything):
            matched += 1
        if not in_season(entry, newest):
            exempt += 1
        elif not any(covers(entry, e) for e in recent):
            findings.append(entry["name"])
    # Yield: if the tier-1 list matches nothing that was ever listed, the
    # matching is broken, and "every venue is quiet" is not a finding.
    if tier1 and matched == 0:
        raise CannotCheck(
            f"none of the {len(tier1)} tier-1 entries matches any venue in the data — "
            "the matching is broken, so checks 3 and 4 cannot be believed")
    stats.update(exempt=exempt, matched=matched)
    return findings, stats


# --- check 4 · observed, not declared ---------------------------------------

UNDECLARED_MIN_WEEKS = 3
OUTDOOR = {"street", "park"}


def undeclared_rooms(weeks, entries):
    """
    Venues listed in at least UNDECLARED_MIN_WEEKS weeks, more often indoors
    than out, that no sources.yml entry covers by `name` or `venues:`.
    """
    seen = collections.defaultdict(set)
    kinds = collections.defaultdict(collections.Counter)
    label = {}
    covered = set()
    for week, events in weeks:
        for e in events:
            key = venue_key(e)
            seen[key].add(week)
            kinds[key]["out" if e.get("venue_type") in OUTDOOR else "in"] += 1
            label.setdefault(key, e["venue"])
            if any(covers(entry, e) for entry in entries):
                covered.add(key)
    regular = [k for k in seen if len(seen[k]) >= UNDECLARED_MIN_WEEKS]
    rooms = [k for k in regular if kinds[k]["in"] > kinds[k]["out"]]
    findings = sorted((label[k], k[1], len(seen[k])) for k in rooms if k not in covered)
    stats = {"venues": len(seen), "regular": len(regular), "rooms": len(rooms),
             "covered": sum(1 for k in rooms if k in covered)}
    return findings, stats


# --- self-test --------------------------------------------------------------

# Recorded history, by the week in which the second spelling arrived. Every
# other week from the second onward must replay to nothing.
KNOWN_SPLITS = {
    "2026-08-31": [("regency ballroom", "San Francisco", "The Regency Ballroom")],
    "2026-09-14": [("4 star theater", "San Francisco", "4-Star Theater"),
                   ("montgomery theater", "San Jose", "Montgomery Theater")],
}
# Check 2's recorded flags, measured on bare (canon(venue), city) keys with no
# sources.yml — which is how the replay runs, so that declaring a venue later
# cannot change what history is expected to say.
KNOWN_THIN = {
    "2026-09-07": [],
    "2026-09-14": [("bampfa", "Berkeley"), ("mountain winery", "Saratoga"),
                   ("yerba buena center for the arts", "San Francisco")],
    "2026-09-21": [("castro theater", "San Francisco"), ("thee stork club", "Oakland")],
    "2026-09-28": [],
    "2026-10-05": [("dna lounge", "San Francisco"), ("regency ballroom", "San Francisco")],
}
KNOWN_THROUGH = "2026-10-05"


def _week(name, *venues):
    return (name, [{"venue": v, "city": c} for v, c in venues])


def _run(venue, counts, kind="club", geo="sf"):
    """Weeks 2026-01-05, -12, … with `counts[i]` listings at `venue` in week i."""
    start = datetime.date(2026, 1, 5)
    return [((start + datetime.timedelta(weeks=i)).isoformat(),
             [{"venue": venue, "city": "X", "venue_type": kind, "geo": geo}] * n
             + [{"venue": "Filler Hall", "city": "X", "venue_type": "club", "geo": geo}])
            for i, n in enumerate(counts)]


def _fake(name, kind="tier 1", region="sf", venues=(), season_ends=None):
    return {"name": name, "kind": kind, "region": region,
            "keys": {canon(n) for n in (name, *venues)}, "season_ends": season_ends}


def _thin(weeks, entries=()):
    return sorted(f["label"] for f in thin_venues(weeks, entries)[0])


def _split_keys(weeks):
    return sorted((f["key"][0], f["key"][1], f["new"]) for f in spelling_splits(weeks)[0])


def selftest(weeks):
    """Returns the number of known cases reproduced; raises CannotCheck on any miss."""
    cases = []

    def expect(label, got, want):
        if got != want:
            raise CannotCheck(f"self-test failed — {label}: expected {want}, got {got}. "
                              "The checks cannot be trusted until this is explained.")
        cases.append(label)

    # Planted. Each is one behaviour the check must have, including the ones
    # where the right answer is silence.
    expect("a new spelling of an earlier venue is caught",
           _split_keys([_week("a", ("Foo Hall", "X")), _week("b", ("The Foo Hall", "X"))]),
           [("foo hall", "X", "The Foo Hall")])
    expect("theatre/theater, hyphen, ampersand and accent all collide",
           _split_keys([_week("a", ("Café Rock & Roll Theatre", "X"), ("4 Star", "X")),
                        _week("b", ("Cafe Rock and Roll Theater", "X"), ("4-Star", "X"))]),
           [("4 star", "X", "4-Star"),
            ("cafe rock and roll theater", "X", "Cafe Rock and Roll Theater")])
    expect("the same name in another city is a different room",
           _split_keys([_week("a", ("Fox Theater", "Oakland")),
                        _week("b", ("Fox Theatre", "Redwood City"))]),
           [])
    expect("an established spelling is not new",
           _split_keys([_week("a", ("Foo Hall", "X")), _week("b", ("The Foo Hall", "X")),
                        _week("c", ("Foo Hall", "X"), ("The Foo Hall", "X"))]),
           [])
    expect("a venue with no history is not a split",
           _split_keys([_week("a", ("Foo Hall", "X")), _week("b", ("Bar Room", "X"))]),
           [])

    # Check 2, planted.
    expect("a venue at 2 against a median of 5.5 is thin", _thin(_run("Foo Hall", [4, 5, 6, 7, 2])),
           ["Foo Hall"])
    expect("a venue at exactly 40% of its median is not thin",
           _thin(_run("Foo Hall", [5, 5, 5, 5, 2])), [])
    expect("a venue that usually has two listings is not watched",
           _thin(_run("Foo Hall", [2, 2, 2, 2, 0])), [])
    expect("a venue that vanishes entirely is thin", _thin(_run("Foo Hall", [3, 3, 3, 3, 0])),
           ["Foo Hall"])
    expect("a venue past its season_ends is exempt",
           _thin(_run("Foo Hall", [3, 3, 3, 3, 0]),
                 [_fake("Foo Hall", season_ends=datetime.date(2026, 1, 31))]), [])
    expect("a venue still in season is not exempt",
           _thin(_run("Foo Hall", [3, 3, 3, 3, 0]),
                 [_fake("Foo Hall", season_ends=datetime.date(2026, 2, 28))]), ["Foo Hall"])
    expect("two strings declared as one venue are counted as one",
           _thin([(w, [dict(e, venue="Foo Hall, Annex") if i % 2 else e
                       for i, e in enumerate(evs)])
                  for w, evs in _run("Foo Hall", [4, 4, 4, 4, 4])],
                 [_fake("Foo Presents", venues=["Foo Hall", "Foo Hall, Annex"])]), [])
    expect("with four weeks, check 2 says it was not evaluated",
           thin_venues(_run("Foo Hall", [4, 5, 6, 2]))[0], None)

    foo = {"names": {"The Foo Hall", "Foo Presents"}}
    for label, line, want in [
        ("a line naming the venue, its status and what was checked accounts for it",
         "- **The Foo Hall** — reached; the calendar shows two dark weeks for a refit.", True),
        ("unreached counts as a status",
         "- Foo Presents: unreached, the calendar returned 503 on three attempts.", True),
        ("a line with no status does not account for it",
         "- **The Foo Hall** — the calendar shows two dark weeks for a refit.", False),
        ("a line with a status and nothing checked does not account for it",
         "- **The Foo Hall** — reached.", False),
        ("a line about another venue does not account for it",
         "- **Bar Room** — reached; the calendar shows two dark weeks for a refit.", False),
    ]:
        expect(label, accounted_for(foo, [line]), want)

    # Check 3, planted.
    quiet = _run("Foo Hall", [3, 0, 0, 0, 0])
    expect("a tier-1 venue with nothing in four weeks is quiet",
           quiet_tier1(quiet, [_fake("Foo Hall"), _fake("Filler Hall")])[0], ["Foo Hall"])
    expect("a tier-1 venue that produced under a declared venue string is not quiet",
           quiet_tier1(_run("Courthouse Sq", [1, 1, 1, 1, 1]),
                       [_fake("Music on the Sq", venues=["Courthouse Sq"])])[0], [])
    expect("a tier-1 venue past its season_ends is not quiet",
           quiet_tier1(quiet, [_fake("Foo Hall", season_ends=datetime.date(2026, 1, 9)),
                               _fake("Filler Hall")])[0], [])
    expect("an entry in another region does not claim the venue",
           quiet_tier1(_run("Foo Hall", [1, 1, 1, 1, 1]),
                       [_fake("Foo Hall", region="east-bay"), _fake("Filler Hall")])[0],
           ["Foo Hall"])

    # Check 4, planted.
    def rooms(weeks, entries=()):
        return [name for name, _, _ in undeclared_rooms(weeks, list(entries))[0]]

    expect("a room listed three weeks running and never declared is found",
           rooms(_run("Foo Hall", [1, 1, 1])), ["Filler Hall", "Foo Hall"])
    expect("a room listed in two weeks is not yet a dependency",
           rooms(_run("Foo Hall", [1, 1, 0]), [_fake("Filler Hall")]), [])
    expect("a park is not a room", rooms(_run("Foo Green", [1, 1, 1], kind="park"),
                                         [_fake("Filler Hall")]), [])
    expect("a room covered by a venues: list is declared",
           rooms(_run("Foo Hall", [1, 1, 1]),
                 [_fake("Foo Presents", venues=["Foo Hall"]), _fake("Filler Hall")]), [])
    expect("a room covered only by an observed entry is declared",
           rooms(_run("Foo Hall", [1, 1, 1]),
                 [_fake("Foo Hall", kind="observed", region=None), _fake("Filler Hall")]), [])

    # Recorded history.
    names = [w for w, _ in weeks]
    for week in sorted({*KNOWN_SPLITS, *(w for w, v in KNOWN_THIN.items() if v)}):
        if week not in names:
            raise CannotCheck(f"self-test needs data/{week}.json, which is gone")
    # Not the newest week: that one is the subject of the real check, and a
    # split in it must come out as a finding (exit 1), not as a broken
    # self-test (exit 2). It joins the replay once a later week exists.
    for week in names[1:-1]:
        if week > KNOWN_THROUGH:
            break
        expect(f"recorded spelling history, week of {week}",
               _split_keys(as_of(weeks, week)), sorted(KNOWN_SPLITS.get(week, [])))
        if week in KNOWN_THIN:
            thin = thin_venues(as_of(weeks, week))[0]
            expect(f"recorded thin-venue history, week of {week}",
                   sorted(f["ident"] for f in thin or ()), sorted(KNOWN_THIN[week]))
    return len(cases)


# --- report -----------------------------------------------------------------

def report(weeks, entries, digest_dir):
    """
    Print every check with what it was counted over. Returns the number of
    blocking findings; WARN lines are printed for the caller to count.
    """
    names = [w for w, _ in weeks]
    newest = names[-1]
    total = sum(len(evs) for _, evs in weeks)
    print(f"weeks read: {len(weeks)} ({names[0]} … {newest}), {total} listings; "
          f"newest {newest}: {len(weeks[-1][1])} listings; "
          f"sources.yml: {len(entries)} entries")
    blocking = 0

    splits, s = spelling_splits(weeks)
    print(f"check 1 · spelling: {s['venues']} venues in {s['newest']} compared with "
          f"{s['earlier_venues']} venues from {s['earlier_weeks']} earlier week(s), "
          f"{s['overlap']} in common — {len(splits)} new spelling(s)")
    for f in splits:
        blocking += 1
        print(f"  BLOCK  “{f['new']}” ({f['key'][1]}, {f['listings']} listing(s)) is a new "
              f"spelling of “{f['established']}”. Use the established spelling.")

    thin, s = thin_venues(weeks, entries)
    if thin is None:
        print(f"check 2 · thin venue: NOT EVALUATED — {s['weeks']} week(s), needs {s['needs']}")
        print(f"  WARN  check 2 was not evaluated: {s['weeks']} week(s) of data, needs {s['needs']}")
    else:
        digest = Path(digest_dir) / f"{newest}.md"
        lines = thin_lines(digest)
        open_ = [f for f in thin if not accounted_for(f, lines)]
        print(f"check 2 · thin venue: {s['watched']} of {s['venues']} venues usually have "
              f"{THIN_MIN_MEDIAN}+ listings ({s['exempt']} more out of season) — "
              f"{len(thin)} thin, {len(thin) - len(open_)} accounted for in the digest")
        for f in thin:
            was = ", ".join(str(n) for n in f["prior"])
            if f in open_:
                blocking += 1
                why = ("has no “Thin this week” section" if lines is None
                       else "does not account for it under “Thin this week”")
                print(f"  BLOCK  {f['label']}: {f['now']} listing(s) after {was}. "
                      f"{digest.name} {why} — add a line naming the venue, saying "
                      "reached or unreached, and what was checked.")
            else:
                print(f"  ok     {f['label']}: {f['now']} listing(s) after {was} — accounted for")

    quiet, s = quiet_tier1(weeks, entries)
    if quiet is None:
        print(f"check 3 · declared, not producing: NOT EVALUATED — "
              f"{s['weeks']} week(s), needs {s['needs']}")
        print(f"  WARN  check 3 was not evaluated: {s['weeks']} week(s) of data, needs {s['needs']}")
    else:
        print(f"check 3 · declared, not producing: {s['tier1']} tier-1 entries, {s['matched']} "
              f"ever matched a listing, {s['exempt']} out of season — "
              f"{len(quiet)} with nothing in the last {QUIET_WEEKS} weeks")
        for name in quiet:
            print(f"  WARN  {name} is declared tier 1 and has produced no listing in "
                  f"{QUIET_WEEKS} weeks")

    rooms, s = undeclared_rooms(weeks, entries)
    print(f"check 4 · observed, not declared: {s['regular']} of {s['venues']} venues appear in "
          f"{UNDECLARED_MIN_WEEKS}+ weeks, {s['rooms']} of them rooms, {s['covered']} declared — "
          f"{len(rooms)} undeclared")
    for name, city, n in rooms:
        print(f"  WARN  {name} ({city}) has been listed in {n} weeks and is not in sources.yml")
    return blocking


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--as-of", metavar="YYYY-MM-DD",
                    help="treat this week as the newest and ignore later ones")
    ap.add_argument("--data", default=str(ROOT / "data"), help=argparse.SUPPRESS)
    ap.add_argument("--sources", default=str(ROOT / "config" / "sources.yml"),
                    help=argparse.SUPPRESS)
    ap.add_argument("--digests", default=str(ROOT / "digests"), help=argparse.SUPPRESS)
    args = ap.parse_args(argv)

    try:
        weeks = load_weeks(args.data)
        entries = load_sources(args.sources)
        n = selftest(weeks)
        print(f"self-test: {n}/{n} known cases reproduced")
        blocking = report(as_of(weeks, args.as_of) if args.as_of else weeks,
                          entries, args.digests)
    except CannotCheck as e:
        print(f"COULD NOT CHECK: {e}")
        return 2
    if blocking:
        print(f"drift: {blocking} blocking finding(s)")
        return 1
    print("drift: checked, nothing blocking")
    return 0


if __name__ == "__main__":
    try:
        code = main()
    except Exception:
        # A crash is not a finding. Without this it would exit 1 and read as
        # "checked and violated".
        traceback.print_exc()
        print("COULD NOT CHECK: drift.py crashed")
        code = 2
    sys.exit(code)
