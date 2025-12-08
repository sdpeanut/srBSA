# srBSA-seq 多算法一体化工具使用说明

本工具集成了多种 **srBSA-seq 定位算法**，通过一个统一入口脚本调用不同算法，对同一 VCF 数据进行批量分析，自动输出各类图形和 QTL 区间表。

当前集成的算法：

- `DeltaSNP`：ΔSNP-index + Monte-Carlo 置信区间  
- `dP`：Δ-Probability / dP  
- `ED4`：Euclidean Distance⁴  
- `FST`：Hudson F_ST & π 多样性  
- `Gprime`：QTLseqr / Magwene 风格 G′  
- `HMM`：ΔSNP 平滑 + 高斯 HMM 分段 + QTL 区间  
- `LOD`：MULTIPOOL 风格窗口 LOD + QTL 区间  

---

## 一、目录结构

推荐工程目录结构：

```text
BSA_suite/
├── bsa_suite.py          # 统一入口脚本
├── bsa_env_config.py     # 统一参数 & 环境变量配置
├── data/                 # 输入数据（VCF）
│   └── filtered_snps.dp10_all.vcf.gz
└── algorithms/           # 各算法子程序
    ├── __init__.py       # 可留空
    ├── DeltaSNP.py       # ΔSNP-index + CI
    ├── DP.py             # dP 窗口 + QTL
    ├── ED4.py            # ED⁴ + 阈值
    ├── FST.py            # FST & π
    ├── Gprime.py         # G′
    ├── HMM.py            # HMM 分段 + QTL
    └── LOD.py            # 窗口 LOD + QTL
```

各算法运行后，会在 `result/` 目录下生成对应子目录，例如：

```text
result/
├── DeltaSNP/
├── dP/
├── ED4Final/
├── FST/      
├── Gprime/
├── HMM/
└── LOD/
```

---

## 二、运行环境与依赖

建议使用 **Python 3.8+**，并在独立 conda 环境中安装依赖：

```bash
conda create -n bsa_seq python=3.10
conda activate bsa_seq

pip install pysam pandas numpy matplotlib tqdm scipy hmmlearn cyvcf2
```

---

## 三、最简快速使用

在工程根目录（有 `bsa_suite.py` 的目录）执行：

```bash
python bsa_suite.py   --vcf data/filtered_snps.dp10_all.vcf.gz   --high-pool RED   --parent1 TIF   --parent2 NNP   --window-bp 1000000   --step-bp   100000   --methods   all
```

参数含义：

- `--vcf`：输入 VCF 文件路径  
- `--high-pool`：高性状池样本名（对应 VCF 中 sample ID）  
- `--parent1` / `--parent2`：两个亲本样本名  
- `--window-bp`：滑动窗口大小（bp）  
- `--step-bp`：窗口步长（bp）  
- `--methods all`：依次运行所有算法

运行结束后，所有结果存放在 `result/` 目录下各算法对应的子目录中。

---

## 四、交互式菜单模式

在工程根目录执行：

```bash
python bsa_suite.py
```

进入交互式菜单，例如：

```text
======================================================
    srBSA-seq 一体化工具 (srBSA.py)
======================================================
可用分析方法：
    1. delta   —— ΔSNP-index + Monte-Carlo 置信区间
    2. dP      —— Δ-Probability / dP 窗口 + QTL 区间
    3. ed4     —— ED⁴ 窗口 + 置换阈值
    4. fst     —— Hudson FST & π
    5. gprime  —— QTLseqr 风格 G′
    6. hmm     —— ΔSNP 平滑 + HMM 分段 + QTL 区间
    7. lod     —— 窗口 LOD + QTL 区间
    8. all     —— 依次运行上述所有方法
    9. quit    —— 退出
```

在提示符下输入：

- `1` 或 `delta`：只运行 ΔSNP  
- `5` 或 `gprime`：只运行 Gprime  
- `8` 或 `all`：运行全部方法  
- `9` / `quit`：退出  

如未通过命令行指定 `--vcf` 等参数，则使用 `bsa_env_config.py` 中默认设置（默认 VCF 为 `data/filtered_snps.dp10_all.vcf.gz`）。

