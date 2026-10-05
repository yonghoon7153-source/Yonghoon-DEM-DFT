# E2b 진단 — 우리 산화 onset 2.256 V 가 문헌(Zhu15·Schw21 2.01 V)보다 0.246 V 높은 원인 분해 (트랙 ESW · 1저자 = 사용자)
# 출처: litdb/papers/wu2026_asslsb_li2s_reaction_mechanisms_engineering_review.md §11-(iii) E2 (논문 에이전트 2026-10-03)
#
# E2a (계산 없이 답 있음): db/properties/esw_lis4excluded.json 의 comp1 단계표에서 1.717 V 산물 = Li3PS4 + Li2S + LiCl,
#   2.256 V 산물 = Li3PS4 + LiCl + S + 2Li — 두 단계의 차이가 정확히 Li2S -> S + 2Li 다. 우리 hull 에서 산화 onset 은 곧 Li2S 산화 전위다.
# E2b (이 블록): 같은 hull 을 보정(MP2020 / 보정 끔) × 상 제외(GG 3상 / 없음) 네 칸으로 다시 세워 Li2S·comp1·modelc onset 을 낸다.
#   CPU 1 분 미만 · gabia uma env · MP_API_KEY 는 환경변수에서만 읽는다 (찍지 않는다).
#
# 결과 보기 전에 정한 읽는 법 (2026-10-03)
#   ① 대조: MP2020·GG제외 의 comp1 onset 이 2.256 ± 0.0015 V 가 아니면 해석 중지 — hull 이 6 월과 다르다 (원인부터).
#   ② 각 칸에서 Li2S onset = comp1 onset 이면 'onset = Li2S 산화 전위' 를 그 칸 조건부로 적는다.
#   ③ 분해: Δ_LiS4 = (MP2020·제외없음) − (MP2020·GG제외) · Δ_보정 = (보정끔·GG제외) − (MP2020·GG제외). 기록만 한다.
#      HZ-esw-reduction-limit-label 의 '0.246 V 원인 미확정' 문구를 바꿀지는 결과를 보고 1저자가 정한다.
#   ④ ⛔ '보정끔' 값은 절대 전압으로 인용하지 않는다 — 원인 분해용 진단일 뿐이다 (MP2020 보정이 우리 기준계의 일부).
# 못 하는 것: 2015 년 MP 판본 에너지를 되살리지 못한다 — '보정 끔' 은 MP2020 음이온 보정의 몫만 떼어 본다. 판본 차의 나머지는 여기서 안 갈린다.
# 로컬 시험 (2026-10-03 · pymatgen 2026.10.2): 가짜 Li–S 엔트리로 2.000 / 1.750 / LiS4 경유 1.986 V 기대값 통과 · 가짜 mp_api 로 블록 전체 문법 확인.
cd /data/work && /data/apps/miniforge3/envs/uma/bin/python - <<'EOF'
import os, warnings; warnings.filterwarnings("ignore")
from mp_api.client import MPRester
from pymatgen.core import Composition, Element
from pymatgen.analysis.phase_diagram import PhaseDiagram
from pymatgen.entries.computed_entries import ComputedEntry
GG = ("LiS4", "SCl3", "Li5PS4Cl2"); T = {"Li2S": "Li2S", "comp1": "Li6PS5Cl", "modelc": "Li5.4P1S4.4Cl1.6"}
with MPRester(os.environ.get("MP_API_KEY")) as m:
    E = m.get_entries_in_chemsys(["Li", "P", "S", "Cl"], additional_criteria={"thermo_types": ["GGA_GGA+U"]})
def onset(es, comp, drop):
    es = [e for e in es if e.composition.reduced_formula not in drop]
    pd = PhaseDiagram(es); li = Element("Li"); mu0 = pd.el_refs[li].energy_per_atom
    st = sorted((round(mu0 - s["chempot"], 3), round(s["evolution"], 3), str(s["reaction"])) for s in pd.get_element_profile(li, Composition(comp)))
    r = [s for s in st if s[1] < -1e-6]; return r[0] if r else None
raw = [ComputedEntry(e.composition, e.uncorrected_energy, entry_id=e.entry_id) for e in E]
res = {}
for tag, es in (("MP2020", E), ("보정끔", raw)):
    for dtag, drop in (("GG제외", GG), ("제외없음", ())):
        res[tag, dtag] = o = {k: onset(es, c, drop) for k, c in T.items()}
        print(f"{tag} {dtag} | " + " | ".join(f"{k} {v[0]:.3f} V ({v[2]})" if v else f"{k} —" for k, v in o.items()))
c = res["MP2020", "GG제외"]["comp1"]; cv = c[0] if c else float("nan")
print(f"entries {len(E)} · 대조 comp1 (MP2020·GG제외) = {cv:.3f} V → " + ("OK (6 월 2.256 재현)" if abs(cv - 2.256) < 0.0015 else "⛔ 6 월 hull 과 다름 — 해석 중지"))
l = min((e for e in E if e.composition.reduced_formula == "Li2S"), key=lambda e: e.energy_per_atom); n = l.composition.get_reduced_composition_and_factor()[1]
print(f"Li2S {l.entry_id} 보정 {l.correction / n:+.3f} eV/fu · " + " · ".join(f"{a.name} {a.value / n:+.3f}" for a in l.energy_adjustments))
EOF
