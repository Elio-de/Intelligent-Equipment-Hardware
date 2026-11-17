# -*- coding: utf-8 -*-
"""Remaining figures: op-amp schematics, plots, timing, ADC."""
from pathlib import Path
import math

from PIL import Image, ImageDraw, ImageFont

BASE = Path(r"C:\DeepSeek_ Project\智能装备电子硬件学习手册\99_资源\图片")
FONT = r"C:\Windows\Fonts\msyh.ttc"
F_TITLE = ImageFont.truetype(FONT, 30)
F_LABEL = ImageFont.truetype(FONT, 22)
F_SMALL = ImageFont.truetype(FONT, 18)
F_TICK = ImageFont.truetype(FONT, 16)
INK = (31, 41, 55); BLUE = (29, 78, 216); RED = (185, 28, 28)
GRAY = (107, 114, 128); WHITE = (255, 255, 255); GREEN = (21, 128, 61)
LIGHT = (229, 231, 235)


def canvas(w=1000, h=640):
    img = Image.new("RGB", (w, h), WHITE)
    return img, ImageDraw.Draw(img)


def txt(d, x, y, s, font=F_LABEL, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)


def wire(d, pts, color=INK, w=3):
    d.line(pts, fill=color, width=w, joint="curve")


def dot(d, x, y, r=5, color=INK):
    d.ellipse([x - r, y - r, x + r, y + r], fill=color)


def res_h(d, x, y, w=90, label="R1", val="10 kΩ"):
    pts = [(x, y)]; n = 6; seg = w / n
    for i in range(n):
        pts.append((x + seg * i + seg / 2, y + (11 if i % 2 == 0 else -11)))
    pts.append((x + w, y))
    d.line(pts, fill=INK, width=3, joint="curve")
    txt(d, x + w / 2, y - 44, label, F_SMALL, INK, "mm")
    txt(d, x + w / 2, y - 21, val, F_SMALL, GRAY, "mm")


def res_v(d, x, y, h=90, label="R1", val="10 kΩ"):
    pts = [(x, y)]; n = 6; seg = h / n
    for i in range(n):
        pts.append((x + (11 if i % 2 == 0 else -11), y + seg * i + seg / 2))
    pts.append((x, y + h))
    d.line(pts, fill=INK, width=3, joint="curve")
    txt(d, x + 22, y + h / 2 - 22, label, F_SMALL)
    txt(d, x + 22, y + h / 2 + 2, val, F_SMALL, GRAY)


def cap_v(d, x, y, h=70, label="C1", val="10 nF"):
    cy = y + h / 2
    d.line([(x, y), (x, cy - 7)], fill=INK, width=3)
    d.line([(x - 22, cy - 7), (x + 22, cy - 7)], fill=INK, width=5)
    d.line([(x - 22, cy + 7), (x + 22, cy + 7)], fill=INK, width=5)
    d.line([(x, cy + 7), (x, y + h)], fill=INK, width=3)
    txt(d, x + 30, cy - 26, label, F_SMALL)
    txt(d, x + 30, cy - 2, val, F_SMALL, GRAY)


def gnd(d, x, y):
    d.line([(x, y), (x, y + 15)], fill=INK, width=3)
    d.line([(x - 24, y + 15), (x + 24, y + 15)], fill=INK, width=4)
    d.line([(x - 14, y + 23), (x + 14, y + 23)], fill=INK, width=4)
    d.line([(x - 6, y + 31), (x + 6, y + 31)], fill=INK, width=4)


def amp_block(d, x, y, w=170, h=150):
    d.rectangle([x, y, x + w, y + h], outline=INK, fill=WHITE, width=3)
    ym = y + h * 0.25
    yp = y + h * 0.75
    d.line([(x, ym), (x + 26, ym)], fill=INK, width=3)
    d.line([(x, yp), (x + 26, yp)], fill=INK, width=3)
    txt(d, x + 34, ym - 14, "−", F_TITLE)
    txt(d, x + 34, yp - 15, "+", F_TITLE)
    txt(d, x + w / 2, y + h / 2, "A", F_LABEL, GRAY, "mm")
    return (x, ym), (x, yp), (x + w, y + h / 2)


