# -*- coding: utf-8 -*-
"""Timing and ADC figures."""
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
SHADE = (254, 226, 226)


def canvas(w=1000, h=640):
    img = Image.new("RGB", (w, h), WHITE)
    return img, ImageDraw.Draw(img)


def txt(d, x, y, s, font=F_LABEL, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)


def dot(d, x, y, r=5, color=INK):
    d.ellipse([x - r, y - r, x + r, y + r], fill=color)


def save(img, rel):
    p = BASE / rel
    img.save(p)
    print("wrote", p)


# ---------- timing ----------
img, d = canvas(1000, 640)
txt(d, 40, 25, "图 04-01  建立时间与保持时间（D 触发器）", F_TITLE)
x0, x1 = 140, 900
T = 10.0


def X(t):
    return x0 + (t / T) * (x1 - x0)


rows = {"CLK": 170, "D": 320, "Q": 470}
for name, y in rows.items():
    txt(d, 80, y - 12, name, F_LABEL, INK, "ra")
    d.line([(x0, y + 50), (x1, y + 50)], fill=(240, 240, 240), width=1)

# clock: high 0-1, low 1-2, ...
clk = []
for k in range(5):
    t = 2 * k
    clk += [(t, 0), (t, 1), (t + 1, 1), (t + 1, 0), (t + 2, 0)]
pts = [(X(t), rows["CLK"] + 50 - v * 50) for t, v in clk]
d.line(pts, fill=BLUE, width=3)

# D: 0 until 2, 1 from 2 to 6, 0 after 6
d.line([(X(0), rows["D"] + 50), (X(2), rows["D"] + 50)], fill=GREEN, width=3)
d.line([(X(2), rows["D"]), (X(6), rows["D"])], fill=GREEN, width=3)
d.line([(X(6), rows["D"] + 50), (X(10), rows["D"] + 50)], fill=GREEN, width=3)
d.line([(X(2), rows["D"] + 50), (X(2), rows["D"])], fill=GREEN, width=3)
d.line([(X(6), rows["D"]), (X(6), rows["D"] + 50)], fill=GREEN, width=3)

# Q: samples at t=0,2,4,6,8
q = [(0, 0), (2, 1), (6, 0)]
d.line([(X(0), rows["Q"] + 50), (X(2), rows["Q"] + 50)], fill=RED, width=3)
d.line([(X(2), rows["Q"]), (X(6), rows["Q"])], fill=RED, width=3)
d.line([(X(6), rows["Q"] + 50), (X(10), rows["Q"] + 50)], fill=RED, width=3)
for t in [2, 6]:
    d.line([(X(t), rows["Q"] + 50), (X(t), rows["Q"])], fill=RED, width=3)

# setup/hold window around edge t=4
for t in [3.6, 4.0, 4.4]:
    d.line([(X(t), 120), (X(t), 540)], fill=GRAY, width=1, )
d.rectangle([X(3.6), 150, X(4.0), 540], fill=SHADE)
d.rectangle([X(4.0), 150, X(4.4), 540], fill=(219, 234, 254))
txt(d, (X(3.6) + X(4.0)) / 2, 120, "tsu", F_SMALL, RED, "mm")
txt(d, (X(4.0) + X(4.4)) / 2, 120, "th", F_SMALL, BLUE, "mm")
dot(d, X(4.0), rows["CLK"] + 50, 5, RED)
txt(d, X(4.0), 575, "↑ 采样沿", F_SMALL, RED, "ma")
txt(d, 140, 610, "D 在 tsu 之前必须稳定，在 th 之后才能变化；违反 → 亚稳态。", F_SMALL, GRAY)
save(img, "04/图04-01_建立保持时序.png")

# ---------- ADC quantization + aliasing ----------
img, d = canvas(1000, 640)
txt(d, 40, 25, "图 04-02  ADC 量化与采样混叠", F_TITLE)


def frame2(x0, y0, x1, y1, title):
    d.rectangle([x0, y0, x1, y1], outline=INK, width=2)
    txt(d, (x0 + x1) / 2, y0 - 32, title, F_LABEL, INK, "mm")


