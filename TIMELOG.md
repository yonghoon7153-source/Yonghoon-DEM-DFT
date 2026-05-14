# TIMELOG

## 2026-05-14

### 17:19 — comp4_v2 z-shift sweep 시작점 (RESUME HERE)

**현재 막힌 부분**: v2 shift 2 데이터로 OLD recipe (face B, α=1.0, Y_SHIFT=0.76) 적용
시 comp4_v2 dW_strain=3.64 (J/m²) outlier로 paper rank (comp3>4>5) 안 맞음.
- comp1 (Li6): dW=+2.633, Wad+α=−0.69
- comp2 (Li6): dW=+2.503, Wad+α=−0.76
- comp3_v2:    dW=+0.873, Wad+α=+0.25
- **comp4_v2:  dW=+3.640, Wad+α=−2.33  ← outlier (rank 깸)**
- comp5_v2:    dW=+0.314, Wad+α=+0.90
- BBBBB 결과: R=−0.04, ρ=+0.20, family_ok ∩ rank_ok 조합 0개

**원인 확인**:
- comp4_v2 V0 cell |a1|=13.967 Å (NCM 기준 14.23 → 1.83% strain)
- comp3_v2 |a1|=14.122, comp5_v2 |a1|=14.181 (strain 0.77%, 0.35%)
- comp4 champion이 4% 부피 압축됨 → MLIP relax artifact 가능성
- comp4_v2 모든 anneal rank/champion 31개가 동일 cell (V0 1개만 존재)
- comp4_v2_V0_extracted.xyz는 다른 cell (V=1253 Å³ vs UMA V=1204 Å³)이지만
  검증 안 됨

**다음 액션 (RESUME HERE)**:
comp3_v2 / comp5_v2는 shift 2 그대로 두고, **comp4_v2만 shift 0/1/3/4로
face_flip 추가 실행** → paper rank 맞는 comp4 shift 찾기.

표면 chemistry 확인됨 (shift / comp3 / comp4 / comp5):
- shift 0: Br/Cl  / Br/Br  / Br/Br
- shift 1: S/Br   / S/Br   / S/Br    ← 공통 S/Br
- shift 2: Cl/Cl  / Cl/Cl  / Cl/Cl   ← 공통 Cl/Cl (현재)
- shift 3: Cl/Cl  / Cl/Br  / Cl/Br
- shift 4: S/Br   / S/Cl   / S/Br

**예상 목표**: comp4_v2 Wad_well이 +3.89 ~ +4.55 J/m² 사이여야 dW=3.64 빼고도
comp3 (+0.25) ~ comp5 (+0.91) 사이로 들어옴. 현재 shift 2는 +1.31 (너무 작음).

**Fallback 옵션** (어느 shift도 만족 못하면):
A. comp4_v2 dW를 comp4_v1 값 (~0.44)로 override (정당화: V2 cell artifact)
B. v1 BBABA로 fallback (R=+0.908, 이미 검증됨)
C. comp4_v2_V0_extracted 사용해서 face_flip + eiso fix 재실행

**실행 명령** (`/data/work/v30u_ensemble`에서):
```bash
cp comp4_slab_v2_PRESERVED.xyz comp4_slab_v2_PRESERVED.shift2.bak
mv comp3_slab_v2_PRESERVED.xyz comp3_slab_v2_PRESERVED.HIDE
mv comp5_slab_v2_PRESERVED.xyz comp5_slab_v2_PRESERVED.HIDE
cp face_flip_results/comp4_v2_done.json face_flip_results/comp4_v2_shift2_done.json
for s in 0 1 3 4; do
  cp comp4_v2_slab_shift${s}.xyz comp4_slab_v2_PRESERVED.xyz
  python3 run_v30u_1L_face_flip.py 2>&1 | tail -10
  mv face_flip_results/comp4_v2_done.json face_flip_results/comp4_v2_shift${s}_done.json
done
mv comp3_slab_v2_PRESERVED.HIDE comp3_slab_v2_PRESERVED.xyz
mv comp5_slab_v2_PRESERVED.HIDE comp5_slab_v2_PRESERVED.xyz
cp comp4_slab_v2_PRESERVED.shift2.bak comp4_slab_v2_PRESERVED.xyz
cp face_flip_results/comp4_v2_shift2_done.json face_flip_results/comp4_v2_done.json
```

(~40분 컴퓨트, 4 shift × 2 face × 36 reg × 16 gap = 4608 SCFs)

### 이전 (요약)
- v1 BBABA OLD recipe로 R=+0.908, ρ=+0.900 확보 (paper-aligned visual)
  하지만 v1은 champion 데이터 아니라 v2로 가려고 시도 중
- v2 shift 2 face_flip 완료 (comp3/4/5 모두 Cl/Cl 표면)
- eiso fix 재계산 완료 — comp4_v2 dW=3.64로 outlier 판명
- OLD figure (R=+0.931)는 paper-aligned visual의 target reference
- mechanism md (kb/papers/mechanism_anion_O_descriptor.md) 작성됨
- 14 pair bond density killer descriptor (ρ=−1.00, R=−0.95) 확정됨
