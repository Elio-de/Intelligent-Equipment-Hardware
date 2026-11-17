# -*- coding: utf-8 -*-
"""Build a readable DOCX compilation of the handbook (basic Markdown converter)."""
import re
from pathlib import Path

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

HB = Path(r"C:\DeepSeek_ Project\智能装备电子硬件学习手册")
OUT = HB / "90_附录" / "交付" / "智能装备电子硬件学习手册_v1.1.docx"
OUT.parent.mkdir(parents=True, exist_ok=True)

FILES = [
    "README.md",
    "学习路线与能力地图.md",
    "安全与实践须知.md",
    "维护记录.md",
    "完整章节目录.md",
    "01_电路基础与电子学数学/01A_直流电路与动态分析.md",
    "01_电路基础与电子学数学/01B_交流频域与噪声.md",
    "02_半导体器件与电子元器件/02A_半导体与晶体管.md",
    "02_半导体器件与电子元器件/02B_无源器件封装与选型.md",
    "03_模拟电子技术/03A_放大器与运放基础.md",
    "03_模拟电子技术/03B_滤波器反馈与噪声.md",
    "04_数字电子技术/04A_逻辑与时序基础.md",
    "04_数字电子技术/04B_ADC时序与接口.md",
    "05_传感器信号调理与数据采集/05_传感器信号调理与数据采集.md",
    "06_嵌入式硬件与微控制器/06_嵌入式硬件与微控制器.md",
    "07_电机执行器与功率驱动/07_电机执行器与功率驱动.md",
    "08_电源技术与电力电子/08_电源技术与电力电子.md",
    "09_工业通信与硬件接口/09_工业通信与硬件接口.md",
    "10_PCB设计EMC与可靠性/10_PCB设计EMC与可靠性.md",
    "11_电子测量实验与故障排查/11_电子测量实验与故障排查.md",
    "12_智能装备综合硬件系统/12_智能装备综合硬件系统.md",
    "13_参考资料Datasheet与术语表/13_参考资料Datasheet与术语表.md",
    "12_智能装备综合硬件系统/实验/00_基础实验手册.md",
    "12_智能装备综合硬件系统/项目/00_项目总览.md",
    "12_智能装备综合硬件系统/项目/项目1_传感器信号采集模块.md",
    "12_智能装备综合硬件系统/项目/项目2_STM32最小系统与接口板.md",
    "12_智能装备综合硬件系统/项目/项目3_MOSFET驱动与直流电机控制板.md",
    "12_智能装备综合硬件系统/项目/项目4_低压BUCK降压电源.md",
    "12_智能装备综合硬件系统/项目/项目5_多传感器采集与控制板.md",
    "12_智能装备综合硬件系统/项目/项目6_智能装备综合控制板.md",
    "12_智能装备综合硬件系统/案例/工程案例研究.md",
]


def set_font(run, name="微软雅黑", size=10.5, bold=None, italic=None):
    run.font.name = name
    run.font.size = Pt(size)
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic


def clean(s):
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    s = s.replace("**", "").replace("__", "")
    s = s.replace("`", "")
    s = re.sub(r"\$([^$]+)\$", lambda m: formula_text(m.group(1)), s)
    s = formula_text(s)
    return s.strip()


def formula_text(s):
    s = s.replace("\\times", "×").replace("\\approx", "≈").replace("\\le", "≤").replace("\\ge", "≥")
    s = s.replace("\\mu", "µ").replace("\\Omega", "Ω").replace("\\pi", "π").replace("\\pm", "±")
    s = s.replace("\\cdot", "·").replace("\\rightarrow", "→").replace("\\infty", "∞")
    s = re.sub(r"\\frac\{([^{}]+)\}\{([^{}]+)\}", r"(\1)/(\2)", s)
    s = re.sub(r"\\text\{([^{}]+)\}", r"\1", s)
    s = re.sub(r"\\[a-zA-Z]+", "", s)
    s = s.replace("\\\\", " ").replace("\\,", " ").replace("\\;", " ").replace("\\!", "")
    s = s.replace("\\", "")
    s = s.replace("{", "").replace("}", "").replace("&", "")
    return re.sub(r"\s+", " ", s).strip()


def add_page_number(paragraph):
    run = paragraph.add_run()
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    run._r.addnext(fld)


def add_toc(doc):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("目录")
    set_font(r, size=18, bold=True)
    note = doc.add_paragraph()
    note.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = note.add_run("在 Word 中右键此处 →“更新域”生成/刷新目录")
    set_font(r, size=9, italic=True)
    p = doc.add_paragraph()
    run = p.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = 'TOC \\o "1-3" \\h \\z \\u'
    sep = OxmlElement("w:fldChar")
    sep.set(qn("w:fldCharType"), "separate")
    text = OxmlElement("w:t")
    text.text = "右键“更新域”生成目录"
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.append(begin)
    run._r.append(instr)
    run._r.append(sep)
    run._r.append(text)
    run._r.append(end)
    doc.add_paragraph()


