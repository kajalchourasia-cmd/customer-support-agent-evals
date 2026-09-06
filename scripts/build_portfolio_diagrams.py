from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parents[1] / "assets" / "diagrams"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1600, 900
NAVY = "#12304A"
TEAL = "#159E91"
MINT = "#DDF5EF"
BLUE = "#DCECF8"
GOLD = "#F4B740"
RED = "#D65A5A"
INK = "#18252F"
MUTED = "#5B6872"
BG = "#F7FAFC"
WHITE = "#FFFFFF"


def font(size, bold=False):
    name = "seguisb.ttf" if bold else "segoeui.ttf"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / name), size)


def canvas(title, subtitle):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((54, 42, W - 54, H - 42), 28, fill=WHITE, outline="#D9E2E8", width=2)
    d.text((100, 82), title, font=font(48, True), fill=NAVY)
    d.text((100, 148), subtitle, font=font(25), fill=MUTED)
    d.line((100, 200, W - 100, 200), fill=TEAL, width=5)
    return im, d


def centered(d, box, text, size=25, bold=False, color=INK):
    f = font(size, bold)
    lines = text.split("\n")
    heights = [d.textbbox((0, 0), line, font=f)[3] for line in lines]
    total = sum(heights) + (len(lines) - 1) * 10
    y = box[1] + (box[3] - box[1] - total) / 2
    for line, hh in zip(lines, heights):
        bb = d.textbbox((0, 0), line, font=f)
        x = box[0] + (box[2] - box[0] - (bb[2] - bb[0])) / 2
        d.text((x, y), line, font=f, fill=color)
        y += hh + 10


def box(d, xy, title, detail, fill=BLUE, border=NAVY):
    d.rounded_rectangle(xy, 22, fill=fill, outline=border, width=3)
    centered(d, (xy[0] + 12, xy[1] + 16, xy[2] - 12, xy[1] + 78), title, 26, True, NAVY)
    centered(d, (xy[0] + 22, xy[1] + 80, xy[2] - 22, xy[3] - 16), detail, 20, False, INK)


def arrow(d, x1, y1, x2, y2, color=TEAL, width=7):
    d.line((x1, y1, x2, y2), fill=color, width=width)
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    a = 18
    pts = [(x2, y2), (x2 - a * math.cos(ang - .55), y2 - a * math.sin(ang - .55)),
           (x2 - a * math.cos(ang + .55), y2 - a * math.sin(ang + .55))]
    d.polygon(pts, fill=color)


def footer(d, text):
    d.text((100, 825), text, font=font(18), fill=MUTED)


def architecture():
    im, d = canvas("System architecture", "How a support ticket becomes an evaluated, traceable routing decision")
    xs = [90, 390, 690, 990, 1290]
    titles = ["Ticket", "LangGraph", "Model", "Structured output", "LangSmith"]
    details = ["ticket_text", "classify node\n+ state", "prompt +\ncategory policy", "category +\nreasoning", "trace + scores\n+ comparison"]
    fills = [MINT, BLUE, "#EEE7FA", MINT, "#FFF1D6"]
    for x, t, de, f in zip(xs, titles, details, fills):
        box(d, (x, 315, x + 220, 555), t, de, f)
    for x in xs[:-1]:
        arrow(d, x + 220, 435, x + 292, 435)
    d.rounded_rectangle((370, 635, 1230, 755), 18, fill="#F0F7FA", outline="#B9CCD8", width=2)
    centered(d, (390, 646, 1210, 744), "Reference labels grade the output after inference;\nthey are not passed to the model as answers.", 24, True, NAVY)
    footer(d, "LangGraph executes the workflow. LangSmith records and evaluates it.")
    im.save(OUT / "01_system_architecture.png")


