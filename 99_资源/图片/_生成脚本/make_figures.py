# -*- coding: utf-8 -*-
"""Generate PNG figures for the handbook using Pillow only."""
from pathlib import Path
import math

from PIL import Image, ImageDraw, ImageFont

BASE = Path(r"C:\DeepSeek_ Project\智能装备电子硬件学习手册\99_资源\图片")
for sub in ["01", "02", "03", "04"]:
    (BASE / sub).mkdir(parents=True, exist_ok=True)

FONT = r"C:\Windows\Fonts\msyh.ttc"
F_TITLE = ImageFont.truetype(FONT, 30)
F_LABEL = ImageFont.truetype(FONT, 22)
F_SMALL = ImageFont.truetype(FONT, 18)
F_TICK = ImageFont.truetype(FONT, 17)

INK = (31, 41, 55)
BLUE = (29, 78, 216)
RED = (185, 28, 28)
GRAY = (107, 114, 128)
LIGHT = (229, 231, 235)
WHITE = (255, 255, 255)
GREEN = (21, 128, 61)


def canvas(w=1000, h=620):
    img = Image.new("RGB", (w, h), WHITE)
    return img, ImageDraw.Draw(img)


def txt(d, x, y, s, font=F_LABEL, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)


def wire(d, pts, color=INK, w=3):
    d.line(pts, fill=color, width=w, joint="curve")


def dot(d, x, y, r=5, color=INK):
    d.ellipse([x - r, y - r, x + r, y + r], fill=color)


def res_v(d, x, y, h=90, label="R1", val="10 kΩ"):
    pts = [(x, y)]
    n = 6
    seg = h / n
    for i in range(n):
        pts.append((x + (12 if i % 2 == 0 else -12), y + seg * i + seg / 2))
    pts.append((x, y + h))
    d.line(pts, fill=INK, width=3, joint="curve")
    txt(d, x + 22, y + h / 2 - 26, label, F_SMALL)
    txt(d, x + 22, y + h / 2 - 2, val, F_SMALL, GRAY)


def res_h(d, x, y, w=90, label="R1", val="10 kΩ"):
    pts = [(x, y)]
    n = 6
    seg = w / n
    for i in range(n):
        pts.append((x + seg * i + seg / 2, y + (12 if i % 2 == 0 else -12)))
    pts.append((x + w, y))
    d.line(pts, fill=INK, width=3, joint="curve")
    txt(d, x + w / 2, y - 48, label, F_SMALL, INK, "mm")
    txt(d, x + w / 2, y - 22, val, F_SMALL, GRAY, "mm")


def cap_v(d, x, y, h=70, label="C1", val="100 nF"):
    cy = y + h / 2
    d.line([(x, y), (x, cy - 7)], fill=INK, width=3)
    d.line([(x - 22, cy - 7), (x + 22, cy - 7)], fill=INK, width=5)
    d.line([(x - 22, cy + 7), (x + 22, cy + 7)], fill=INK, width=5)
    d.line([(x, cy + 7), (x, y + h)], fill=INK, width=3)
    txt(d, x + 30, cy - 30, label, F_SMALL)
    txt(d, x + 30, cy - 6, val, F_SMALL, GRAY)


def gnd(d, x, y):
    d.line([(x, y), (x, y + 16)], fill=INK, width=3)
    d.line([(x - 26, y + 16), (x + 26, y + 16)], fill=INK, width=4)
    d.line([(x - 16, y + 25), (x + 16, y + 25)], fill=INK, width=4)
    d.line([(x - 7, y + 34), (x + 7, y + 34)], fill=INK, width=4)


def source_v(d, x, y, label="V1", val="12 V"):
    d.ellipse([x - 30, y - 30, x + 30, y + 30], outline=INK, width=3)
    txt(d, x, y - 20, "+", F_TITLE, INK, "mm")
    txt(d, x, y + 18, "−", F_TITLE, INK, "mm")
    d.line([(x, y - 30), (x, y - 60)], fill=INK, width=3)
    d.line([(x, y + 30), (x, y + 60)], fill=INK, width=3)
    txt(d, x - 40, y - 22, label, F_SMALL, INK, "ra")
    txt(d, x - 40, y + 4, val, F_SMALL, GRAY, "ra")


def opamp(d, x, y, w=160, h=150):
    d.polygon([(x, y), (x, y + h), (x + w, y + h / 2)], outline=INK, fill=WHITE)
    d.line([(x, y), (x, y + h), (x + w, y + h / 2), (x, y)], fill=INK, width=3)
    txt(d, x + 14, y + h * 0.30 - 12, "−", F_TITLE)
    txt(d, x + 14, y + h * 0.70 - 14, "+", F_TITLE)
    txt(d, x + w / 2 - 8, y + h / 2 - 14, "A", F_LABEL, GRAY)


