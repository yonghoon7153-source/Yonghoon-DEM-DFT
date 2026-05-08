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

## Section status

| Section | Status | Page est. |
|---|---|---|
| Abstract | Draft (needs final numbers) | 1 |
| 1. Introduction | Placeholder | 1.5 – 2 |
| 2. Methodology | Filled outline (Fig 1 leading) | 3 |
| 3. Stage E corrections | Filled outline | 1 – 1.5 |
| 4. 7-Layer defence | Filled outline (commits cited) | 1.5 – 2 |
| 5. Results: 160-case ensemble | Filled outline | 2 – 3 |
| 6. Discussion | Placeholder | 1 – 2 |
| 7. Conclusion | Filled | 0.5 |

## What to fill in

Sections marked "Placeholder" need user-written prose. The structural
skeleton, equations, figure references, and citations are all in place
so you only need to fill in the narrative text between the
`[Placeholder --- N pages]` markers.

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