---

## 五、命令行参数说明

`bsa_suite.py` 支持通过命令行统一设置参数，这些参数会写入环境变量 `BSA_...`，由各算法脚本读取。

常用参数：

```text
--vcf              VCF 文件路径 (BSA_VCF_FILE)
--high-pool        高性状池样本名 (BSA_HIGH_POOL)
--parent1          亲本1样本名 (BSA_PARENT1)
--parent2          亲本2样本名 (BSA_PARENT2)

--window-bp        滑动窗口大小 bp (BSA_WINDOW_BP)
--step-bp          步长 bp (BSA_STEP_BP)
--min-dp-snp       单 SNP 最小总深度 (BSA_MIN_DP_SNP)
--min-sites        窗口内最少 SNP 数 (BSA_MIN_SITES)
--min-dp-win       窗口总深度阈值 (BSA_MIN_DP_WIN)

--n-perm           置换次数 (BSA_N_PERM)
--max-dp-perm      置换时单位点最大深度 (BSA_MAX_DP_PERM)

--ed-alpha         ED⁴ 阈值分位，例如 0.999 (BSA_ED_ALPHA)
--dp-thr-q         dP |dP| 分位阈值，如 0.99 (BSA_DP_THR_Q)
--fst-thr-fst-q    FST 分位阈值 (BSA_FST_THR_FST_Q)
--fst-thr-pi-q     π 的极低分位 (BSA_FST_THR_PI_Q)
--lod-thr-q        LOD 分位阈值 (BSA_LOD_THR_Q)

--hmm-init-p0      HMM 初始背景状态概率 (BSA_HMM_INIT_P0)
--hmm-self-p       HMM 自循环概率 (BSA_HMM_SELF_P)
--hmm-thresholds   HMM 阈值列表，如 "-0.3,0.3" (BSA_HMM_THRESHOLDS)

--g-ed-threshold   Gprime 中 ED 平滑曲线阈值 (BSA_G_ED_THRESHOLD)
--g-fdr            Gprime 中 G′ FDR 阈值 (BSA_G_FDR)

--methods          要运行的方法列表（逗号分隔）：
                   delta, dP, ed4, fst, gprime, hmm, lod, all
```

示例（只运行 ΔSNP + ED4 + LOD）：

```bash
python bsa_suite.py   --vcf data/filtered_snps.dp10_all.vcf.gz   --high-pool RED   --parent1 TIF   --parent2 NNP   --window-bp 1000000   --step-bp   100000   --min-dp-snp 10   --methods delta,ed4,lod
```

---

## 六、环境变量方式配置（可选）

也可通过环境变量配置参数，例如：

```bash
export BSA_VCF_FILE=data/filtered_snps.dp10_all.vcf.gz
export BSA_HIGH_POOL=RED
export BSA_PARENT1=TIF
export BSA_PARENT2=NNP
export BSA_WINDOW_BP=1000000
export BSA_STEP_BP=100000
export BSA_DP_THR_Q=0.99
export BSA_LOD_THR_Q=0.995

python bsa_suite.py --methods all
```

未在命令行显式给定的参数，会从对应 `BSA_...` 环境变量中读取。

---

## 七、各算法输出概览

### 1. DeltaSNP（`algorithms/DeltaSNP.py` → `result/DeltaSNP/`）

- `*_deltaSNP_perSNP.csv`：逐 SNP ΔSNP-index  
- `*_deltaSNP_window_allChr.csv`：窗口 ΔSNP 平均值  
- `*_ChrXX_deltaSNP_window.png`：每染色体 ΔSNP 窗口曲线图  
- `*_deltaSNP_window_allChr.png`：整基因组拼接图  
- `*_deltaSNP_window_grid.png`：4×5 网格图  

### 2. dP（`algorithms/DP.py` → `result/dP/`）

