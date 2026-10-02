# 믹서 고-Bo 강성 축 — 개발 탐색 `dev-bo` 덱 (LH ×10 · ×30) · 되읽기 · 덱 비교 증거 (2026-10-02)

**등록 = 사전등록 v2.8 §11** (`docs/reviews/mixer_highbo_stiffness_prereg_20260929.md` · 1저자 *"ㄱㄱ"* 10-02) — DEV seed 1 의 2 바퀴 M 열람
(`docs/data/mixer_highbo_devrot_prelim_20261002/`) **뒤** 정한 개발 탐색 두 팔.  ⛔ 확인 블록 아님 · 확인 seed 와 섞지 않는다 · 판정선 없음.

| 덱 (`decks/`) | 팔 | AM–AM Bo_code | 생성 명령 (`gen_cmd.txt`) | in.mixer sha256 앞 16 |
|---|---|---|---|---|
| `LHx10_ref_r2_s32452843` | `LHx10` | 384 (= LH 38.4 × 10) | `--n-total 100000 --cgf 151.4 --arm LHx10 --seed 32452843 --revolutions 2 --stiffen-se 20 --hold-bo-pairwise` | a2792897f32c3858 |
| `LHx30_ref_r2_s32452843` | `LHx30` | 1152 (= LH × 30) | 같은 명령 · `--arm LHx30` | d00eb369f35145dd |

생성 규약 = 팔 `LH` 와 같다 (`bond 1 · layered · abs_base 0.21244 · abs_mult = AM 쌍 셋`) ⇒ AM–벽 CED 도 같은 벽 규칙 (대각 ÷ 1.842) 으로 함께 오른다 =
**공동 개입 B** (AM–AM 만의 개입 아님).  강성 · seed · 바퀴 · 삽입 · 기구는 `LH_ref_r2_s32452843` (ibb dev-rot 에서 돈 덱) 과 같다.

재생성: `bash docs/data/mixer_highbo_dev_decks_20261002_bo/build.sh` → `(cd docs/data/mixer_highbo_dev_decks_20261002_bo && sha256sum -c SHA256SUMS)` (12 줄 —
덱 폴더 8 파일 · 되읽기 2 · 덱 비교 2).  ⛔ 시뮬레이션 · ibb · WSL 실행 없음 — 덱 텍스트의 계약이다.

| 검사 | 결과 |
|---|---|
| 같은 명령을 임시 폴더에 다시 돌린 덱 = 커밋 덱 (바이트) | 2/2 |
| 기존 팔 불변 — 지금 생성기의 `LC_ref_r2` · `LH_ref_r2` = v26 커밋 덱 (= ibb dev-rot 실행 덱 · 판독 JSON 출처 sha256 `5405067f…` · `3125d244…`) | 2/2 |
| 이름 → 덱 (`mixer_deck_diff.cell_expected_deck` — 런처 `dev-bo` 관문이 쓰는 경로) = 커밋 덱 | 2/2 |
| 되읽기 표 B (`readback.md` · `readback.json`): LC_ref_r2 → LHx10 · LHx30 · LH_ref_r2 → LHx10 · LHx30 · LHx10 → LHx30 | **5/5 PASS** — 같은 E · ν · dt (Rayleigh 1/k) · 다섯 쌍만 증가 · 나머지 CED 인쇄 토큰까지 같다 |
| 덱 비교 `--allow A` (AM–AM 셋만) — LH_ref_r2 → LHx10 · LHx30 | **2/2 FAIL (기대대로)** — AM_P–벽 · AM_S–벽 이 허용목록 밖 |
| 덱 비교 `--allow B` (AM–AM 셋 + AM–벽 둘) `--expect-deck <재생성 덱>` — LH_ref_r2 · LC_ref_r2 → LHx10 · LHx30 · LHx10 → LHx30 | **5/5 PASS** — CED 밖 명령 (E · ν · timestep · run · 덤프 · 기하 · seed · 삽입) 은 토큰까지 같다 |

