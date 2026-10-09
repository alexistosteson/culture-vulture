#!/usr/bin/env bash
#
# verify.sh — the gate a week must clear before it may be merged to main.
#
#     bash scripts/verify.sh
#
# Exit 0 — every required check passed. The weekly run merges on this.
# Exit 1 — something failed. Leave the branch unmerged and escalate to a human.
#
# This exists because "I validated it" was previously a judgement call made in
# prose, and prose does not gate anything. The 2026-08-17 run published a week
# that validate.py called clean and that was nonetheless missing 23 listings
# from four tier-1 venues. validate.py checks the data file against itself; it
# cannot tell you the research was thin. So this script checks the things that
# are mechanically checkable, and the report still has to say what it could not
# reach.
#
# Two classes of check:
#   REQUIRED — pure python plus the repo. Always runs. Failure blocks the merge.
#   OPTIONAL — needs a tool that may be absent (ruff, Chromium). If the tool is
#              there the check is binding; if not, it is reported SKIPPED and
#              does not block, because CI runs the same checks on the push.
#
# A SKIPPED check is not a passed check. The summary prints them separately and
# the weekly report is expected to repeat them.
#
# A fourth word, WARN, is for a check that ran and found something worth saying
# that is not worth stopping a week for — a watched venue gone quiet, a
# relied-on venue never written down. Warnings never change the exit code. They
# are counted in the summary and listed again beneath it, and the weekly report
# is expected to repeat every one, by the same rule as SKIPPED.

set -uo pipefail
cd "$(dirname "$0")/.."

pass=0; fail=0; skip=0; warn=0; warnings=""
ok()   { echo "  PASS  $1"; pass=$((pass+1)); }
no()   { echo "  FAIL  $1"; fail=$((fail+1)); }
meh()  { echo "  SKIP  $1"; skip=$((skip+1)); }

echo "=== REQUIRED ==="

# 1. Both configs parse. A broken brief.yml silently degrades build.py to
#    "publish the data file as-is", which loses the whole geography.
if python3 -c "
import yaml
yaml.safe_load(open('config/brief.yml'))
yaml.safe_load(open('config/sources.yml'))
" 2>/dev/null; then ok "config/brief.yml and config/sources.yml parse"
else no "a config file does not parse"; fi

# 2. Schema + vocabulary + window + duplicate ids, across every data file.
if out=$(python3 scripts/validate.py 2>&1); then
  ok "validate.py — $(echo "$out" | tail -1)"
else
  no "validate.py"; echo "$out" | sed 's/^/        /'
fi

# 3. The JSON Schema itself. validate.py deliberately does not import
#    jsonschema, so nothing else covers additionalProperties or the patterns.
if python3 - <<'PY' 2>/dev/null
import json, glob, sys
try:
    import jsonschema
except ImportError:
    sys.exit(2)
schema = json.load(open("schema/events.schema.json"))
v = jsonschema.Draft202012Validator(schema)
n = sum(len(list(v.iter_errors(json.load(open(f))))) for f in glob.glob("data/*.json"))
sys.exit(1 if n else 0)
PY
then ok "jsonschema — all data files conform"
else
  [ $? -eq 2 ] && meh "jsonschema not installed (pip install jsonschema)" || no "jsonschema — a data file violates the schema"
fi

# 4. docs/events.json is what build.py would produce. CI enforces this too;
#    catching it here saves a red push.
before=$(git status --porcelain docs/events.json)
python3 scripts/build.py >/dev/null 2>&1
if [ -z "$(git diff --name-only docs/events.json)" ] || [ -n "$before" ]; then
  ok "docs/events.json is current"
else
  no "docs/events.json was stale — build.py has now refreshed it, commit the change"
fi

# 5. The digest and the data agree on what is featured. These are written
#    separately and drift silently; a reader trusts the digest's bold text.
if python3 - <<'PY'
import json, glob, re, sys, os
data = sorted(glob.glob("data/*.json"))[-1]
week = os.path.basename(data)[:-5]
md = f"digests/{week}.md"
if not os.path.exists(md):
    print(f"        no digest for {week}"); sys.exit(1)
d = json.load(open(data))
cap = 8
n_data = sum(1 for e in d["events"] if e.get("featured"))
n_md = len(re.findall(r"\*\*Featured", open(md).read()))
print(f"        {week}: data {n_data}, digest {n_md}, cap {cap}")
sys.exit(0 if n_data == n_md and n_data <= cap else 1)
PY
then ok "digest and data agree on the featured set, and it is within cap"
else no "featured set disagrees between digest and data, or exceeds cap"; fi

# 6. Every event in the newest week has a note. A listing that says nothing is
#    a database row, which is the thing this project exists not to be.
if python3 - <<'PY'
import json, glob, sys
d = json.load(open(sorted(glob.glob("data/*.json"))[-1]))
bare = [e["id"] for e in d["events"] if not e.get("note", "").strip()]
if bare:
    print("        no note:", ", ".join(bare[:8]))
sys.exit(1 if bare else 0)
PY
then ok "every listing in the newest week has a note"
else no "some listings have no note"; fi

# 7. The tool floor must be ENFORCEABLE. Pure python, so this always runs.
#    Mirrors .github/workflows/validate.yml — keep the two lists in step.
if python3 - <<'PY'
import sys, pathlib, re
REQUIRED = {"F", "ARG", "B", "RUF"}
p = pathlib.Path("ruff.toml")
if not p.exists():
    print("        ruff.toml is missing"); sys.exit(1)
