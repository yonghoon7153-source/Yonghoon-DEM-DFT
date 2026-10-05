# 믹서 고-Bo 강성 축 — 개발 탐색 `dev-u` 덱 (균일 γ 배율 두 수준) · 되읽기 · 덱 비교 증거 (2026-10-05)

**등록 = 사전등록 v2.9 §12** (`docs/reviews/mixer_highbo_stiffness_prereg_20260929.md` · 1저자 *"ㅇㅇ 그러자 하지만 망이 더 우선순위로"* 10-05) —
dev-rot · dev-bo 의 M 을 **본 뒤** 정한 개발 탐색 두 팔 (사후 설계).  ⛔ 확인 블록 아님 · 확인 seed 와 섞지 않는다 · 판정선 없음.

| 덱 (`decks/`) | 팔 | CED 배율 (LC 대비 · 9 비영 원소 전부) | SE 쪽 Bo_code | 생성 명령 (`gen_cmd.txt`) | in.mixer sha256 앞 16 |
|---|---|---|---|---|---|
| `LU212_ref_r2_s32452843` | `LU212` | ×10 | 212.44 (= 0.212 × 1000) | `--n-total 100000 --cgf 151.4 --arm LU212 --seed 32452843 --revolutions 2 --stiffen-se 20 --hold-bo-pairwise` | 8cb48a132d8a90c0 |
| `LU637_ref_r2_s32452843` | `LU637` | ×14.422496 (= 10 · 3^(1/3)) | 637.32 (= 0.212 × 3000) | 같은 명령 · `--arm LU637` | 57872d5d4a1c7162 |

생성 규약 = 팔 `LC` 와 같다 (`bond 1 · layered · abs_base 0.21244 · coat AM→SE`) + `abs_mult` = SE 낀 세 쌍 (SE–SE · AM_P–SE · AM_S–SE) × 1000 · 3000 × BO_BASE.
코팅 상 (AM) 의 목표 Bo 가 SE–SE Bo 를 JKR 기하로 따라 오르고 벽은 대각 ÷ 1.842 ⇒ **CED 9 비영 원소 전부 같은 배율** (생성기 셀프테스트 U② · soft · ×20 경화 둘 다
상대 1e-12) = 같은 γ 세계 (LC) 를 키운 것 = **균일 γ 배율** (SE 만의 개입 아님 · 혼합쌍은 min 규칙 그대로).  강성 · seed · 바퀴 · 삽입 · 기구는 `LC_ref_r2_s32452843`
(ibb dev-rot 에서 돈 덱) 과 같다.

재생성: `bash docs/data/mixer_highbo_dev_decks_20261005_u/build.sh` → `(cd docs/data/mixer_highbo_dev_decks_20261005_u && sha256sum -c SHA256SUMS)` (12 줄 —
덱 폴더 8 파일 · 되읽기 2 · 덱 비교 2).  ⛔ 시뮬레이션 · ibb · WSL 실행 없음 — 덱 텍스트의 계약이다.

| 검사 | 결과 |
|---|---|
| 같은 명령을 임시 폴더에 다시 돌린 덱 = 커밋 덱 (바이트) | 2/2 |
| 기존 팔 불변 — 지금 생성기의 `LC_ref_r2` · `LH_ref_r2` = v26 커밋 덱 (= ibb dev-rot 실행 덱 · sha256 `5405067f…` · `3125d244…`) | 2/2 |
| 이름 → 덱 (`mixer_deck_diff.cell_expected_deck` — 런처 `dev-u` 관문이 쓰는 경로) = 커밋 덱 | 2/2 |
| 되읽기 표 U (`readback.md` · `readback.json`): LC_ref_r2 → LU212 · LU637 · LU212 → LU637 | **3/3 PASS** — 같은 E · ν · dt (Rayleigh · k = 1) · 9 비영 항 한 공통 배율 ×10 · ×14.42249 · ×1.442249 (인쇄 덱의 기하평균 · 퍼짐 0 · 5.86e-06 · 5.86e-06 ≤ 2e-05) · 벽–벽 0 · 나머지 명령 토큰 동일 |
| 덱 비교 `--allow A` · `--allow B` (쌍 집합) — LC_ref_r2 → LU212 · LU637 | **4/4 FAIL (기대대로)** — SE 낀 쌍 (AM_P–SE · AM_S–SE · SE–SE · SE–벽) 이 허용목록 밖 |
| 덱 비교 `--allow U` (배율 하나) `--expect-deck <재생성 덱>` — LC_ref_r2 → LU212 · LU637 · LU212 → LU637 | **3/3 PASS** — CED 밖 명령 (E · ν · timestep · run · 덤프 · 기하 · seed · 삽입) 은 토큰까지 같다 · 목표 배율 (Bo 배수^(1/3)) 과 원소별 배율의 최대 상대 차 2.2e-16 · 2.9e-06 · 2.9e-06 (≤ 1e-5) |
| (참고) `--allow U` — LH_ref_r2 → LU212 · LU637 | **2/2 FAIL (기대대로)** — LH 의 AM 점착 사다리 위가 아니다 (배율이 하나가 아니고 AM 쌍은 줄어든다) |

