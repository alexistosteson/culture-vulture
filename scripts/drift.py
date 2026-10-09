#!/usr/bin/env python3
"""
drift.py — rot checks: the ways a week goes thin without anything failing.

    python3 scripts/drift.py                    # self-test, then the newest week
    python3 scripts/drift.py --as-of 2026-09-14 # treat an earlier week as newest

validate.py checks a data file against itself. This checks the newest week
against the weeks before it, which is where rot shows: a venue spelled a new
way has split in two, and every count made of it afterwards is wrong.

Exit codes — and callers must read all three:

    0  checked, and nothing blocking was found
    1  checked, and a blocking check fired
    2  COULD NOT CHECK — no data, unreadable data, or the self-test failed.
       This is a failure, not a skip. A detector's failure mode is silence:
       a check that has gone blind prints nothing, and nothing looks exactly
       like a healthy week. So the script proves it can still see before it
       reports that it saw nothing.

The self-test replays cases whose answers are already known — planted ones, and
the recorded history in KNOWN_SPLITS below, measured 8 October 2026 and written
up in specs/fallback-sourcing.md, Addendum 3. If a listed week's file is gone
or its answer has changed, that is exit 2, not a quiet pass. A fork that
replaces data/ wholesale must empty KNOWN_SPLITS; the planted cases still run.

The decisions behind every threshold here are the owner's and are recorded in
that addendum. specs/rot-checks-build.md is the build record.
"""
import argparse
import collections
import datetime
import json
import re
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


# --- self-test --------------------------------------------------------------

# Recorded history, by the week in which the second spelling arrived. Every
# other week from the second onward must replay to nothing.
KNOWN_SPLITS = {
    "2026-08-31": [("regency ballroom", "San Francisco", "The Regency Ballroom")],
    "2026-09-14": [("4 star theater", "San Francisco", "4-Star Theater"),
                   ("montgomery theater", "San Jose", "Montgomery Theater")],
}
KNOWN_THROUGH = "2026-10-05"


def _week(name, *venues):
    return (name, [{"venue": v, "city": c} for v, c in venues])


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

    # Recorded history.
    names = [w for w, _ in weeks]
    for week in sorted(KNOWN_SPLITS):
        if week not in names:
            raise CannotCheck(f"self-test needs data/{week}.json, which is gone")
    # Not the newest week: that one is the subject of the real check, and a
    # split in it must come out as a finding (exit 1), not as a broken
    # self-test (exit 2). It joins the replay once a later week exists.
    for week in names[1:-1]:
        if week > KNOWN_THROUGH:
            break
        expect(f"recorded history, week of {week}",
               _split_keys(as_of(weeks, week)), sorted(KNOWN_SPLITS.get(week, [])))
    return len(cases)


# --- report -----------------------------------------------------------------

def report(weeks):
    """Print every check with what it was counted over. Returns blocking findings."""
    names = [w for w, _ in weeks]
    total = sum(len(evs) for _, evs in weeks)
    print(f"weeks read: {len(weeks)} ({names[0]} … {names[-1]}), {total} listings; "
          f"newest {names[-1]}: {len(weeks[-1][1])} listings")

    splits, s = spelling_splits(weeks)
    print(f"check 1 · spelling: {s['venues']} venues in {s['newest']} compared with "
          f"{s['earlier_venues']} venues from {s['earlier_weeks']} earlier week(s), "
          f"{s['overlap']} in common — {len(splits)} new spelling(s)")
    for f in splits:
        print(f"  BLOCK  “{f['new']}” ({f['key'][1]}, {f['listings']} listing(s)) is a new "
              f"spelling of “{f['established']}”. Use the established spelling.")
    return len(splits)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--as-of", metavar="YYYY-MM-DD",
                    help="treat this week as the newest and ignore later ones")
    ap.add_argument("--data", default=str(ROOT / "data"), help=argparse.SUPPRESS)
    args = ap.parse_args(argv)

    try:
        weeks = load_weeks(args.data)
        n = selftest(weeks)
        print(f"self-test: {n}/{n} known cases reproduced")
        blocking = report(as_of(weeks, args.as_of) if args.as_of else weeks)
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
