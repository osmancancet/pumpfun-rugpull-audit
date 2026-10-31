"""Figure 1 (conceptual, contains no data): decision time, label window and evaluation protocols."""
from PIL import Image, ImageDraw, ImageFont
import config as C
W, H = 2400, 1300
im = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(im)
def font(s):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"]:
        try: return ImageFont.truetype(p, s)
        except OSError: pass
    return ImageFont.load_default()
f, fb, fs = font(34), font(40), font(28)
d.text((60, 30), "(a) One launch: what is known when", font=fb, fill="black")
y = 200; x0, x1 = 120, 2280
d.line((x0, y, x1, y), fill="black", width=4)
def tick(x, lab, below=""):
    d.line((x, y - 25, x, y + 25), fill="black", width=4); d.text((x - 60, y - 75), lab, font=f, fill="black")
    if below: d.text((x - 60, y + 35), below, font=fs, fill="dimgray")
tick(x0, "t0", "create"); tick(380, "≤10 s", "f10 snapshot = decision time")
tick(1500, "300 s", "label horizon"); tick(2120, "t0 + 1 h", "embargo")
d.rectangle((x0, y + 110, 380, y + 160), fill="#4C72B0"); d.text((x0 + 10, y + 115), "features", font=fs, fill="white")
d.rectangle((380, y + 110, 1500, y + 160), fill="#DD8452"); d.text((400, y + 115), "rug event counted in y (strictly after snapshot)", font=fs, fill="white")
d.text((60, 470), "Creator history: an earlier launch counts only if its outcome time < t0 (causal reputation)", font=f, fill="black")
d.text((60, 560), "(b) Evaluation protocols (rows = launches, colour = split)", font=fb, fill="black")
rows = [("P1 random mint", "train/test interleaved; same creators on both sides"),
        ("P2 creator-grouped", "creators disjoint; time interleaved"),
        ("P3 time-forward", "train on days ≤ T, 1-day purge, test on next 2 days"),
        ("P4 time + unseen creator", "P3, test restricted to creators never seen in training")]
for i, (a, b) in enumerate(rows):
    yy = 650 + i * 150
    d.text((60, yy + 20), a, font=f, fill="black")
    for k in range(40):
        xx = 640 + k * 30
        if i == 0: c = "#DD8452" if (k * 7) % 5 == 0 else "#4C72B0"
        elif i == 1: c = "#DD8452" if k % 5 in (1, 3) else "#4C72B0"
        else: c = "#4C72B0" if k < 28 else ("white" if k < 30 else "#DD8452")
        d.rectangle((xx, yy + 10, xx + 24, yy + 70), fill=c, outline="gray")
    d.text((1880, yy + 25), "", font=fs, fill="black")
    d.text((640, yy + 80), b, font=fs, fill="dimgray")
d.rectangle((1900, 660, 1940, 700), fill="#4C72B0"); d.text((1955, 660), "train", font=fs, fill="black")
d.rectangle((1900, 720, 1940, 760), fill="#DD8452"); d.text((1955, 720), "test", font=fs, fill="black")
d.rectangle((1900, 780, 1940, 820), fill="white", outline="gray"); d.text((1955, 780), "purge gap", font=fs, fill="black")
C.FIGURES.mkdir(parents=True, exist_ok=True)
im.save(C.FIGURES / "fig1_design_schematic.png", dpi=(300, 300)); print("saved")