⇒ **통과하는 가장 좁은 허용목록 = U**.  정확한 명령과 출력 = `deck_diff.txt` (절마다 머리 줄 = 명령 · 끝 줄 = rc) · 원소별 배율 = `deck_diff.json` (`ced` · `target_ratio` ·
`max_rel_dev_from_target`).  예:

```
python3 scripts/mixer_deck_diff.py docs/data/mixer_highbo_dev_decks_20260930_v26/decks/LC_ref_r2_s32452843/in.mixer \
        docs/data/mixer_highbo_dev_decks_20261005_u/decks/LU212_ref_r2_s32452843/in.mixer --allow B     # → FAIL · rc 1 (SE 낀 쌍 목록 밖)
python3 scripts/mixer_deck_diff.py <같은 두 덱> --allow U --expect-deck <같은 명령 재생성 덱>            # → 1/1 PASS · rc 0 · 공통 배율 ×10
```

## ibb 에서 (리포 루트 · dev-rot · dev-bo 와 같은 OUT · NP 20)

⚠ 셸에 넣는 줄에 **꺾쇠 자리표시를 쓰지 않는다** — 10-02 dev-bo 첫 발사 줄이 `LMP=<…>` 를 리다이렉트로 읽어 발사 0 이었다.  아래 `XXXXXXXXXXXX` 하나만 통합 커밋 SHA 로 바꾼다.

```bash
# ① ibb 사본을 통합 커밋으로 (사본은 detached — pull 대신 fetch + checkout)
cd ~/Yonghoon-DEM-DFT                       # dev-bo 때와 같은 사본 (경로가 다르면 그 경로)
SHA=XXXXXXXXXXXX                            # ⬜ 통합 커밋 SHA
git fetch origin claude/sdcp-dem-manuscript-si-pqwtv8 && git checkout --detach "$SHA" && git log -1 --format='%H %s'
(cd docs/data/mixer_highbo_dev_decks_20261005_u && sha256sum -c SHA256SUMS)          # 12 줄 OK
python3 scripts/mixer_deck_diff.py --selftest | tail -1                              # 55/55 PASS
python3 scripts/mixer_stage_gate.py --selftest | tail -1                             # 14/14 PASS

# ② 같은 OUT 에 셀 둘 (fresh — 이미 있으면 멈춘다)
OUT=$HOME/mixer_dev7_20260930_v26
for c in LU212_ref_r2_s32452843 LU637_ref_r2_s32452843; do
  mkdir "$OUT/$c" || break
  cp docs/data/mixer_highbo_dev_decks_20261005_u/decks/$c/in.mixer docs/data/mixer_highbo_dev_decks_20261005_u/decks/$c/deck_meta.json "$OUT/$c/"
  cp dem_scripts/mixer_20260919/Drum.stl dem_scripts/mixer_20260919/Front.stl dem_scripts/mixer_20260919/Back.stl "$OUT/$c/"
  printf '100000\n' > "$OUT/$c/n_expected"; printf '0.013138\n' > "$OUT/$c/r_container"
done
python3 scripts/mixer_deck_diff.py --runs "$OUT" --cohort dev-u                       # 관문 1 미리보기 → PASS (U 쌍 LU212 → LU637 · 공통 배율 ×1.442249)

# ③ E0 진단을 새 기록 파일로 — mixer_deck_diff.py 가 바뀌어 옛 기록 (dev_e0_diag_devbo.json 등) 은 도구 sha 대조로 거부된다 · LIGGGHTS 재실행 없음
python3 scripts/mixer_smoke_blind.py --e0-diag "$OUT" --record "$OUT/dev_e0_diag_devu.json"   # → PASS (complete · technical · a) 여야 ④

# ④ 발사 — dev-bo 와 같은 바이너리 · PATH · conda env (dev-bo 봉인에서 읽는다 · §8-1 같은 환경)
REC_BO="$OUT/LHx10_ref_r2_s32452843/launch_record.json"
LMP_BO=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["lmp_path"])' "$REC_BO")
SBP_BO=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["slurm"]["path_prefix"])' "$REC_BO")
SBE_BO=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["slurm"]["conda_env"])' "$REC_BO")
echo "LMP=$LMP_BO · SB_PATH=$SBP_BO · SB_ENV=$SBE_BO"
BACKEND=slurm NP=20 OUT="$OUT" LMP="$LMP_BO" SB_PATH="$SBP_BO" SB_ENV="$SBE_BO" \
  bash dem_scripts/mixer_20260921/launch_highbo.sh dev-u "$OUT/dev_e0_diag_devu.json"
squeue -u "$USER"                                                                     # 두 job (LU212 → LU637) · NP 20 · 3 일 한도
```