raw = p.read_text()
try:
    import tomllib
    select = set(tomllib.loads(raw).get("lint", {}).get("select", []))
except ImportError:
    # Python < 3.11 has no tomllib. Fall back to reading the select list
    # directly rather than reporting a failure the week did not cause — a
    # missing stdlib module is not a narrowed floor, and silently skipping
    # would be worse than either.
    m = re.search(r"^\s*select\s*=\s*\[(.*?)\]", raw, re.S | re.M)
    select = set(re.findall(r'"([^"]+)"', m.group(1))) if m else set()
missing = sorted(REQUIRED - select)
if missing:
    print(f"        ruff.toml no longer selects: {', '.join(missing)}"); sys.exit(1)
sys.exit(0)
PY
then ok "tool floor is enforceable (ruff.toml selects F, ARG, B, RUF)"
else no "tool floor is NOT enforceable — never fix this by narrowing ruff.toml"; fi

# 8. Rot checks: the newest week against the weeks before it. drift.py has
#    THREE exits and all three are read here. Exit 2 means it could not check —
#    no data, unreadable data, or its own self-test failed — and that is a
#    failure, never a skip: a detector that has gone blind prints nothing, and
#    nothing looks like a healthy week. Its output is printed on a pass too,
#    because the counts it was made over are the proof that it looked.
#    Its "  WARN  " lines are counted whatever the exit: a week that is blocked
#    still owes its warnings to the report.
out=$(python3 scripts/drift.py 2>&1); rc=$?
case $rc in
  0) ok "drift.py — rot checks ran, nothing blocking" ;;
  1) no "drift.py — a rot check is blocking this week" ;;
  2) no "drift.py COULD NOT CHECK — a failure, not a skip" ;;
  *) no "drift.py exited $rc, which it never should — treated as could-not-check" ;;
esac
echo "$out" | sed 's/^/        /'
warnings=$(echo "$out" | grep '^  WARN  ' || true)
[ -n "$warnings" ] && warn=$(echo "$warnings" | wc -l | tr -d ' ')

echo
echo "=== OPTIONAL (binding when the tool is present) ==="

# 9. Lint.
if command -v ruff >/dev/null 2>&1; then
  if ruff check . >/dev/null 2>&1; then ok "ruff check ."
  else no "ruff check ."; ruff check . 2>&1 | sed 's/^/        /' | head -20; fi
else
  meh "ruff not installed — CI still runs it on push"
fi

# 10. The behavioural check: does the page actually render the week? index.html
#     fetches events.json at runtime, so a payload that validates can still
#     fail to display. Nothing else in this repo catches that.
CHROME=$(ls -d /opt/pw-browsers/chromium-*/chrome-linux/chrome 2>/dev/null | head -1)
[ -z "$CHROME" ] && CHROME=$(command -v chromium chromium-browser google-chrome 2>/dev/null | head -1)
if [ -n "$CHROME" ]; then
  port=$((8000 + RANDOM % 1000))
  (cd docs && python3 -m http.server "$port" >/dev/null 2>&1) &
  srv=$!; sleep 2
  dom=$(mktemp)
  "$CHROME" --headless --no-sandbox --disable-gpu --virtual-time-budget=8000 \
            --dump-dom "http://localhost:$port/index.html" >"$dom" 2>/dev/null
  kill $srv 2>/dev/null; wait $srv 2>/dev/null
  if python3 - "$dom" <<'PY'
import sys, json, glob, re, html
dom = open(sys.argv[1], encoding="utf-8", errors="replace").read()
# Assert only on RENDERED text: strip script/style, drop tags, unescape
# entities. Both are load-bearing — index.html's error strings live in an
# inline <script>, and titles containing & appear as &amp;.
body = re.sub(r"<script\b.*?</script>|<style\b.*?</style>", "", dom, flags=re.S | re.I)
text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", body)))
d = json.load(open(sorted(glob.glob("data/*.json"))[-1]))
missing = [e["title"] for e in d["events"]
           if html.unescape(e["title"]).split(",")[0][:24] not in text]
bad = [s for s in ("Could not load data", "No data") if s in text]
if missing: print(f"        {len(missing)} title(s) not rendered, e.g. {missing[:3]}")
if bad:     print(f"        page is in its error state: {bad}")
print(f"        rendered {len(d['events']) - len(missing)}/{len(d['events'])} listings")
sys.exit(1 if missing or bad else 0)
PY
  then ok "page renders every listing, no error state"
  else no "page does not render the week correctly"; fi
  rm -f "$dom"
else
  meh "no Chromium — cannot confirm the page actually renders"
fi

echo
echo "================================================================"
printf 'passed %d   failed %d   skipped %d   warnings %d\n' "$pass" "$fail" "$skip" "$warn"
if [ "$warn" -ne 0 ]; then
  echo "note: $warn warning(s) — repeat each one in the report; a warning does not block."
  echo "$warnings"
fi
if [ "$fail" -ne 0 ]; then
  echo "VERIFICATION FAILED — do not merge. Escalate with the failures above."
  exit 1
fi
[ "$skip" -ne 0 ] && echo "note: $skip check(s) skipped — say so in the report; a skip is not a pass."
echo "VERIFICATION PASSED — safe to merge."
exit 0
