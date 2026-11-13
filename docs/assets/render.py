#!/usr/bin/env python3
"""Render docs/assets/cover.png (1500x1000, 3:2) and docs/assets/sample-report.png from HTML with headless Chrome.
The report content is copied from a real bench run: eval/v2/runs/skill-final/C01/final.md (stand-in model following the Skill)."""
import os
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))

ROWS = [
    ("Mon 2026-11-02", "09:00–12:00", "3 h 00", "09:04–11:58", "2 h 54", "6 min", "Confirmed", "ok"),
    ("Wed 2026-11-04", "09:00–13:00", "4 h 00", "09:10–11:25", "2 h 15", "billed 1 h 45 min more", "Billed more than seen", "more"),
    ("Thu 2026-11-05", "14:00–17:00", "3 h 00", "13:55–17:40", "3 h 45", "seen 45 min longer", "Seen more than billed", "seen"),
    ("Fri 2026-11-06", "09:00–12:00", "3 h 00", "09:02 only", "", "none", "Inconclusive · one sighting only", "inc"),
]

CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: Inter, 'DejaVu Sans', sans-serif; color: #12201a; }
.chip { display: inline-block; padding: 5px 11px; border-radius: 999px; font-weight: 600; font-size: 15px; white-space: nowrap; }
.ok { background: #d9f5e6; color: #0b6b3a; } .more { background: #ffedd0; color: #8a4b00; }
.seen { background: #dbeafe; color: #1e4fa3; } .inc { background: #eceff3; color: #4a5568; } .not { background: #fde2e1; color: #9b2c2c; }
.card { background: #fff; border-radius: 22px; box-shadow: 0 20px 60px rgba(9, 52, 32, .18); padding: 30px 32px; }
.card h3 { font-size: 22px; margin-bottom: 4px; } .card .sub { color: #5b6b63; font-size: 15px; margin-bottom: 18px; }
table { border-collapse: collapse; width: 100%; font-size: 16px; }
th { text-align: left; color: #6b7a72; font-weight: 600; font-size: 13px; text-transform: uppercase; letter-spacing: .06em; padding: 0 10px 10px 0; }
td { white-space: nowrap; padding: 12px 10px 12px 0; border-top: 1px solid #edf1ef; vertical-align: middle; }
td small { color: #6b7a72; }
.totals { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 18px; }
.tot { border-radius: 14px; padding: 12px 16px; font-size: 15px; } .tot b { display: block; font-size: 24px; margin-top: 2px; }
.user { align-self: flex-end; background: #0f5132; color: #fff; border-radius: 18px 18px 4px 18px; padding: 14px 20px; font-size: 18px; max-width: 80%; }
"""


def table(rows, narrow=False):
    out = ["<table><tr><th>Date</th><th>Billed</th><th>Seen at the door</th>" + ("" if narrow else "<th>Difference</th>") + "<th>Result</th></tr>"]
    for d, b, bh, s, sh, diff, res, cls in rows:
        out.append(f"<tr><td><b>{d[:3]}</b> {"Nov " + str(int(d[-2:]))}</td><td>{b}<br><small>{bh}</small></td><td>{s}<br><small>{sh}</small></td>"
                   + ("" if narrow else f"<td><small>{diff}</small></td>") + f"<td><span class='chip {cls}'>{res}</span></td></tr>")
    out.append("</table>")
    return "".join(out)


TOTALS = """<div class="totals">
<div class="tot more">Billed more than seen<b>1 h 45 min · $43.75</b></div>
<div class="tot seen">Seen more than billed<b>45 min · $18.75</b></div></div>"""

COVER = f"""<html><head><style>{CSS}
body {{ width: 1500px; height: 1000px; background: radial-gradient(1200px 700px at 85% 15%, #e3f7ec 0%, #f6faf8 55%, #eef3f1 100%); display: flex; padding: 70px 70px; gap: 56px; }}
.left {{ width: 520px; display: flex; flex-direction: column; justify-content: center; }}
.brand {{ font-size: 18px; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: #0f7a46; margin-bottom: 18px; }}
h1 {{ font-size: 92px; line-height: .95; letter-spacing: -2px; color: #0b3d26; }}
.tag {{ font-size: 28px; line-height: 1.3; margin: 26px 0 34px; color: #24382e; }}
.pts {{ font-size: 19px; line-height: 1.55; color: #33463c; }} .pts div::before {{ content: "→ "; color: #0f7a46; font-weight: 700; }}
.right {{ flex: 1; display: flex; flex-direction: column; justify-content: center; gap: 18px; }}
.foot {{ position: absolute; bottom: 34px; left: 70px; font-size: 16px; color: #5b6b63; }}
</style></head><body>
<div class="left"><div class="brand">Uliya Skill · UGREEN AI NAS</div><h1>Fair<br>Hours</h1>
<div class="tag">Did the hours on the bill happen at your door?</div>
<div class="pts"><div>Each billed visit vs. your entry camera</div><div>Differences counted both ways</div><div>Every doubt goes to the helper</div><div>Faces, bills and reports stay on the NAS</div></div></div>
<div class="right"><div class="user">Check Ana’s cleaning invoice against the front door camera.</div>
<div class="card"><h3>Fair Hours: Ana Ruiz, Nov 2–8</h3><div class="sub">Front Door camera · tolerance 10 min · $25/h printed</div>{table(ROWS, narrow=True)}{TOTALS}</div></div>
<div class="foot">Open Innovation · UGREEN Hackathon 2026 on AI NAS · sample from the offline test bench</div>
</body></html>"""

SAMPLE = f"""<html><head><style>{CSS} body {{ width: 1200px; padding: 30px; background: #f3f6f5; }}</style></head><body>
<div class="card"><h3>Fair Hours: Ana Ruiz, 2026-11-02 to 2026-11-08 (New York)</h3>
<div class="sub">Bill: Ana Ruiz - Nov week 1.pdf · Camera: Front Door · Tolerance 10 min · notice confirmed</div>
{table(ROWS)}{TOTALS}
<p style="margin-top:16px;font-size:15px;color:#33463c;line-height:1.5">Camera times show passages through the entry, not the work done between them.
A good way to go through this is with Ana, starting with Nov 5, where the difference is in her favour.</p></div></body></html>"""


def main():
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
        for name, html, size in [("cover", COVER, (1500, 1000)), ("sample-report", SAMPLE, (1200, 700))]:
            path = os.path.join(HERE, name + ".html")
            open(path, "w").write(html)
            pg = b.new_page(viewport={"width": size[0], "height": size[1]}, device_scale_factor=1)
            pg.goto("file://" + path)
            pg.screenshot(path=os.path.join(HERE, name + ".png"), full_page=(name != "cover"))
        b.close()
    print("ok")


if __name__ == "__main__":
    main()
