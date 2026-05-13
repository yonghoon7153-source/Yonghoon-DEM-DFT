# Paper draft — ASSB Stage E network solver

## Quick wget (single-command download)

```bash
BR="claude/stagewise-fracture-solver-3VvPg"
RAW="https://raw.githubusercontent.com/yonghoon7153-source/Yonghoon-DEM-DFT/$BR"

# Paper source + bibliography + matplotlib panel figure
wget "$RAW/docs/paper/main.tex"
wget "$RAW/docs/paper/refs.bib"
wget "$RAW/docs/figures/figure1_panel_e.pdf"   # default placeholder figure
# OR drop your own finalised image as ./figure1.png (auto-detected)
```

## Compile

```bash
pdflatex main.tex
bibtex   main
pdflatex main.tex
pdflatex main.tex
# → main.pdf
```

## Figure inclusion

`main.tex` references the matplotlib panels we generated:
- `../figures/figure1_panel_e.pdf` (currently used as Figure 1 placeholder)

To switch to your finalized composite figure (the LLM-generated one),
edit the `\includegraphics{...}` line inside the `figure*` environment
in `main.tex`.

## Section status (2026-05-13 update)

| Section | Status | Page est. |
|---|---|---|
| Abstract | Draft (needs final numbers) | 1 |
| 1. Introduction | Filled (porosity contribution added) | 1.5 – 2 |
| 2. Methodology | Filled (Fig 1 leading) | 3 |
| 3. Stage E corrections | Filled | 1 – 1.5 |
| 4. 7-Layer defence | Filled (commits cited) | 1.5 – 2 |
| 5. Results | Filled — §5.4 Section-7 heatmap, §5.5 strict-physics porosity 82-case validation added | 3 – 4 |
| 6. Discussion | Filled — two-mechanism wave-shape, no-overfit rationale, 3 future-work items | 1 – 2 |
| 7. Conclusion | Filled (porosity integrated) | 0.5 |

All `[Placeholder --- N pages]` markers in `main.tex` have been cleared
or replaced with prose. Section-by-section review for tone / brevity
is still recommended.

## New figures (drop next to main.tex before compiling)

| File | Generator | Referenced by |
|---|---|---|
| `section7_design_rules.png` | `scripts/plot_section7_design_rules.py` | Fig. \ref{fig:section7-heatmap} |
| `porosity_4panel.png`       | `scripts/plot_porosity_4panel.py`     | Fig. \ref{fig:porosity-validation} |

Both figures use `\IfFileExists{...}` cascades in `main.tex` so the
build falls back to `docs/figures/` or a placeholder box if the
file is missing — no compile errors if either is absent.

## Bibliography

`refs.bib` includes:
- Holm 1967 (constriction resistance)
- Lawn 1998 (fracture stages)
- Auerbach 1891 (cone-crack onset)
- Bruggeman 1935 (effective-medium theory)
- Cronau 2022 (SE size factor)
- Trevisanello 2021 (AM crystallinity)
- Wang 2022 (thermal grain factor)
- Bielefeld 2022 (ASSB microstructural modelling)
- Minnmann 2021 (cathode performance)
- Lee 2020 (Argyrodite cathode)
- Sakuda 2013 (sulfide mechanical)
- Kloss 2012 (LIGGGHTS)
- **Porosity-model additions (new):**
  - Bouvard 2004 (binary RCP curve)
  - Sridhar–Fleck 2000 (SFM constraint factor)
  - Heckel 1961 (plastic compaction)
  - Tabor 1948 (hardness/yield ratio)
  - Storåkers–Fleck–McMeeking 2000 (composite-powder yield)
  - Bouvard 2000 (three-regime hard-soft powder)
  - Jacobs–Thorpe 2009 (rigidity-percolation 2/3 anchor)
  - Henkes–O'Hern–Chakraborty 2005 (force-chain percolation)
  - Liu–Yin 2025 (ASSB stress-bearing percolation)