⇒ **통과하는 가장 좁은 허용목록 = B**.  CED 배수 (LH_ref_r2 → LHx10 · LHx30): 다섯 쌍 ×2.154 = 10^(1/3) · ×3.107 = 30^(1/3) (Bo ∝ CED³) ·
SE 낀 쌍 · 벽–벽 정확히 같다.  정확한 명령과 출력 = `deck_diff.txt` (절마다 머리 줄 = 명령 · 끝 줄 = rc) — 예:

```
python3 scripts/mixer_deck_diff.py docs/data/mixer_highbo_dev_decks_20260930_v26/decks/LH_ref_r2_s32452843/in.mixer \
        docs/data/mixer_highbo_dev_decks_20261002_bo/decks/LHx10_ref_r2_s32452843/in.mixer --allow A     # → FAIL · rc 1
python3 scripts/mixer_deck_diff.py <같은 두 덱> --allow B --expect-deck <같은 명령 재생성 덱>            # → 1/1 PASS · rc 0
```

## 런 폴더로 옮길 때 (ibb · 리포 루트 · dev-rot 과 같은 OUT)

계약은 `docs/data/mixer_highbo_dev_decks_20260930/README.md` §6 과 같다 — `in.mixer` + `deck_meta.json` + Drum · Front · Back STL (`dem_scripts/mixer_20260919/`) +
`n_expected` (100000) + `r_container` (0.013138):

```bash
OUT=$HOME/mixer_dev7_20260930_v26
for c in LHx10_ref_r2_s32452843 LHx30_ref_r2_s32452843; do
  mkdir "$OUT/$c" || break                                   # 이미 있으면 멈춘다 (새 단계 = fresh 만)
  cp docs/data/mixer_highbo_dev_decks_20261002_bo/decks/$c/in.mixer docs/data/mixer_highbo_dev_decks_20261002_bo/decks/$c/deck_meta.json "$OUT/$c/"
  cp dem_scripts/mixer_20260919/Drum.stl dem_scripts/mixer_20260919/Front.stl dem_scripts/mixer_20260919/Back.stl "$OUT/$c/"
  printf '100000\n' > "$OUT/$c/n_expected"; printf '0.013138\n' > "$OUT/$c/r_container"
done
```

런처 `dev-bo` 관문이 다시 본다: 덱 = 이름에서 재생성한 덱 (바이트) · deck_meta (deck_sha256 · 팔 · seed · 바퀴 · 강성) · STL = 캠페인 원본 · n_expected · r_container ·
fresh · 디스크 · E0 진단 PASS 기록.

## 한정

- 정적 평형 겹침 δ/r (CGF 151.4 · 점착 지배 · 고립 접촉 근사): AM_P 0.214 · 0.445 % · AM_S 0.125 · 0.259 % (LH 0.046 · 0.027 %) — 1 % 천장 안 ·
  생성기 셀프테스트 BO⑤ 가 고정 · **충돌 최대 겹침의 상한이 아니다** (동적 겹침은 미측정).
- dt 2.62e-07 s (경화 SE 가 정한다) · run 1 · 518,714 · 518,714 · 6,102,533 · 덤프 30,512 step — `LH_ref_r2` 와 같다 (비용 같다 · BO③).
  `--stiffen-se` 는 SE 만 경화 ⇒ AM–AM · AM–벽 CED 는 soft 값 그대로 = 명목 Bo_code 정확히 (BO⑥).
- `deck_meta.json` 은 생성기 sha256 을 적는다 — 생성기가 바뀐 뒤 build.sh 를 다시 돌리면 meta 바이트는 달라질 수 있다 (덱 바이트는 그대로여야 한다 · build.sh 가 본다).
- 이 증거는 **덱 텍스트의 계약**이다 — 실행 · 완주 · 접촉 상태 · M 은 ibb `dev-bo` 뒤.
