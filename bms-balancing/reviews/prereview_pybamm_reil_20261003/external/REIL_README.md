# Multi-Objective Optimization for Lithium-Ion Battery Degradation Diagnostics

Code and data repository for the journal article **"Benchmarking half-cell model fitting approaches for lithium-ion battery degradation diagnostics"**, published in *eTransportation*.

## Overview

This repository benchmarks single- and multi-objective optimization approaches for fitting half-cell (electrode-level) models to full-cell voltage data, in order to diagnose lithium-ion battery degradation modes:

- **LAM** (loss of active material) at the positive electrode (PE/LFP) and negative electrode (NE/Graphite)
- **LLI** (loss of lithium inventory)

Half-cell PE/NE voltage curves are fit to full-cell experimental data by optimizing electrode mass-scaling and capacity-offset parameters. Optimization is performed with a genetic algorithm (GA) for single-objective cases and NSGA-II/NSGA-III for multi-objective cases (2–4 objectives combining end-point error, QV curve error, dV/dQ peak error, and dV/dQ curve error).

## Repository Contents

| File / Folder | Description |
|---|---|
| `Benchmarking_LFP_final.ipynb` | Main notebook: loads half-cell/full-cell data, runs the optimization cases, and generates all figures. |
| `util_LFP.py` | Core library: data loading/parsing, the multi-objective loss function, `pymoo` problem definitions (GA/NSGA2/NSGA3), and plotting utilities. |
| `LFP_Data.xlsx` | Experimental half-cell and full-cell voltage/capacity data (multiple sheets, one per cell/test condition). |
| `results/` | Pickled optimization outputs (`LFP_Models_R1.pkl`, `LFP_Results_R1.pkl`, `LFP_hps_R1.pkl`) and generated figure PDFs. |
| `LICENSE` | MIT License. |

## Installation

Requires Python 3.9+ with the following packages:

```bash
pip install numpy pandas scipy matplotlib seaborn pymoo openpyxl
```

## Usage

1. Ensure `LFP_Data.xlsx` is in the repository root (the notebook reads it via `data_file = 'LFP_Data.xlsx'`).
2. Open and run `Benchmarking_LFP_final.ipynb`:
   - **Process data** — loads half-cell PE/NE curves and full-cell data for each degradation case.
   - **Run MOO** — runs the optimization (`run_optimization`) for six single/multi-objective case combinations (`case_selection`) across all cells, then extracts health parameters (mass factors and LII) via `extract_health_parameter`.
   - **Visualization** — reloads results from `results/` and reproduces the QV/dV-dQ comparison plots, health-parameter violin plots, and Pareto-front panels used in the paper.

Intermediate results are cached as pickle files in `results/` so the visualization section can be re-run without repeating the (slower) optimization step.

## Citation

If you use this code or data, please cite:

> T. Li, Y. Zhang, B. Nowacki, S. Navidi, T. Schmitt, S. Hu, C. Hu, "Benchmarking half-cell model fitting approaches for lithium-ion battery degradation diagnostics," *eTransportation*, vol. 29, p. 100593, 2026. [https://doi.org/10.1016/j.etran.2026.100593](https://doi.org/10.1016/j.etran.2026.100593)

```bibtex
@article{li2026benchmarking,
  title   = {Benchmarking half-cell model fitting approaches for lithium-ion battery degradation diagnostics},
  author  = {Li, Tingkai and Zhang, Yifan and Nowacki, Benjamin and Navidi, Sina and Schmitt, Thomas and Hu, Shan and Hu, Chao},
  journal = {eTransportation},
  volume  = {29},
  pages   = {100593},
  year    = {2026},
  doi     = {10.1016/j.etran.2026.100593}
}
```

The experimental dataset (`LFP_Data.xlsx`) is the **ISU-UConn LFP/Graphite Emulated Degradation Dataset**, published separately (CC BY 4.0):

> Zhang, Yifan; Li, Tingkai; Hu, Shan; and Hu, Chao, "ISU-UConn LFP/Graphite Emulated Degradation Dataset" (2026). *REIL Datasets*. 6. [https://digitalcommons.lib.uconn.edu/reil_datasets/6/](https://digitalcommons.lib.uconn.edu/reil_datasets/6/)

```bibtex
@misc{zhang2026dataset,
  title  = {ISU-UConn LFP/Graphite Emulated Degradation Dataset},
  author = {Zhang, Yifan and Li, Tingkai and Hu, Shan and Hu, Chao},
  year   = {2026},
  note   = {REIL Datasets. 6},
  url    = {https://digitalcommons.lib.uconn.edu/reil_datasets/6/}
}
```

## License

MIT License — see [LICENSE](LICENSE) for details.
