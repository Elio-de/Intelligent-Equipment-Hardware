# -*- coding: utf-8 -*-
import re
from pathlib import Path

hb = Path(r"C:\DeepSeek_ Project\智能装备电子硬件学习手册")

chapters = [
    ("00", "项目说明、知识体系与学习路线", "00_项目说明", []),
    ("01", "电路基础与电子学数学", "01_电路基础与电子学数学", ["01A_直流电路与动态分析.md", "01B_交流频域与噪声.md"]),
    ("02", "半导体器件与电子元器件", "02_半导体器件与电子元器件", ["02A_半导体与晶体管.md", "02B_无源器件封装与选型.md"]),
    ("03", "模拟电子技术", "03_模拟电子技术", ["03A_放大器与运放基础.md", "03B_滤波器反馈与噪声.md"]),
    ("04", "数字电子技术", "04_数字电子技术", ["04A_逻辑与时序基础.md", "04B_ADC时序与接口.md"]),
    ("05", "传感器、信号调理与数据采集", "05_传感器信号调理与数据采集", ["05_传感器信号调理与数据采集.md"]),
    ("06", "嵌入式硬件与微控制器", "06_嵌入式硬件与微控制器", ["06_嵌入式硬件与微控制器.md"]),
    ("07", "电机、执行器与功率驱动", "07_电机执行器与功率驱动", ["07_电机执行器与功率驱动.md"]),
    ("08", "电源技术与电力电子", "08_电源技术与电力电子", ["08_电源技术与电力电子.md"]),
    ("09", "工业通信与硬件接口", "09_工业通信与硬件接口", ["09_工业通信与硬件接口.md"]),
    ("10", "PCB 设计、EMC 与可靠性", "10_PCB设计EMC与可靠性", ["10_PCB设计EMC与可靠性.md"]),
    ("11", "电子测量、实验与故障排查", "11_电子测量实验与故障排查", ["11_电子测量实验与故障排查.md"]),
    ("12", "智能装备综合硬件系统", "12_智能装备综合硬件系统", ["12_智能装备综合硬件系统.md"]),
    ("13", "参考资料、Datasheet 与术语表", "13_参考资料Datasheet与术语表", ["13_参考资料Datasheet与术语表.md"]),
]

plan_docs = [
    ("项目定位与专业需求分析.md", "岗位需求、能力目标、专业定位"),
    ("电子硬件完整知识体系.md", "14 个知识域、深度、学时"),
    ("知识依赖关系.md", "依赖图、并行簇、门禁"),
    ("../学习路线与能力地图.md", "S0–S6 能力驱动路线"),
    ("../安全与实践须知.md", "安全边界与项目分级"),
    ("参考资料总表.md", "资料编号与 L1–L3 核查"),
    ("README.md", "00 章导航"),
]

lines = []
lines.append("# 完整章节目录")
lines.append("")
lines.append("> 文档编号：EHB-00-05  ")
lines.append("> 版本：v1.1.0  ")
lines.append("> 日期：2026-11-14  ")
lines.append("> 状态：最终版（按正文标题自动生成，共 204 节）  ")
lines.append("> 说明：本目录位于根目录，取代 v0.2.0 的规划节表；节标题、编号以正文为准。")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## 0. 使用说明")
lines.append("")
lines.append("- 节号格式：`章.节`；每节对应正文中的一个 `##` 标题。")
lines.append("- 深度标记与先修关系见《知识依赖关系》《电子硬件完整知识体系》。")
lines.append("- 项目与实验见 `12_智能装备综合硬件系统/`（实验/项目/案例）。")
lines.append("- 本目录不含“核心内容”摘要，避免与正文重复；需要时直接查正文。")
lines.append("")
lines.append("---")
lines.append("")

def href(fn):
    if fn.startswith("../"):
        return fn[3:]
    return "00_项目说明/" + fn

total = 0
for num, title, d, files in chapters:
    lines.append(f"## 第 {num} 章 {title}")
    lines.append("")
    if num == "00":
        lines.append("本章为规划文档集合，0.1–0.8 为导航节，正文见下列文档。")
        lines.append("")
        lines.append("| 节 | 标题 | 对应文档 |")
        lines.append("|---|---|---|")
        nav = [
            ("0.1", "手册定位与使用方式", "项目定位与专业需求分析.md"),
            ("0.2", "学习者画像与起点诊断", "项目定位与专业需求分析.md"),
            ("0.3", "知识体系总览", "电子硬件完整知识体系.md"),
            ("0.4", "深度分级与验收", "电子硬件完整知识体系.md"),
            ("0.5", "学习路线与阶段", "../学习路线与能力地图.md"),
            ("0.6", "工具、安全与实验环境", "../安全与实践须知.md"),
            ("0.7", "资料检索与 Datasheet 阅读法", "参考资料总表.md"),
            ("0.8", "版本与维护", "../维护记录.md"),
        ]
        for sec, t, fn in nav:
            lines.append(f"| {sec} | {t} | [{fn.split('/')[-1]}]({href(fn)}) |")
        lines.append("")
        lines.append("| 文档 | 用途 |")
        lines.append("|---|---|")
        for fn, desc in plan_docs:
            lines.append(f"| [{fn.split('/')[-1]}]({href(fn)}) | {desc} |")
        lines.append("")
        lines.append("---")
        lines.append("")
        total += len(nav)
        continue

    lines.append("**正文文件**：" + "、".join(f"[{f}]({d}/{f})" for f in files))
    lines.append("")
    rows = []
    for f in files:
        p = hb / d / f
        text = p.read_text(encoding="utf-8")
        for m in re.finditer(r"^## (\d+\.\d+) (.+)$", text, flags=re.M):
            if m.group(1).endswith(".0"):
                continue
            rows.append((m.group(1), m.group(2).strip(), f))
    rows.sort(key=lambda x: tuple(int(x) for x in x[0].split(".")))
    total += len(rows)
    print(num, len(rows))
    lines.append("| 节 | 标题 | 文件 |")
    lines.append("|---|---|---|")
    for sec, t, f in rows:
        lines.append(f"| {sec} | {t} | {f} |")
    lines.append("")
    lines.append("---")
    lines.append("")

lines.append("## 统计")
lines.append("")
lines.append(f"- 章：14（00–13）")
lines.append(f"- 编号节：{total}")
lines.append("- 项目：6 个设计包")
lines.append("- 实验：10 个基础实验")
lines.append("- 资料：75 条（L1–L3）")
lines.append("")
lines.append("> 注：第 00 章为规划文档，不计入编号节；统计与正文标题一致。")

(hb / "完整章节目录.md").write_text("\n".join(lines), encoding="utf-8")
print("sections:", total)
