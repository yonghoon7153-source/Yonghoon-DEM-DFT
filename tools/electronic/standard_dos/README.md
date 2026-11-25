# Standard DOS / band-gap recipe (literature-aligned)

**Why:** our M1 gap (LPSCl 1.76 eV) came from `occupations='smearing' (mv, 0.01 Ry)` + a
DOS<0.5 threshold straddling E_F. Smearing broadens the band edges into the gap and the
threshold cuts inside it, so the gap reads LOW. The literature standard (VASP ISMEAR=-5 /
QE `tetrahedra_opt`) takes the gap directly from the **eigenvalues (VBM/CBM)** with **no
smearing**. CEJ Lu 2025 = 1.88 (Γ-only), JMCA-C Rao 2025 = 2.19/2.32 (PAW 4x4x4), MDPI
Batteries = 2.45 (PBE)/3.30 (HSE06), Physica B = 3.11 (mBJ). Our value should land in the
PBE band-structure band (~2.0-2.4) once the method is fixed.

## What changed vs the old run
| | OLD (1.76) | NEW (standard) |
|---|---|---|
| occupations | `smearing='mv'`, degauss 0.01 Ry (~0.27 eV) | `fixed` (gap) / `tetrahedra_opt` (DOS) — NO smearing |
| gap source | DOS < 0.5 threshold | **VBM/CBM eigenvalues** (QE prints "highest occupied, lowest unoccupied") |
| empty bands | (few) | `nbnd` = N_occ + ~30% (need empty states to see CBM) |
| k-mesh | k666 SCF | dense NSCF (8x8x8 comp1; comparable for modelc) |

(Pseudo/ecut: keep IDENTICAL to the SCF that made the density — reuse `./tmp`. USPP→PAW is a
secondary ~0.1 eV; the gap-extraction fix above is the dominant correction. If you want the
most PAW-literature-faithful number, re-run SCF with the kjpaw 70 Ry pseudos used for LOBSTER/Bader.)

## N_occ / nbnd (USPP valence: Li 3, P 5, S 6, Cl 7)
- comp1 Li6PS5Cl (52 at): 24*3+4*5+20*6+4*7 = **240 e -> N_occ 120**, set `nbnd = 160`
- modelc Li5.4PS4.4Cl1.6 (62 at, Li27P5S22Cl8): 27*3+5*5+22*6+8*7 = **294 e -> N_occ 147**, set `nbnd = 190`
- VERIFY: grep "number of electrons" / "number of Kohn-Sham states" in your existing SCF .out.

## Run sequence (KISTI, 1-GPU convention; reuse existing SCF density in ./tmp)
```bash
B=/scratch/x3430a02/kgy/apps/qe-gpu/bin
# (A) direct gap — fixed occupations prints VBM/CBM
mpirun -np 1 $B/pw.x -npool 1 < nscf_gap.in   > nscf_gap.out
python3 extract_gap.py nscf_gap.out
# (B) DOS + PDOS figure — tetrahedron (no smearing)
mpirun -np 1 $B/pw.x -npool 1 < nscf_dos.in   > nscf_dos.out
$B/dos.x      < dos.in      > dos.out
$B/projwfc.x  < projwfc.in  > projwfc.out
```
Gap = number from (A). DOS plot from `${PREFIX}.dos` (col1=E, col2=DOS); shift by E_F (dos.out header).

## Expected
- comp1: gap should rise from 1.76 to ~2.0-2.4 eV (matches PBE band-structure literature).
- modelc: if `fixed` reports "highest occupied, lowest unoccupied" cleanly -> that's the gap.
  If it instead shows partial occupation / no clean LUMO, that IS the arrangement-dependent
  defect-band (the EF<VBM we discussed) — note it and use the tetrahedron DOS to inspect.
- Report Delta(gap) = modelc - comp1 (robust) alongside the absolute (method-dependent).