런처 `dev-u` 관문이 다시 본다: 정책 v4 (`STIFF-DEV-U-2026-10-05`) · 덱 = 이름에서 재생성한 덱 (바이트) · deck_meta (deck_sha256 · 팔 · seed · 바퀴 · 강성) ·
STL = 캠페인 원본 · n_expected · r_container · fresh · 디스크 · E0 진단 PASS 기록 (지금 도구 sha · 블록 NP = 기록 NP = 20) → 봉인 (`requires` = 기록의 절대경로 · sha256) →
sbatch → job 시작 직전 `start_check.py` 재대조.  SB_TIME 은 주지 않는다 (새 단계는 정책 시간 3 일 · 주면 거부).
비용 = `LC_ref_r2` · `LH_ref_r2` · dev-bo 와 같다: 2 바퀴 6,102,533 step · dt 2.62e-07 s · NP 20 에서 ≈ 27 h/런 (dev-bo 실측) · 둘 동시 = 40 코어 (QOS cpu-60).

## 한정

- 정적 평형 겹침 δ/r (CGF 151.4 · SE–SE · 점착 지배 · 고립 접촉 근사): soft 0.402 · 0.837 % · ref ×20 (덱 E) 0.055 · 0.114 % — 1 % 천장 안 · 생성기 셀프테스트 U⑤ 가 고정 ·
  **충돌 최대 겹침의 상한이 아니다** (동적 겹침은 미측정 · 저장 프레임 최대는 `check_contact_validity.py` 로 보고만 — 관문 아님).
- ⚠ LU637 은 CGF 200 에서 SE–SE 1.007 % 로 천장 밖 = 생성기가 거부한다 (같은 Bo 면 parcel 이 클수록 겹침이 크다) · X = 850 (Bo ×4000) 은 캠페인 CGF 151.4 에서도 1.014 % 로 거부.
- dt 2.62e-07 s (경화 SE 가 정한다) · run 1 · 518,714 · 518,714 · 6,102,533 · 덤프 30,512 step — `LC_ref_r2` 와 같다 (비용 같다 · 셀프테스트 U③).
  `--stiffen-se` 는 SE 만 경화 ⇒ AM–AM · AM–벽 CED 는 soft 값 그대로 · 9 원소 F₀ 비 1 (U⑦) ⇒ 경화 덱에서도 9 원소가 LC 와 같은 배율.
- `deck_meta.json` 은 생성기 sha256 을 적는다 — 생성기가 바뀐 뒤 build.sh 를 다시 돌리면 meta 바이트는 달라질 수 있다 (덱 바이트는 그대로여야 한다 · build.sh 가 본다).
- 이 증거는 **덱 텍스트의 계약**이다 — 실행 · 완주 · 접촉 상태 · M 은 ibb `dev-u` 뒤.  공동 개입 = CED 9 원소 전부 (균일 γ 배율) · SE ×20 경화가 SE 쪽 충돌 점착을
  soft 보다 약하게 만든다 (붙는 속도 ×0.37 · 사전등록 §12-4) · *"실제 코팅 효과"* · *"실제 분말"* 문장 금지.
