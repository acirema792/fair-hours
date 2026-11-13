#!/usr/bin/env python3
"""Build the Round 1 Skill ZIP: dist/fair-hours.zip containing fair-hours/SKILL.md and fair-hours/references/*.md.

Refuses to build unless the official static checker (uliya-skill-kit 0.7.3 rules) returns static-pass with
0 errors and 0 warnings. Re-checks the unzipped copy, enforces the rules' limits (ZIP and unzipped <= 10 MB,
<= 1 MB per file, <= 100 files, Markdown only) and prints SHA-256 checksums.
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, "skill", "fair-hours")
# The official checker: set ULIYA_SKILL_KIT to an unzipped uliya-skill-kit 0.7.3 folder (from the Hackathon
# Starter Kit). Falls back to a local copy in tools/uliya-kit-local/ (kept out of the public repository).
_KIT = os.environ.get("ULIYA_SKILL_KIT") or os.path.join(ROOT, "tools", "uliya-kit-local")
CHECK = os.path.join(_KIT, "scripts", "check-skill.mjs")
if not os.path.exists(CHECK):
    sys.exit("official checker not found: set ULIYA_SKILL_KIT to the unzipped uliya-skill-kit folder")
DIST = os.path.join(ROOT, "dist")
OUT = os.path.join(DIST, "fair-hours.zip")


def check(path):
    r = subprocess.run(["node", CHECK, path], capture_output=True, text=True)
    res = json.loads(r.stdout)
    ok = res["status"] == "static-pass" and res["summary"]["errors"] == 0 and res["summary"]["warnings"] == 0
    return ok, res


def main():
    ok, res = check(SKILL)
    print("checker:", res["status"], res["summary"])
    if not ok:
        sys.exit("refusing to build: the checker must pass with 0 errors and 0 warnings")
    files = []
    for dirpath, _, names in os.walk(SKILL):
        for n in sorted(names):
            full = os.path.join(dirpath, n)
            rel = os.path.relpath(full, SKILL)
            if not n.endswith(".md"):
                sys.exit(f"non-Markdown file in package: {rel}")
            files.append((full, "fair-hours/" + rel.replace(os.sep, "/")))
    os.makedirs(DIST, exist_ok=True)
    if os.path.exists(OUT):
        os.remove(OUT)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for full, arc in sorted(files, key=lambda x: x[1]):
            info = zipfile.ZipInfo(arc, date_time=(2026, 11, 15, 12, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, open(full, "rb").read())
    total = sum(os.path.getsize(f) for f, _ in files)
    biggest = max(os.path.getsize(f) for f, _ in files)
    zsize = os.path.getsize(OUT)
    print(f"files {len(files)} (max 100) · unzipped {total} B · largest {biggest} B (max 1 MB) · zip {zsize} B (max 10 MB)")
    assert len(files) <= 100 and total <= 10 * 2**20 and biggest <= 2**20 and zsize <= 10 * 2**20
    with tempfile.TemporaryDirectory() as tmp:
        zipfile.ZipFile(OUT).extractall(tmp)
        ok2, res2 = check(os.path.join(tmp, "fair-hours"))
        print("unzipped copy checker:", res2["status"], res2["summary"])
        if not ok2:
            sys.exit("unzipped copy fails the checker")
    lines = [f"{hashlib.sha256(open(OUT, 'rb').read()).hexdigest()}  fair-hours.zip"]
    for full, arc in sorted(files, key=lambda x: x[1]):
        lines.append(f"{hashlib.sha256(open(full, 'rb').read()).hexdigest()}  {arc}")
    open(os.path.join(DIST, "SHA256SUMS.txt"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