- `*_dP_perSNP.csv`：逐 SNP dP  
- `*_ChrXX_dP_window.csv`：每染色体 dP 窗口  
- `*_dP_window_allChr.csv`：整基因组 dP 窗口  
- `*_ChrXX_dP_window.pdf`：单染色体 dP 曲线 + 阈值  
- `*_dP_window_allChr.png`：整基因组 dP + 阈值  
- `*_dP_window_grid.png`：4×5 网格图  
- `*_dP_QTL_segments.csv`：基于整基因组 |dP| 分位阈值的 QTL 区间  

### 3. ED4（`algorithms/ED4.py` → `result/ED4Final/`）

- `*_ED4_raw.csv`：逐位点 ED⁴  
- `*_ED4_window_allChr.csv`：窗口 ED⁴ 平滑结果  
- 若脚本中开启绘图：每染色体 PDF、整基因组 PNG、网格 PNG  
- 当设置 `ED_ALPHA`（例如 0.999）时，会输出 ED⁴ 阈值线并用于 QTL 筛选

### 4. FST（`algorithms/FST.py` → `result/PopGen/`）

- `*_ChrXX_popgen_window.csv`：每窗 FST / π_high / π_low  
- `*_fst_window_allChr.png`：整基因组 FST 拼接图  
- `*_fst_window_grid.png`：4×5 FST 网格图  
- `*_ChrXX_popgen_window.pdf`：单染色体 FST + π_high + π_low 曲线  

### 5. Gprime（`algorithms/Gprime.py` → `result/Gprime/`）

- `*_Gprime_raw.csv`：原始 ΔSNP / ED 等  
- `*_Gprime_smoothed.csv`：平滑后的 ΔSNP / ED  
- `*_Gprime_withG.csv`：增加 G / G′  
- `*_DeltaSNP_allChr.png`：ΔSNP 平滑曲线图  
- `*_ED_allChr.png`：ED 平滑曲线 + 阈值  
- `*_Gprime_allChr.png`：G′ 曲线 + χ²/FDR 阈值  

### 6. HMM（`algorithms/HMM.py` → `result/HMM/`）

- `*_deltaSNP_smoothed_allChr.csv`：滑窗 ΔSNP 结果（若不存在会自动生成）  
- `*_HMM_windows.csv`：窗口 ΔSNP 中心化值 + HMM STATE  
- `*_HMM_segments_all.csv`：STATE=0/1 连续区段信息  
- `*_HMM_QTL_segments.csv`：结合 STATE 和阈值过滤后的 QTL 区间  
- `*_ChrXX_HMM_delta.pdf`：单染色体 ΔSNP + 区段背景 + 阈值线  
- `*_HMM_delta_allChr.png`：整基因组 ΔSNP + 阈值线  

### 7. LOD（`algorithms/LOD.py` → `result/LOD/`）

- `*_lod_window_allChr.csv`：窗口 LOD 统计  
- `*_lod_QTL_segments.csv`：基于 LOD 分位阈值合并的 QTL 区间  
- `*_ChrXX_lod_window.pdf`：单染色体 LOD 曲线 + 阈值  
- `*_lod_window_allChr.png`：整基因组 LOD 拼接图  
- `*_lod_window_grid.png`：4×5 LOD 网格图  

---

## 八、常见问题与调参建议

1. **窗口大小怎么选？**  
   - 推荐初始：`WINDOW_BP = 1,000,000`，`STEP_BP = 100,000`  
   - 若 QTL 区域较尖锐，可减小窗口（如 500 kb），提升定位精度，但噪声会略增。

2. **分位阈值如何设置？**  
   - `dP / LOD / FST`：可分别测试 0.95、0.99、0.995 等分位数，看 QTL 是否稳定存在。  
   - `HMM_THRESHOLDS`：可从 ΔSNP = ±0.25 或 ±0.3 开始，根据经验微调。

3. **输出文件找不到？**  
   - 确认运行时当前目录是包含 `bsa_suite.py` 的根目录；  
   - 所有结果均位于 `result/` 子目录中，各算法有独立子文件夹。

4. **某个算法报错中断？**  
   - 入口脚本在某个方法出错时会询问是否继续后续方法；  
   - 建议先单独调试该算法，例如：  
     ```bash
     python bsa_suite.py --methods lod --vcf data/xxx.vcf.gz ...
     ```