def nmos(d, x, y):
    # gate plate at x, drain up-right, source down-right
    d.line([(x, y - 42), (x, y + 42)], fill=INK, width=5)
    d.line([(x + 14, y - 36), (x + 14, y - 10)], fill=INK, width=4)
    d.line([(x + 14, y - 5), (x + 14, y + 5)], fill=INK, width=4)
    d.line([(x + 14, y + 10), (x + 14, y + 36)], fill=INK, width=4)
    d.line([(x + 14, y - 36), (x + 52, y - 36), (x + 52, y - 70)], fill=INK, width=3)
    d.line([(x + 14, y + 36), (x + 52, y + 36), (x + 52, y + 70)], fill=INK, width=3)
    d.polygon([(x + 14, y - 2), (x + 40, y + 8), (x + 14, y + 18)], fill=INK)
    txt(d, x + 60, y - 88, "D", F_SMALL)
    txt(d, x + 60, y + 58, "S", F_SMALL)
    txt(d, x - 32, y - 10, "G", F_SMALL, INK, "ra")
    txt(d, x - 10, y + 95, "NMOS", F_SMALL, GRAY, "mm")


def diode_v(d, x, y):
    d.polygon([(x - 18, y - 18), (x + 18, y - 18), (x, y + 12)], outline=INK, fill=WHITE)
    d.line([(x - 18, y - 18), (x + 18, y - 18), (x, y + 12), (x - 18, y - 18)], fill=INK, width=3)
    d.line([(x - 18, y + 12), (x + 18, y + 12)], fill=INK, width=5)
    d.line([(x, y - 30), (x, y - 18)], fill=INK, width=3)
    d.line([(x, y + 12), (x, y + 30)], fill=INK, width=3)


def save(img, rel):
    p = BASE / rel
    img.save(p)
    print("wrote", p)


# ---------- 01-01 divider ----------
img, d = canvas(1000, 600)
txt(d, 40, 30, "图 01-01  分压电路与加载效应", F_TITLE)
source_v(d, 160, 300, "V1", "12 V")
wire(d, [(160, 240), (160, 130), (380, 130)])
wire(d, [(160, 360), (160, 500), (380, 500)])
res_v(d, 380, 130, 100, "R1", "10 kΩ")
res_v(d, 380, 300, 100, "R2", "10 kΩ")
wire(d, [(380, 230), (380, 300)])
dot(d, 380, 265)
wire(d, [(380, 265), (650, 265)])
res_v(d, 650, 290, 100, "RL", "10 kΩ")
wire(d, [(650, 265), (650, 290)])
wire(d, [(650, 390), (650, 500), (380, 500)])
wire(d, [(380, 400), (380, 500)])
gnd(d, 380, 500)
txt(d, 400, 232, "A", F_LABEL, BLUE)
txt(d, 670, 250, "Vout", F_LABEL, BLUE)
txt(d, 60, 550, "空载 6.0 V；接 10 kΩ 负载后 4.0 V。负载越重，输出越低。", F_SMALL, GRAY)
save(img, "01/图01-01_分压电路.png")

# ---------- 02-01 NMOS ----------
img, d = canvas(1000, 660)
txt(d, 40, 30, "图 02-01  NMOS 低边开关（含续流二极管）", F_TITLE)
txt(d, 120, 100, "+12 V", F_LABEL, RED)
wire(d, [(190, 110), (520, 110)])
d.rectangle([360, 140, 500, 210], outline=INK, fill=(243, 244, 246), width=3)
txt(d, 430, 165, "负载", F_LABEL, INK, "mm")
wire(d, [(430, 110), (430, 140)])
wire(d, [(430, 210), (430, 250), (522, 250)])
nmos(d, 470, 320)
wire(d, [(522, 390), (522, 450), (360, 450)])
gnd(d, 360, 450)
diode_v(d, 300, 175)
wire(d, [(300, 145), (300, 110)])
wire(d, [(300, 145), (360, 145)])
wire(d, [(300, 205), (300, 250), (430, 250)])
txt(d, 240, 150, "D1 续流", F_SMALL, INK, "ra")
res_h(d, 150, 320, 100, "Rg", "100 Ω")
wire(d, [(250, 320), (470, 320)])
dot(d, 300, 320)
res_v(d, 300, 320, 100, "Rpd", "10 kΩ")
wire(d, [(300, 420), (300, 450)])
txt(d, 40, 300, "PWM", F_SMALL, BLUE, "ra")
txt(d, 40, 326, "3.3 V", F_SMALL, BLUE, "ra")
txt(d, 570, 290, "VDS", F_LABEL, BLUE)
txt(d, 570, 316, "测这里", F_SMALL, GRAY)
save(img, "02/图02-01_NMOS低边开关.png")
print("done schematics")
