#!/usr/bin/env python3
"""Build the Round 1 proposal PDF from proposal.md.

- Fills {{PLACEHOLDERS}} from values.json (bench numbers, entrant name).
- Counts English words in the ten answers only (title, headings and the Declarations section excluded,
  as the rules allow) and refuses to build over 500.
- Renders Markdown with pandoc, prints to PDF with headless Chrome (Playwright), and checks the 1 MB limit.
usage: python3 proposal/build_proposal.py [--allow-placeholders]
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "proposal.md")
VALUES = os.path.join(HERE, "values.json")
OUT_HTML = os.path.join(HERE, "Fair-Hours-Round1-Proposal.html")
OUT_PDF = os.path.join(HERE, "Fair-Hours-Round1-Proposal.pdf")

CSS = """
@page { size: Letter; }
body { font-family: Inter, 'DejaVu Sans', sans-serif; font-size: 9.6pt; line-height: 1.38; color: #1d2430; }
h1 { font-size: 20pt; margin: 0 0 2pt 0; color: #0f5132; letter-spacing: -0.3px; }
h1 + p { margin-top: 0; color: #4a5568; font-size: 10pt; }
h2 { font-size: 10.4pt; margin: 9pt 0 2pt 0; color: #0f5132; }
p { margin: 2pt 0 3pt 0; }
ul { margin: 2pt 0 3pt 0; padding-left: 15pt; }
li { margin: 0.5pt 0; }
hr { border: 0; border-top: 1px solid #cfd8dc; margin: 10pt 0 6pt 0; }
hr ~ h2, hr ~ p { font-size: 8.4pt; color: #4a5568; }
strong { color: #111827; }
img { display: block; margin: 5pt auto 4pt; border-radius: 6px; }
.wc { position: fixed; bottom: 0; right: 0; font-size: 7.5pt; color: #8a94a6; }
"""


def answers_text(md):
    body = md.split("## 1.", 1)[1].split("\n---", 1)[0]
    body = "## 1." + body
    lines = [l for l in body.splitlines() if not l.startswith("## ") and not l.startswith("![")]
    text = " ".join(lines)
    text = re.sub(r"[*`#>|]", " ", text)
    return text


def count_words(text):
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’./+\-–]*", text))


def main():
    allow = "--allow-placeholders" in sys.argv
    md = open(SRC).read()
    values = json.load(open(VALUES)) if os.path.exists(VALUES) else {}
    for k, v in values.items():
        md = md.replace("{{" + k + "}}", str(v))
    left = sorted(set(re.findall(r"\{\{([A-Z_]+)\}\}", md)))
    if left and not allow:
        sys.exit(f"unfilled placeholders: {left}")
    words = count_words(answers_text(md))
    print(f"words in the ten answers: {words} / 500")
    if words > 500:
        sys.exit("over the 500-word limit")
    html = subprocess.run(["pandoc", "-f", "markdown", "-t", "html5", "--standalone", "--metadata", "title=Fair Hours: Round 1 Proposal"],
                          input=md, capture_output=True, text=True, check=True).stdout
    html = html.replace("</head>", f"<style>{CSS}</style></head>")
    html = re.sub(r"<header id=\"title-block-header\">.*?</header>", "", html, flags=re.S)
    html = html.replace("</body>", f'<div class="wc">Ten answers: {words} words</div></body>')
    open(OUT_HTML, "w").write(html)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = b.new_page()
        pg.goto("file://" + OUT_HTML)
        pg.pdf(path=OUT_PDF, format="Letter", print_background=True, margin={"top": "15mm", "bottom": "15mm", "left": "17mm", "right": "17mm"})
        b.close()
    size = os.path.getsize(OUT_PDF)
    print(f"PDF {OUT_PDF} {size} bytes ({'OK' if size <= 1024 * 1024 else 'OVER 1 MB'})")
    if size > 1024 * 1024:
        sys.exit(1)


if __name__ == "__main__":
    main()