def save(img, rel):
    p = BASE / rel
    img.save(p)
    print("wrote", p)


# ---------- 03-01 non-inverting ----------
img, d = canvas(1000, 560)
txt(d, 40, 30, "图 03-01  同相放大器（方块为运放等效）", F_TITLE)
mn, pl, out = amp_block(d, 420, 170)
txt(d, 60, 370, "Vin", F_LABEL, BLUE)
wire(d, [(120, 380), (400, 380), (400, pl[1]), (420, pl[1])])
wire(d, [(out[0], out[1]), (720, out[1])])
txt(d, 640, out[1] - 38, "Vout", F_LABEL, BLUE)
wire(d, [(mn[0], mn[1]), (340, mn[1]), (340, 140)])
res_h(d, 340, 140, 180, "Rf", "100 kΩ")
wire(d, [(520, 140), (700, 140), (700, out[1])])
dot(d, 700, out[1])
res_v(d, 340, mn[1], 110, "Rg", "10 kΩ")
wire(d, [(340, mn[1] + 110), (340, 340)])
gnd(d, 340, 340)
txt(d, 560, 420, "Av = 1 + Rf/Rg = 11", F_LABEL, GRAY)
save(img, "03/图03-01_同相放大器.png")

# ---------- 03-02 Sallen-Key ----------
img, d = canvas(1000, 580)
txt(d, 40, 30, "图 03-02  二阶 Sallen-Key 低通（方块为运放等效）", F_TITLE)
mn, pl, out = amp_block(d, 420, 200)
txt(d, 50, 340, "Vin", F_LABEL, BLUE)
res_h(d, 110, 350, 110, "R1", "10 kΩ")
wire(d, [(220, 350), (250, 350)])
dot(d, 250, 350)
res_h(d, 250, 350, 110, "R2", "10 kΩ")
wire(d, [(360, 350), (390, 350), (390, pl[1]), (420, pl[1])])
wire(d, [(out[0], out[1]), (720, out[1])])
txt(d, 610, out[1] - 36, "Vout", F_LABEL, BLUE)
wire(d, [(250, 350), (250, 250)])
cap_v(d, 250, 180, 70, "C1", "22 nF")
wire(d, [(250, 180), (250, 150), (720, 150), (720, out[1])])
dot(d, 720, out[1])
wire(d, [(390, pl[1]), (390, 430)])
cap_v(d, 390, 430, 70, "C2", "10 nF")
wire(d, [(390, 500), (390, 520)])
gnd(d, 390, 520)
wire(d, [(out[0], out[1]), (720, out[1]), (720, 110), (380, 110), (380, mn[1]), (420, mn[1])])
txt(d, 470, 545, "f0 ≈ 1.07 kHz, Q ≈ 0.74", F_LABEL, GRAY)
save(img, "03/图03-02_SallenKey低通.png")

# ---------- 03-03 comparator ----------
img, d = canvas(1000, 580)
txt(d, 40, 30, "图 03-03  迟滞比较器（方块为比较器等效）", F_TITLE)
mn, pl, out = amp_block(d, 420, 180)
txt(d, 50, 205, "Vref", F_LABEL, BLUE)
wire(d, [(130, mn[1]), (420, mn[1])])
txt(d, 50, 300, "Vin", F_LABEL, BLUE)
res_h(d, 120, 315, 110, "R1", "10 kΩ")
wire(d, [(230, 315), (420, 315)])
dot(d, 270, 315)
wire(d, [(out[0], out[1]), (740, out[1])])
dot(d, 650, out[1])
txt(d, 700, out[1] + 45, "Vout", F_LABEL, BLUE)
d.rectangle([620, 110, 680, 140], outline=INK, fill=(243, 244, 246), width=3)
txt(d, 650, 125, "5 V", F_SMALL, INK, "mm")
wire(d, [(650, 140), (650, 160)])
res_v(d, 650, 160, 60, "R3", "10 kΩ")
wire(d, [(650, 220), (650, 255)])
dot(d, 650, 255)
wire(d, [(270, 315), (270, 430), (740, 430), (740, 255)])
dot(d, 740, 255)
txt(d, 660, 470, "R2 = 100 kΩ 正反馈", F_SMALL, GRAY, "mm")
txt(d, 250, 530, "VTH− = 2.25 V, VTH+ = 3.25 V, 回差 = 1.0 V", F_LABEL, GRAY)
save(img, "03/图03-03_迟滞比较器.png")


