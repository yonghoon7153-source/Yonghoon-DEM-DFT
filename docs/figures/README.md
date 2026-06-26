# Figure 1 — DEM-driven multi-physics network solver pipeline

Two parallel implementations of the same paper figure. Pick the one that fits
your workflow:

## Option A: Python matplotlib (immediate PNG/PDF)

```bash
python3 scripts/figure1_panels.py
# → docs/figures/figure1_panel_d.{png,pdf}
# → docs/figures/figure1_panel_e.{png,pdf}
# → docs/figures/figure1_panel_f.{png,pdf}
```

Generates the schematic panels (d, e, f) as standalone images. Panels (a)
DEM render, (b) contact network, and (c) resistor network must come from
your existing DEM/network visualization output (paste them into the final
composite).

Requirements: `pip install matplotlib numpy`

Each output file is rendered at 300 dpi with embedded TrueType fonts so
PDFs are editable in Illustrator.

## Option B: TikZ / LaTeX (paper-grade, fully editable)

```bash
cd docs/figures
pdflatex figure1.tex
# → figure1.pdf
```

Single-file LaTeX standalone; everything is vector. Panels (a–c) currently
contain `[insert ... render here]` placeholders — replace each with
`\includegraphics{your_render.png}` once your DEM renders are ready.

To embed the figure in the main paper:
```latex
\usepackage{tikz}
\usetikzlibrary{positioning, shapes.geometric, arrows.meta, ...}
\input{figures/figure1_body.tex}  % extracted figure environment
```

## Why two implementations?

- **matplotlib**: fast preview, easy data integration (you can re-plot panel
  (e) using actual DEM contact-network data via the same script).
- **TikZ**: paper submission. Vector, font-embedded, no rendering artefacts,
  symbol-perfect (no Korean OCR glitches like `흐 훌물질` or `f_ronan`).

Use matplotlib while iterating, switch to TikZ for journal submission.

## Customising

### Colour palette
Both implementations share the same colour tokens. Edit:
- matplotlib: top of `scripts/figure1_panels.py` (`COL_AM_P`, `COL_SE`, …)
- TikZ: top of `figure1.tex` (`\definecolor{cAMP}{HTML}{3a3a3a}` …)

### Per-panel re-render (matplotlib only)
```bash
python3 scripts/figure1_panels.py --panel d  # only R-split
python3 scripts/figure1_panels.py --panel e  # only 3-channel
python3 scripts/figure1_panels.py --panel f  # only flowchart
```

### Caption (paper LaTeX form)

```latex
\begin{figure}[t]
  \centering
  \includegraphics[width=\linewidth]{figures/figure1.pdf}
  \caption{Schematic of the DEM-driven multi-physics network solver
    pipeline used in this work.
    \textbf{(a)} DEM-generated cathode microstructure with bimodal active
    material (AM\_P, polycrystalline NCM811, D12, $\sigma_{\rm grain} = 50$
    mS/cm; AM\_S, single-crystal NCM811, D4) and solid electrolyte (SE,
    LPSCl, D1, $\sigma_{\rm grain} = 3$ mS/cm).
    \textbf{(b)} Contact network color-coded by phase pair (SE-SE for
    $\sigma_{\rm ionic}$; AM-SE for ionic + interface; AM-AM for
    $\sigma_{\rm e}$).
    \textbf{(c)} Equivalent Kirchhoff resistor network solved as sparse
    linear system $\mathbf{Lx}=\mathbf{b}$.
    \textbf{(d)} Per-edge resistance decomposed into bulk ($R_{\rm bulk}$,
    internal) and constriction ($R_{\rm constriction}$, Holm 1967)
    components.
    \textbf{(e)} Three parallel circuits ($\sigma_{\rm ionic}$,
    $\sigma_{\rm e}$, $\kappa$) extracted from phase-specific contact
    subsets.
    \textbf{(f)} Stage E correction pipeline: per-contact Lawn 1998
    fracture factor $f_r$, combined with Cronau 2022 / Trevisanello 2021
    / Wang 2022 grain-level $\sigma$ corrections; modified resistance
    $R' = (R_{\rm bulk} + R_{\rm constriction})/f_r$; sanity-checked
    through 7-Layer defense (git commits logged for reproducibility) with
    Bruggeman-weighted-mean EMT fallback when the solver is numerically
    unstable.}
  \label{fig:network-solver-pipeline}
\end{figure}
```