def add_table(doc, rows, base_dir):
    if not rows:
        return
    cols = max(len(r) for r in rows)
    table = doc.add_table(rows=len(rows), cols=cols)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(rows):
        for j in range(cols):
            cell = table.cell(i, j)
            cell.text = ""
            p = cell.paragraphs[0]
            txt = clean(row[j]) if j < len(row) else ""
            r = p.add_run(txt)
            set_font(r, size=8.5, bold=(i == 0))
            p.paragraph_format.space_after = Pt(0)
    doc.add_paragraph()


def add_image(doc, path, alt):
    try:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run()
        run.add_picture(str(path), width=Inches(6.2))
        cap = doc.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = cap.add_run(alt)
        set_font(r, size=9, italic=True, bold=False)
    except Exception as e:
        p = doc.add_paragraph()
        r = p.add_run(f"[图片缺失: {path.name}] {e}")
        set_font(r, size=9, italic=True)


doc = Document()
style = doc.styles["Normal"]
style.font.name = "微软雅黑"
style.font.size = Pt(10.5)
style._element.rPr.rFonts.set(qn("w:eastAsia"), "微软雅黑")
for s in ["Heading 1", "Heading 2", "Heading 3", "Title"]:
    try:
        st = doc.styles[s]
        st.font.name = "微软雅黑"
        st._element.rPr.rFonts.set(qn("w:eastAsia"), "微软雅黑")
    except Exception:
        pass

# cover
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("\n\n智能装备与系统专业\n电子硬件知识学习手册")
set_font(r, size=26, bold=True)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("文档版 v1.1.0")
set_font(r, size=16)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("2026-11-14")
set_font(r, size=12)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("说明：本 Word 版为阅读汇编，公式以文本近似显示；\n精确排版、链接与代码以 Markdown 源文件为准。\n工程验证（PCB/打样/实测/EMC）未完成。")
set_font(r, size=10, italic=True)

doc.add_page_break()
add_toc(doc)
doc.add_page_break()

for rel in FILES:
    path = HB / rel
    if not path.exists():
        continue
    lines = path.read_text(encoding="utf-8").splitlines()
    doc.add_page_break()
    i = 0
    para_buf = []

    def flush():
        if not para_buf:
            return
        text = " ".join(clean(x) for x in para_buf if clean(x))
        para_buf.clear()
        if not text:
            return
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.25
        r = p.add_run(text)
        set_font(r, size=10.5)

    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            flush()
            i += 1
            code = []
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.0
            r = p.add_run("\n".join(code))
            set_font(r, name="Consolas", size=8)
            continue
        if line.strip() == "$$":
            flush()
            i += 1
            buf = []
            while i < len(lines) and lines[i].strip() != "$$":
                buf.append(lines[i])
                i += 1
            i += 1
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(formula_text(" ".join(buf)))
            set_font(r, name="Cambria Math", size=10)
            continue
        if line.startswith("|"):
            flush()
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                raw = lines[i].strip().strip("|")
                cells = [c.strip() for c in raw.split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            add_table(doc, rows, path.parent)
            continue
        m = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", line.strip())
        if m:
            flush()
            alt, src = m.group(1), m.group(2)
            img = (path.parent / src).resolve()
            if img.exists():
                add_image(doc, img, alt)
            i += 1
            continue
        if line.startswith("# "):
            flush()
            h = doc.add_heading(clean(line[2:]), level=0)
            i += 1
            continue
        if line.startswith("## "):
            flush()
            doc.add_heading(clean(line[3:]), level=1)
            i += 1
            continue
        if line.startswith("### "):
            flush()
            doc.add_heading(clean(line[4:]), level=2)
            i += 1
            continue
        if line.startswith("#### "):
            flush()
            doc.add_heading(clean(line[5:]), level=3)
            i += 1
            continue
        if line.startswith("> "):
            flush()
            p = doc.add_paragraph()
            r = p.add_run(clean(line[2:]))
            set_font(r, size=9.5, italic=True)
            p.paragraph_format.left_indent = Inches(0.25)
            i += 1
            continue
        if re.match(r"^\s*[-*] ", line):
            flush()
            p = doc.add_paragraph(style="List Bullet")
            r = p.add_run(clean(re.sub(r"^\s*[-*] ", "", line)))
            set_font(r, size=10)
            i += 1
            continue
        if re.match(r"^\s*\d+\. ", line):
            flush()
            p = doc.add_paragraph(style="List Number")
            r = p.add_run(clean(re.sub(r"^\s*\d+\. ", "", line)))
            set_font(r, size=10)
            i += 1
            continue
        if line.strip() in ("---", "***"):
            flush()
            i += 1
            continue
        if not line.strip():
            flush()
            i += 1
            continue
        para_buf.append(line)
        i += 1
    flush()

# footer page number
section = doc.sections[0]
footer = section.footer
fp = footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
add_page_number(fp)

doc.save(OUT)
print("saved", OUT, "size", OUT.stat().st_size)
