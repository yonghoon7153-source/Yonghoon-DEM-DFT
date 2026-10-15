# Independent visual inspection, seminar v3.3

2026-10-15. Read-only review of the actual delivered PDF. No producer script was executed and no submitted file was modified. The PDF and Presentations skills were read. All 18 pages were independently rendered with bundled Poppler at 144 dpi (1440 x 1080 pixels) and visually inspected. A separate 288 dpi crop of slide 3's source text was also inspected. This is PDF inspection, not a PowerPoint application rendering check.

## Result

No new actionable blocking visibility defect was found in the revised PDF. The revised content on 3, 7, 11 and 15 is visible, complete and free of title overlap, clipping or obstruction. Dense inherited slide styling alone is not a HOLD finding.

| Page | Actual PDF observation | Disposition |
|---|---|---|
| 3 | The representative-equation source is two right-aligned lines. The second line visibly says that equation ② uses the small-overlap approximation. The `ℓᵢⱼ ≈ Rᵢnᵢⱼ` subscripts render without replacement boxes. The PDF uses Carlito Italic plus DejaVu Sans for fallback glyphs. The source text ends at y = 91.632608 pt and the following title begins at y = 96.893 pt, giving 5.260392 pt clearance. The source text is 10.006 pt in the PDF. | PDF visibility passes. Native PowerPoint OMML and font substitution on the presentation PC remain untested. |
| 7 | The first body bullet visibly includes `nominal stopping pressure; see Problem 4`, across the existing two lines. It does not collide with the second bullet or the bed images. | Accept. |
| 11 | The four-line second bullet visibly names the combined follow-up protocol, plate-contact history reset, lower damping, force hold, and pending static-equilibrium/conservation checks. `combined follow-up protocol` and `model-internal diagnostic` remain red. The three-row open-check table is readable, including the plate-history-reset row and `13 SE particles lost`. The hatched bars remain apparent. The three-line `registered prediction band` callout and its leader are visible, and the (b) caption uses the same name. The y-axis ends at 20. | Accept visible revision. Scientific meaning and source arithmetic are separately reviewed by the parent. |
| 15 | The flow reads insertion, stabilization, compression, servo, relaxation, unloading, platen removal. Unloading and platen removal are both bold navy, in their respective sixth and seventh boxes. The two-line small print ends `Heckel analysis to be redone`; it is fully visible with substantial clearance before the footer. Its PDF font is approximately 13.01 pt. | Accept. |

All other pages were visually inspected, including charts, captions, references and footers. Zero extracted words extend outside any PDF page. This geometric check supports the visual inspection; it is not treated as proof of every layout property.

## Direct unchanged-page verification

Exactly these 14 pages are unchanged: **1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16, 17, 18**.

This was independently established in two ways, without relying on the producer manifest:

1. Each v3.3 submitted `input/png/slide-NN.png` was read and compared byte-for-byte (and by decoded pixels) to the preserved v3.2 `input/png/slide-NN.png`.
2. Both actual PDFs were independently rendered with the same Poppler settings. The rendered pixels are exactly equal for those same 14 pages.

Only pages 3, 7, 11 and 15 have changed pixels. Their changed bounding rectangles, in pixels of the 1440 x 1080 independent render, are:

| Page | Changed pixel bounding rectangle (left, top, right, bottom) | Consistent with |
|---|---|---|
| 3 | (568, 138, 1375, 181) | Source line band only |
| 7 | (193, 244, 1306, 316) | First body bullet only |
| 11 | (87, 345, 1361, 973) | Second body bullet and shifted figure/table/caption area |
| 15 | (300, 787, 1327, 928) | Flow labels and small print |

The source PDF SHA-256 is `706d6a1d062936c16aff15af4500cb7cff9ef8e5c19866d4c48ccaaeea64999e`.

## Word-limit question

An independent XML read of the actual PPTX reproduces the declared counts: slide 7 **104/100**, slide 11 **121/120**, slide 15 **121/120**. The declared counting rule excludes source/credit/literature/section/bridge labels, footer text, numeric page numbers, grouped text and table cells. These are not counts of every visible word on the page.

The 4-word and 1-word overruns are acceptable for this presentation revision: the required qualifying language remains readable, body text is approximately 15 pt in the PDF, and there is no resulting collision or lost disclosure. Slide 11 is dense and deserves deliberate delivery, but no additional shortening or font reduction is required to close the requested visual corrections. This is a specific acceptance of the reviewed overruns, not a claim that the original numerical caps were literally met.

## Inherited presentation preparation

The first-slide date placeholder and presenter-reserved empty image regions on 4, 6, 12 and 13 remain visible. These are pixel-identical to v3.2 and were already explicitly excluded from scientific change findings in the prior review (its section 7). They still need the presenter's normal completion before use; they are not newly introduced v3.3 blockers.

The presentation PC check remains separate: open slide 3 in PowerPoint and inspect the eight native OMML equations plus the added Unicode subscripts. The present review does not claim that this has happened.

## Evidence

- `agents/visual_render.py`: independent render and comparison script; no producer imports.
- `agents/visual_geometry.json`: PDF words/characters, hashes, direct PNG and independently rendered PDF comparisons.
- `agents/visual_metrics.py` and `agents/visual_metrics.json`: independent PPTX word counts, numeric source-line clearance and comparison summary.
- `agents/visual_text.txt`: extracted actual PDF text.
- `renders/page-01.png` through `renders/page-18.png`: independent actual v3.3 PDF renders.
- `renders/prior-page-01.png` through `renders/prior-page-18.png`: corresponding independently rendered v3.2 PDF.
- `renders/page03-source-detail-03.png`: 288 dpi PDF source-line detail.
