#!/usr/bin/env bash
# Pre-push Tau Ceti review of a LOCAL commit: runs TauCetiReview's own engine
# (runner/review.py, current main) on HEAD of a TauCeti checkout, every rubric,
# read-only, nothing posted or archived.
# Exit: 0 every rubric approves; 1 findings; 2 setup/engine failure; 3 provider down.
#
# usage: local-review.sh <tauceti-checkout> <title-and-body-file> [rubric,list]
# env:   TAUCETI_PROVIDERS (default: claude)  e.g. claude,codex
#        TAUCETI_REVIEW_HOME (default: ~/.cache/tauceti-review-local)
set -euo pipefail
fail() { echo "local-review: $*" >&2; exit 2; }
want=0  # the only exit codes other than 2 are the deliberate ones below
trap 'rc=$?; [ -n "${w:-}" ] && rm -rf "$w"; [ $rc -eq $want ] || rc=2; exit $rc' EXIT
co=$(cd "$1" && pwd); body=$(cd "$(dirname "$2")" && pwd)/$(basename "$2"); only=${3:-}
home=${TAUCETI_REVIEW_HOME:-$HOME/.cache/tauceti-review-local}; eng=$home/TauCetiReview
up=$(git -C "$co" remote -v | awk '/TauCetiProject\/TauCeti(\.git)? \(fetch\)/{print $1; exit}')
[ -n "$up" ] || fail "no remote points at TauCetiProject/TauCeti"
[ -z "$(git -C "$co" status --porcelain --untracked-files=no)" ] || fail "commit first; the review is of HEAD"

if [ -d "$eng/.git" ]; then
  [ "$(git -C "$eng" ls-remote origin main | cut -f1)" = "$(git -C "$eng" rev-parse HEAD)" ] ||
    { git -C "$eng" fetch -q origin main && git -C "$eng" reset -q --hard origin/main; }
else mkdir -p "$home" && git clone -q https://github.com/TauCetiProject/TauCetiReview "$eng"; fi
rsha=$(git -C "$eng" rev-parse HEAD)

git -C "$co" fetch -q "$up" main
head=$(git -C "$co" rev-parse HEAD); mb=$(git -C "$co" merge-base HEAD "$up/main")
w=$(mktemp -d "${TMPDIR:-/tmp}/tauceti-local-review.XXXXXX"); mkdir "$w/code" "$w/store"
git -C "$co" archive HEAD | tar -x -C "$w/code"
git -C "$co" diff --no-color --no-ext-diff --no-textconv -M --abbrev=11 \
  --src-prefix=a/ --dst-prefix=b/ "$mb" HEAD -- > "$w/diff.txt"
git -C "$co" diff --name-only -z --no-renames "$mb" HEAD -- > "$w/paths.z"
cp "$body" "$w/pr_desc.txt"; echo '{}' > "$w/replies.json"; echo '{}' > "$w/prior.json"
git clone -q --depth 1 https://github.com/TauCetiProject/TauCetiRoadmap "$w/roadmap"
rm -rf "$w/roadmap/.git"
# reuse/naming grep Mathlib at the checkout's pinned rev (cached shallow fetch)
rev=$(python3 -c 'import json,sys;print([p["rev"] for p in json.load(open(sys.argv[1]))["packages"] if p["name"]=="mathlib"][0])' "$w/code/lake-manifest.json")
mlc=$home/mathlib
[ -d "$mlc/.git" ] || { git init -q "$mlc"; git -C "$mlc" remote add origin https://github.com/leanprover-community/mathlib4; }
git -C "$mlc" cat-file -e "$rev^{commit}" 2>/dev/null || git -C "$mlc" fetch -q --depth 1 origin "$rev"
mkdir "$w/mathlib"; git -C "$mlc" archive "$rev" | tar -x -C "$w/mathlib"

set +e
python3 "$eng/runner/review.py" --repo TauCetiProject/TauCeti --pr 0 --mode manual \
  --rubrics-dir "$eng/rubrics" --tool-cwd "$w" --code-path code --roadmap-path roadmap --mathlib-path mathlib \
  --diff-file "$w/diff.txt" --paths-file "$w/paths.z" --pr-desc-file "$w/pr_desc.txt" \
  --store "$w/store" --head-sha "$head" --merge-base-sha "$mb" --rubrics-sha "$rsha" \
  --auth subscription --providers "${TAUCETI_PROVIDERS:-claude}" --daily-budget 1000000 \
  --no-post ${only:+--rubrics "$only"} --scoreboard-file "$w/scoreboard.md" \
  --threads-dir "$w/threads" --post-plan-file "$w/plan.json" \
  --replies-json "$w/replies.json" --prior-scoreboard-json "$w/prior.json" >&2
rc=$?; set -e
[ $rc -eq 3 ] && { want=3; echo "local-review: provider down (login/quota); retry later" >&2; exit 3; }
[ $rc -eq 0 ] && [ -f "$w/scoreboard.md" ] || fail "engine failed ($rc)"

cat "$w/scoreboard.md"; for t in "$w"/threads/*.md; do [ -f "$t" ] && { echo; cat "$t"; }; done
echo; echo "local-review: head $head  TauCetiReview $rsha"
grep -qx '## AI review — approved' "$w/scoreboard.md" || { want=1; exit 1; }