# left: 4-bit quantization
lx0, ly0, lx1, ly1 = 90, 130, 470, 470
frame2(lx0, ly0, lx1, ly1, "(a) 4 位量化：LSB = 206 mV")
for i in range(5):
    x = lx0 + (lx1 - lx0) * i / 4
    d.line([(x, ly1), (x, ly1 + 6)], fill=INK)
    txt(d, x, ly1 + 10, f"{i*0.825:.2f}", F_TICK, GRAY, "ma")
for i in range(5):
    y = ly1 - (ly1 - ly0) * i / 4
    d.line([(lx0 - 6, y), (lx0, y)], fill=INK)
    txt(d, lx0 - 10, y, f"{i*5}", F_TICK, GRAY, "rm")
# ideal line
d.line([(lx0, ly1), (lx1, ly0)], fill=GRAY, width=2)
# staircase: 16 levels over 0..3.3
levels = 16
for k in range(levels):
    vin0 = k * 3.3 / levels
    vin1 = (k + 1) * 3.3 / levels
    y = ly1 - (ly1 - ly0) * (k + 0.5) / levels
    d.line([(lx0 + (lx1 - lx0) * vin0 / 3.3, y), (lx0 + (lx1 - lx0) * vin1 / 3.3, y)], fill=BLUE, width=3)
    d.line([(lx0 + (lx1 - lx0) * vin0 / 3.3, y), (lx0 + (lx1 - lx0) * vin0 / 3.3, ly1 - (ly1 - ly0) * (k - 0.5) / levels if k else ly1)], fill=BLUE, width=2)
txt(d, lx0, ly1 + 45, "输入电压 / V", F_SMALL, GRAY, "la")
txt(d, lx0 - 50, ly0 - 10, "码值", F_SMALL, GRAY, "ra")

# right: aliasing 9 kHz sampled at 10 kSPS
rx0, ry0, rx1, ry1 = 550, 130, 940, 470
frame2(rx0, ry0, rx1, ry1, "(b) 9 kHz 以 10 kSPS 采样 → 1 kHz 假信号")
for i in range(6):
    x = rx0 + (rx1 - rx0) * i / 5
    d.line([(x, ry1), (x, ry1 + 6)], fill=INK)
    txt(d, x, ry1 + 10, f"{i*0.2:.1f}", F_TICK, GRAY, "ma")
d.line([(rx0, (ry0 + ry1) / 2), (rx1, (ry0 + ry1) / 2)], fill=(200, 200, 200), width=1)
pts = []
for i in range(501):
    t = i * 1e-3 / 500
    v = math.sin(2 * math.pi * 9000 * t)
    pts.append((rx0 + (rx1 - rx0) * t / 1e-3, (ry0 + ry1) / 2 - v * (ry1 - ry0) * 0.38))
d.line(pts, fill=BLUE, width=2)
samp = []
for i in range(11):
    t = i * 1e-4
    v = math.sin(2 * math.pi * 9000 * t)
    x = rx0 + (rx1 - rx0) * t / 1e-3
    y = (ry0 + ry1) / 2 - v * (ry1 - ry0) * 0.38
    samp.append((x, y))
d.line(samp, fill=RED, width=3)
for x, y in samp:
    dot(d, x, y, 5, RED)
txt(d, rx0, ry1 + 45, "时间 / ms", F_SMALL, GRAY, "la")
txt(d, rx1 - 5, ry0 + 20, "蓝：9 kHz 原信号", F_SMALL, BLUE, "ra")
txt(d, rx1 - 5, ry0 + 44, "红：采样点连成 1 kHz", F_SMALL, RED, "ra")
txt(d, 90, 570, "混叠频率 |9k−10k|=1 kHz；抗混叠滤波器必须在采样前把 9 kHz 衰减掉。", F_SMALL, GRAY)
save(img, "04/图04-02_ADC量化与混叠.png")
print("done")
