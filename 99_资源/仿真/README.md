# 仿真文件说明

> 版本：v1.1.0  
> 日期：2026-11-14  
> 适用：第 01–04 章、项目 1/3/4  
> 语法：ngspice / LTspice 兼容的 SPICE 网表（`.cir`）  
> **状态：13 个网表均未运行验证；详见[运行状态](运行状态.md)。**

---

## 1. 怎么运行

### ngspice（命令行）

```bash
cd 99_资源/仿真/01
ngspice -b rc_step.cir
```

- `-b`：批处理模式，运行后退出。
- 输出默认在终端；如需波形，用 `ngspice` 交互模式，再 `plot v(out)`。
- 交流分析：`ngspice -b rc_ac.cir`，然后 `plot vdb(out)`、`plot ph(out)`。

### LTspice

1. 打开 LTspice → `File → Open`，选择 `.cir` 文件。
2. 直接 `Run`；若提示找不到模型，把 `.model` 行保留在网表内（本目录已内置简化模型）。
3. 波形窗口可加 `v(out)`、`v(in)`。

> 本环境未安装 ngspice/LTspice，上述网表**未做运行验证**；语法为通用 SPICE，首次运行如报错，优先检查模型名、节点名与 `.tran/.ac` 参数。欢迎把报错与修正记录到《项目执行与版本记录》的“仿真问题”一节。

---

## 2. 文件清单

| 文件 | 分析 | 关键预期 |
|---|---|---|
| `01/rc_step.cir` | `.tran` | τ=1 ms；5 ms 时 $v_{out}\approx3.28$ V |
| `01/rlc_series.cir` | `.tran` | ζ=0.25，约 15.4 kHz 振铃 |
| `01/rc_ac.cir` | `.ac` | $f_c\approx1.59$ kHz，之后 −20 dB/dec |
| `02/diode_iv.cir` | `.dc` | 1N4148 约 0.6–0.7 V 导通 |
| `02/bjt_switch.cir` | `.tran` | $V_{CE(sat)}<0.3$ V，$I_C\approx20$ mA |
| `02/mosfet_switch.cir` | `.tran` | 3.3 V 驱动下 $V_{DS}$ 与开关波形 |
| `03/opamp_noninverting.cir` | `.ac` | 增益 11，带宽受 E 源理想化限制 |
| `03/sallen_key.cir` | `.ac` | $f_0\approx1.07$ kHz，$Q\approx0.74$ |
| `03/comparator_hysteresis.cir` | `.dc` | 约 2.25 V / 3.25 V 两个阈值 |
| `04/adc_sample_rc.cir` | `.tran` | 10 kΩ 源阻抗 + 100 nF 的建立过程 |

---

## 3. 使用建议

1. **先手算，再仿真**：把预测值写在实验记录里，仿真只用于验证/找错。
2. **改一个参数，看一个结果**：例如把 `rc_step.cir` 的 R 从 10k 改成 100k，观察 τ 变 10 ms。
3. **不要迷信理想模型**：本目录的运放用理想 E 源，没有 GBW/失调/噪声；真实设计要换厂商模型。
4. **仿真与实测对照**：差异 >20% 时，先查元件实际值、探头、接地，再怀疑模型。

---

## 4. 待补

- [ ] 运放的厂商 SPICE 模型（OPA2188、INA333）。
- [ ] 二极管/ MOSFET 的厂商模型（1N4148、IRLZ44N）。
- [ ] 带开关电容的 ADC 采样保持模型。
- [ ] 数字逻辑的 XSPICE 模型或 Verilog-A。