# ---------- plots ----------
def frame(d, x0, y0, x1, y1, title, xunit, yunit):
    txt(d, 40, 25, title, F_TITLE)
    for i in range(6):
        x = x0 + (x1 - x0) * i / 5
        d.line([(x, y0), (x, y1)], fill=(244, 245, 247), width=1)
        y = y0 + (y1 - y0) * i / 5
        d.line([(x0, y), (x1, y)], fill=(244, 245, 247), width=1)
    d.line([(x0, y1), (x1, y1)], fill=INK, width=3)
    d.line([(x0, y0), (x0, y1)], fill=INK, width=3)
    txt(d, x0, y1 + 38, xunit, F_SMALL, GRAY)
    txt(d, x0 - 4, y0 - 28, yunit, F_SMALL, GRAY)


def xmap(v, vmin, vmax, x0, x1):
    return x0 + (v - vmin) / (vmax - vmin) * (x1 - x0)


def ymap(v, vmin, vmax, y0, y1):
    return y1 - (v - vmin) / (vmax - vmin) * (y1 - y0)


def ticks_x(d, x0, y0, x1, y1, vmin, vmax, fmt="{:.1f}", n=5):
    for i in range(n + 1):
        v = vmin + (vmax - vmin) * i / n
        x = x0 + (x1 - x0) * i / n
        d.line([(x, y1), (x, y1 + 7)], fill=INK, width=2)
        txt(d, x, y1 + 12, fmt.format(v), F_TICK, GRAY, "ma")


def ticks_y(d, x0, y0, x1, y1, vmin, vmax, fmt="{:.1f}", n=5):
    for i in range(n + 1):
        v = vmin + (vmax - vmin) * i / n
        y = ymap(v, vmin, vmax, y0, y1)
        d.line([(x0 - 7, y), (x0, y)], fill=INK, width=2)
        txt(d, x0 - 12, y, fmt.format(v), F_TICK, GRAY, "rm")


# 01-02 RC
img, d = canvas(1000, 640)
frame(d, 140, 90, 930, 470, "图 01-02  RC 充电曲线（τ = 1 ms）", "时间 t / ms", "v_C / V")
ticks_x(d, 140, 90, 930, 470, 0, 6, "{:.0f}")
ticks_y(d, 140, 90, 930, 470, 0, 3.5, "{:.1f}")
pts = [(xmap(i / 100, 0, 6, 140, 930), ymap(3.3 * (1 - math.exp(-(i / 100))), 0, 3.5, 90, 470)) for i in range(601)]
d.line(pts, fill=BLUE, width=4)
for t, lab in [(1, "1τ 2.09 V"), (5, "5τ 3.28 V")]:
    v = 3.3 * (1 - math.exp(-t)); x = xmap(t, 0, 6, 140, 930); y = ymap(v, 0, 3.5, 90, 470)
    d.line([(x, y), (x, 470)], fill=GRAY, width=2)
    d.line([(140, y), (x, y)], fill=GRAY, width=2)
    dot(d, x, y, 6, RED)
    txt(d, x + 12, y - 34, lab, F_SMALL, RED)
txt(d, 140, 530, "v(t)=3.3(1−e^(−t/τ))，τ=RC=10 kΩ×100 nF=1 ms；5τ 后误差 <1%。", F_SMALL, GRAY)
save(img, "01/图01-02_RC充电曲线.png")