def lifecycle():
    im, d = canvas("Evaluation lifecycle", "The repeatable product loop from quality definition to production learning")
    steps = [
        ("1", "Define good", "User outcome, risk, rubric"),
        ("2", "Build evidence", "Examples, labels, slices"),
        ("3", "Run experiment", "Frozen baseline and candidate"),
        ("4", "Analyze", "Metrics, regressions, traces"),
        ("5", "Decide", "Pass, Review, or Fail"),
        ("6", "Learn in production", "Monitor, annotate, add tests"),
    ]
    coords = [(100, 285), (550, 285), (1000, 285), (1000, 585), (550, 585), (100, 585)]
    for (num, title, detail), (x, y) in zip(steps, coords):
        d.ellipse((x, y, x + 64, y + 64), fill=TEAL)
        centered(d, (x, y, x + 64, y + 64), num, 28, True, WHITE)
        d.text((x + 82, y - 3), title, font=font(27, True), fill=NAVY)
        d.text((x + 82, y + 38), detail, font=font(20), fill=MUTED)
    arrow(d, 405, 317, 535, 317)
    arrow(d, 855, 317, 985, 317)
    arrow(d, 1320, 365, 1320, 565)
    arrow(d, 990, 617, 870, 617)
    arrow(d, 540, 617, 420, 617)
    arrow(d, 130, 575, 130, 390)
    d.rounded_rectangle((520, 420, 1080, 520), 18, fill="#FFF7E7", outline=GOLD, width=3)
    centered(d, (540, 430, 1060, 510), "Every score must support\na product decision.", 27, True, NAVY)
    footer(d, "Production failures return to the offline regression set only after human review.")
    im.save(OUT / "02_evaluation_lifecycle.png")


def evidence_design():
    im, d = canvas("Evidence design and integrity boundaries", "Three evidence streams, three separate conclusions")
    columns = [
        (90, "Supplied workbook", "150 cases\n121 correct / 29 failures", "Human audit and\nfailure taxonomy", MINT),
        (570, "Frozen notebook", "100 cases\n91 → 98 correct", "8 wins, 1 regression\nDecision: REVIEW", BLUE),
        (1050, "Controlled workbook run", "150 cases\n145 → 146 correct", "1 win, 0 regressions\nDecision: REVIEW", "#FFF1D6"),
    ]
    for x, title, score, use, fill in columns:
        box(d, (x, 280, x + 390, 620), title, score, fill)
        d.rounded_rectangle((x + 35, 650, x + 355, 750), 16, fill=WHITE, outline="#C7D3DB", width=2)
        centered(d, (x + 50, 660, x + 340, 740), use, 21, True, NAVY)
    d.line((540, 260, 540, 775), fill=RED, width=3)
    d.line((1020, 260, 1020, 775), fill=RED, width=3)
    d.text((112, 235), "Do not merge scores across different artifacts or policies", font=font(23, True), fill=RED)
    footer(d, "Later benchmark-informed iterations and perfect-score claims are excluded.")
    im.save(OUT / "03_evidence_integrity.png")


def decision_gate():
    im, d = canvas("Why 98% still means Review", "Aggregate improvement does not override a preregistered regression gate")
    box(d, (100, 285, 430, 575), "Baseline V1", "91 / 100\n9 errors", BLUE)
    arrow(d, 455, 430, 610, 430)
    box(d, (635, 285, 965, 575), "Focused V2", "98 / 100\n2 errors", MINT)
    d.rounded_rectangle((1030, 265, 1490, 595), 24, fill="#FFF7E7", outline=GOLD, width=4)
    d.text((1080, 305), "Outcome accounting", font=font(30, True), fill=NAVY)
    lines = [("90", "stable passes", TEAL), ("8", "wins", TEAL), ("1", "regression", RED), ("1", "remaining failure", GOLD)]
    y = 370
    for n, label, color in lines:
        d.text((1080, y), n, font=font(30, True), fill=color)
        d.text((1140, y + 3), label, font=font(23), fill=INK)
        y += 52
    d.rounded_rectangle((290, 660, 1310, 770), 20, fill="#FDECEC", outline=RED, width=3)
    centered(d, (310, 670, 1290, 760), "Regression rate = 1 ÷ 91 = 1.10%\nGate ≤ 1.00%  →  REVIEW", 29, True, RED)
    footer(d, "Release rules must be defined before results are inspected.")
    im.save(OUT / "04_release_decision.png")


if __name__ == "__main__":
    architecture()
    lifecycle()
    evidence_design()
    decision_gate()
    print(f"Created 4 diagrams in {OUT}")