# 01-03 RLC
img, d = canvas(1000, 640)
frame(d, 140, 90, 930, 470, "图 01-03  二阶 RLC 阶跃响应", "时间 t / ms", "v_C（归一化）")
ticks_x(d, 140, 90, 930, 470, 0, 0.4, "{:.1f}")
ticks_y(d, 140, 90, 930, 470, 0, 1.8, "{:.1f}")
w0 = 1e5
for zeta, color in [(0.25, BLUE), (1.0, GREEN)]:
    pts = []
    for i in range(801):
        t = i * 0.4e-3 / 800
        if zeta < 1:
            wd = w0 * math.sqrt(1 - zeta ** 2)
            v = 1 - math.exp(-zeta * w0 * t) * (math.cos(wd * t) + zeta / math.sqrt(1 - zeta ** 2) * math.sin(wd * t))
        else:
            v = 1 - math.exp(-w0 * t) * (1 + w0 * t)
        pts.append((xmap(t * 1e3, 0, 0.4, 140, 930), ymap(v, 0, 1.8, 90, 470)))
    d.line(pts, fill=color, width=4)
d.line([(760, 170), (800, 170)], fill=BLUE, width=4); txt(d, 810, 160, "ζ=0.25", F_SMALL, BLUE)
d.line([(760, 205), (800, 205)], fill=GREEN, width=4); txt(d, 810, 195, "ζ=1", F_SMALL, GREEN)
txt(d, 140, 530, "ω0=100 krad/s；ζ=(R/2)·√(C/L)。ζ<1 有振铃，ζ=1 最快无超调。", F_SMALL, GRAY)
save(img, "01/图01-03_RLC阶跃响应.png")

# 01-04 Bode
img, d = canvas(1000, 640)
frame(d, 140, 90, 930, 470, "图 01-04  一阶 RC 低通 Bode 图（fc=1.59 kHz）", "频率 f / Hz（对数）", "增益 / dB")
for i in range(6):
    f = 10 ** (1 + i); x = xmap(i + 1, 1, 6, 140, 930)
    d.line([(x, 470), (x, 477)], fill=INK, width=2)
    txt(d, x, 482, f"{f:.0f}" if f < 1000 else f"{f/1000:.0f}k", F_TICK, GRAY, "ma")
for i in range(7):
    g = -60 + 10 * i; y = ymap(g, -60, 10, 90, 470)
    d.line([(133, y), (140, y)], fill=INK, width=2)
    txt(d, 128, y, f"{g}", F_TICK, GRAY, "rm")
pts = []
for i in range(601):
    lf = 1 + i * 5 / 600; f = 10 ** lf
    g = -10 * math.log10(1 + (f / 1591.5) ** 2)
    pts.append((xmap(lf, 1, 6, 140, 930), ymap(g, -60, 10, 90, 470)))
d.line(pts, fill=BLUE, width=4)
xfc = xmap(math.log10(1591.5), 1, 6, 140, 930)
d.line([(xfc, 90), (xfc, 470)], fill=RED, width=2)
dot(d, xfc, ymap(-3, -60, 10, 90, 470), 6, RED)
txt(d, xfc + 12, 430, "fc = 1.59 kHz, −3 dB", F_SMALL, RED)
txt(d, 140, 530, "一阶低通：fc 后以 −20 dB/dec 下降；10fc 处约 −20 dB。", F_SMALL, GRAY)
save(img, "01/图01-04_一阶低通Bode.png")

# 02-02 diode I-V
img, d = canvas(1000, 640)
frame(d, 140, 90, 930, 470, "图 02-02  硅二极管与肖特基二极管正向特性", "正向电压 V_D / V", "电流 I / mA")
ticks_x(d, 140, 90, 930, 470, 0, 0.8, "{:.1f}")
ticks_y(d, 140, 90, 930, 470, 0, 30, "{:.0f}")
for Is, color, lab in [(1e-12, BLUE, "硅管"), (1e-8, GREEN, "肖特基")]:
    pts = []
    for i in range(401):
        v = i * 0.8 / 400
        cur = Is * (math.exp(v / 0.02585) - 1) * 1000
        if cur > 35:
            break
        pts.append((xmap(v, 0, 0.8, 140, 930), ymap(cur, 0, 30, 90, 470)))
    d.line(pts, fill=color, width=4)
txt(d, 700, 170, "硅管", F_SMALL, BLUE)
txt(d, 700, 200, "肖特基", F_SMALL, GREEN)
txt(d, 140, 530, "硅管约 0.65–0.75 V 导通；肖特基约 0.25–0.4 V。必须限流。", F_SMALL, GRAY)
save(img, "02/图02-02_二极管伏安特性.png")

print("part2 done")
