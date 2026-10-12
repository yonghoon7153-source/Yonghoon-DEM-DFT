# ps45 σ_e 보고 기준 검토 증거 반입 (10-13 KST) · 우리 트리 재현

정본 판정 = `docs/reviews/codex_review_ps45_sigmae_reporting_20261013.md` (요청서 `docs/reviews/codex_ps45_sigma_e_basis_request_20261012.md` 의 답 ·
코드 검토 핀 `46cd0bdb8` · 다섯 침대 실행 핀 `0801d4ceb` — 두 핀의 `scripts/network_conductivity.py` 바이트 같음 (sha256 `da9ecfef…`) ·
**권고 (가′) 조건부** = Hertz H0 주 값 + PC 크기 인자 끔 + 공통 기준값 4.1 mS/cm (문헌 펠릿 기준값을 대입한 조건부 환산) · Q1 ×0.082 환산 CONFIRMED ·
Q2 이중 할인 **확정 불가** (인자 끔 = 구조 분리 보고 규약 · 진실 복원 아님) · Q3 부분 (실제 AM 고체 64.7077–64.9201 % · 요청서 60 % 아님) ·
Q5 Hertz H0 주 · Physics g2 = 모형 감도 (전자 Physics = native AM–AM 원판 면적 + ψ 협착 · Tabor 아님) · Q6 정성적 규모 대조만 · 새 P2 `PS45E-01` · `02` · `03` ·
194 · 보충 20 · v1.3 을 다시 막는 판정 아님).  Codex 묶음 설명 = 이 폴더 `README_REVIEW.md` (묶음의 `README.md` 를 이름만 바꿨다).

## 1. 받은 것 · 넣은 것

| 묶음 | 크기 · 항목 | sha256 | 리포 |
|---|---|---|---|
| 원 ZIP `codex_ps45_sigmae_reporting_review_20261013.zip` (1저자 첨부 10-13) | 9,737,493 B · 97 항목 (위험 경로 · 링크 없음 · 새 빈 폴더에 풀고 `python3 -I` 로만 읽음) | `c915131febcac75048d1de9338784a40cfe5cd645f7a4b3e2f92f72ef9a15317` (`ORIGINAL_ZIP_SHA256.txt`) | 넣지 않음 |

- 묶음 표 `DELIVERY_MANIFEST.json` (96 항목 · 자기 제외) 대조 = **96 / 96 같음** (sha256 · 크기) · 표 밖 파일 0 · 판정문 sha256 `9881998b…` = `evidence/final_verification.json` 의 `report_sha256`.
- 민감 정보 검색 (메일 · 토큰 · 개인 경로) = 없음 — `evidence/literature_downloads.json` 의 radware 주소 한 곳 = IOP 봇 확인 페이지 URL 매개변수 (원문 아님 · Codex 도 "NOT used").

| 무엇 | 반입 (26 · 285,179 B) | 뺀 것 (71 · 20,078,508 B — `SLIM_EXCLUDED.tsv` 에 경로 · 크기 · sha256 · 복원 자리 · git blob) |
|---|---|---|
| 판정문 | `docs/reviews/codex_review_ps45_sigmae_reporting_20261013.md` | — |
| 묶음 README · 표 · 스크립트 | `README_REVIEW.md` · `DELIVERY_MANIFEST.json` · `source_manifest.json` · `acquire.py` · `fetch_extra.py` · `fetch_figures.py` · `fetch_references.py` · `package_review.py` · `verify_review.py` | — |
| `evidence/` | 9 (JSON 7 · CSV 1 · 출처 표 1) | 실행 핀 사본 network_conductivity_run0801.py (153,018 B) = `git show 0801d4ceb:scripts/network_conductivity.py` 와 blob 같음 (= 지금 HEAD 의 `scripts/network_conductivity.py`) |
| `notes/` · `probes/` | 4 · 3 (전부) | — |
| `source/` 45 (코드 · 덱 · AM scaffold · 망 표 · 옛 README · CLAUDE.md · 원장 사본) | — | 핀 `46cd0bdb8` 의 git blob 과 **45 / 45 같음** (`git show 46cd0bdb8:<경로>`) |
| `literature_cards/` 5 · `literature_figures/` 16 | — | litdb 정본 핀 `e739c9730` 의 git blob 과 **21 / 21 같음** (`git fetch origin claude/friendly-meitner-lldvar` → `git show e739c9730:<경로>`) |
| `code_tree.json` · `lit_tree.json` (GitHub tree 응답) | — | `git ls-tree -r 46cd0bdb8` 8,233 blob · `git ls-tree -r e739c9730` 12,332 blob — 경로 · SHA-1 **전수 같음** |
| `code_commit.json` · `lit_commit.json` (GitHub 커밋 응답) | — | `sha` 칸 = 핀 (`git show <핀>`) |

- 대조 도구 = `_repro_ours_20261013/verify_excluded.py` (읽기 전용 · rc 0 = 71 / 71 같음).  원문 PDF · 학위논문 · 렌더 이미지는 Codex 가 묶음에 넣지 않았다 (`evidence/literature_access_final.json` 에 URL · sha256 만).

## 2. 우리 트리 재현 (10-13 KST · HEAD `58f40a002` · 컨테이너 Linux · Python 3.11.15 · NumPy 2.4.6 · SciPy 1.17.1 · networkx 3.6.1 — Codex = Windows · Python 3.12.14 · NumPy 2.5.3 · SciPy 1.16.3 · networkx 3.7)

| 무엇 | 어떻게 | 결과 |
|---|---|---|
| Codex 탐침 셋 **무변경** (`code_scaling` · `report_arithmetic` · `composition_basis`) | 새 빈 폴더 `R/ps45_sigmae_review_20261013/` 에 `probes/` 사본 + 작업 트리 자리 = 우리 작업트리 (HEAD 깨끗) 로 가는 링크 + 실행 핀 사본 (evidence 의 network_conductivity_run0801.py) = `git show 0801d4ceb:…` (ZIP 사본 아님) · `R` (검토 폴더의 부모) 에서 `python3 -I -B ps45_sigmae_review_20261013/probes/<탐침>.py` | **셋 다 rc 0** (0.8 s · 0.08 s · 0.09 s) · 작업트리 쓰기 0 (`git status` 깨끗) · 출력 = `_repro_ours_20261013/` |
| `_repro_ours_20261013/compare_probe_outputs.py` → `compare_probe_outputs.json` | 우리 출력 ↔ Codex 증거 — 평탄화 키별 (env · path · resid · float · other — 도구 머리) | **판정값 차이 0** · `code_scaling` 키 2,259 / 2,259 · 같음 1,899 · env 4 (python · numpy · scipy · networkx 판) · resid 158 (반올림 오차 측정 `conservation_rel` · `residual_rel` · `linear_relative_error` — 양쪽 \|값\| ≤ 2.6e-15 · 판정 문턱 1e-6) · float 198 (상대 ≤ 1.8e-15 — 하나만 `maximum_voltage_change` 5.0e-16 ↔ 6.1e-16 = 이론값 0 인 순수 PC 의 기계 잡음) · `report_arithmetic` 261 / 261 전부 같음 · `composition_basis` 245 / 245 · 같음 235 · path 10 (덱 · scaffold 상대 경로 구분자 `\` ↔ `/` 만) |
| `rescaled_readout_pc_factor_on.csv` | `report_arithmetic` 이 다시 씀 | Codex 사본과 **바이트 같음** |

- 대조 도구는 반례 먼저 확인했다 — 자체시험 19 를 엉터리 판정기 둘에 돌려 (`stub_check_compare.py`): 모든 차이를 같음으로 = 4 / 19 · 옛 대조기 꼴 (파이썬 `==` 라 True ↔ 1 을 같다고 봄 · env 범주 없음 · 한쪽만 경로 꼴이어도 path) = 14 / 19 → 실제 판정기 19 / 19.

우리 트리에서 다시 확인된 것 (판정값 = Codex 와 같음):
- **Q1** — 18 가지 비교 (Hertz · Physics × 순수 PC · 순수 SC · 혼합 × FULL · CF · 협착만) q · 간선 · 전위 · 풀이 기록 **비트 같음** · 증서 차이 = `sigma_bulk_S_cm` 하나 · 반올림 전 환산 상대 오차 최대 1.8e-16 (Codex 2.0e-16) · 6 자리 발행값 차 최대 5.04e-7 mS/cm (두 번 반올림 반폭 5.41e-7 안 — 반올림된 열은 비트 비례가 아니다).
- **Q2 인자 끔** (같은 반경 4.5 µm 합성 15 입자 · 22 간선) — 순수 PC 4.375 (세 가지 · = 35/8 · `/0.229` = 4.366812 은 틀린 식) · 순수 SC 1 · 혼합 FULL Hertz 3.154656902 · Physics 3.124849017 · CF 2.384829644 · 협착만 3.288178778 · 전위 변화 최대 0.198 V (1 V 인가) ⇒ 섞인 침대는 배율로 못 바꾼다.
- **소비자 계약** — 기준값을 0.0041 로 바꾼 동안 `tau_flux.sigma0_binding_problems` = 0 · 0.05 로 되돌리면 전자 증서 셋 거부 (두 모드) ⇒ 실행 중 교체한 값을 원 생산물인 척 게시하면 안 된다 (`PS45E-03`).
- **실제 다섯 침대 (PC 인자 ON 그대로 · 저장된 증서 `I_bottom / ΔV × g_to_q` 에서 q 재구성 · 새 풀이 아님)** — σ_ref 4.1 이면 Hertz 0.390802 · 0.235799 · 0.158887 · 0.108846 · 0.106783 · Physics 0.507671 · 0.319762 · 0.220523 · 0.154004 · 0.137301 mS/cm (0:10 → 10:0) · 전자 간선 8,970 · 5,794 · 3,878 · 2,208 · 733 **전부 `native_unsupported_pair`** (`PS45E-02`) · 끝점 산술 (인자 끔 · 균일 반경 PC 만 · 정상 간선 조건) Hertz SC 0.390802 · PC 0.467175 (PC/SC 0.27324 → 1.19543) · Physics 0.507671 · 0.600692.

## 3. 독립 대조 — AM 고체 부피분율 (`_repro_ours_20261013/ps45_solid_fraction_check.py` · Codex 탐침과 다른 길)

- 덱은 템플릿 줄을 통째로 읽어 type ↔ 밀도 ↔ 반경 변수를 한 줄에서 묶고 질량 가중은 `particledistribution/discrete` 쌍에서 · **SE 는 SE scaffold 행** (입자마다 반경 — Codex 묶음에 없던 파일 · Codex 는 SE 개수 × 덱 반경) · AM 은 AM scaffold 행 · 개수는 망 표 `dump_type_counts` 와 대조만.

| PC:SC | 케이스 | 덱 명목 (0.816 : 0.184 · 4.8 / 2.0 g/cm³) | 같은 질량 · 4.85 / 1.64 | scaffold 구 체적 AM / (AM + SE) | 개수 = 덤프 | 질량 되짚기 (덱 밀도 · 4.85/1.64) |
|---|---|---|---|---|---|---|
| 0:10 | 260925_000001_0bee25 | 64.8855 % | 59.9935 % | 64.9065 % | ✓ | 81.61 · 84.54 wt% |
| 3:7 | 260925_000448_bd85f9 | 64.8855 % | 59.9935 % | 64.9025 % | ✓ | 81.61 · 84.54 wt% |
| 5:5 | 260925_000513_123978 | 64.8855 % | 59.9935 % | 64.7077 % | ✓ | 81.48 · 84.43 wt% |
| 7:3 | 260925_000559_082983 | 64.8855 % | 59.9935 % | 64.7937 % | ✓ | 81.54 · 84.48 wt% |
| 10:0 | 260922_222828_6e4ff6 | 64.8855 % | 59.9935 % | 64.9201 % | ✓ | 81.62 · 84.55 wt% |

- Codex 값과 차 ≤ 1.5e-13 (합산 순서) · SE 반경 다섯 침대 전부 0.5 µm · scaffold 머리 케이스 ID = 망 표 5 / 5 (`solid_fraction_check.json`).
- ⇒ 판정문 §5-1 *"64.7077–64.9201 %"* 재현 · 요청서 · README 의 *"NCM 고체 기준 60 vol%"* = 덱 p11 표 밀도 4.85 / 1.64 로 낸 다른 규약 (실행 덱 밀도 아님 · 같은 기하에 4.85 / 1.64 를 붙이면 질량 84.4–84.6 wt% 가 돼 81.6 wt% 침대가 아니다) — `PS45E-01` · `SELF-108`.
- 한정 (Codex 와 같음): 구 체적 = 겹침 합집합 · 변형 입자 부피 · 실험 상 부피가 아니다.  상자 기준 AM 분율 (52.5–55.1 %) · Minnmann 전체 부피 기준 (61 vol% = 고체 약 70.9 %) 과 섞지 않는다.

## 4. 재현 명령 (리포 루트에서)

```bash
R=$(mktemp -d) && mkdir -p "$R/ps45_sigmae_review_20261013/evidence"
cp -r docs/reviews/codex_ps45_sigmae_reporting_evidence_20261013/probes "$R/ps45_sigmae_review_20261013/"
ln -s "$PWD" "$R/ps45_sigmae_review_20261013/source"          # 작업 트리 = 확인할 커밋 (깨끗한 체크아웃)
git show 0801d4ceb:scripts/network_conductivity.py > "$R/ps45_sigmae_review_20261013/evidence/network_conductivity_run0801.py"
( cd "$R" && for p in code_scaling composition_basis; do python3 -I -B ps45_sigmae_review_20261013/probes/$p.py > $p.json; done \
          && python3 -I -B ps45_sigmae_review_20261013/probes/report_arithmetic.py > /dev/null )
E=docs/reviews/codex_ps45_sigmae_reporting_evidence_20261013
python3 -I $E/_repro_ours_20261013/compare_probe_outputs.py "$R/compare.json" \
  $E/evidence/code_scaling.json="$R/code_scaling.json" \
  $E/evidence/report_arithmetic.json="$R/ps45_sigmae_review_20261013/evidence/report_arithmetic.json" \
  $E/evidence/composition_basis.json="$R/composition_basis.json"          # rc 0 = 판정값 차이 0
python3 -I $E/_repro_ours_20261013/ps45_solid_fraction_check.py . "$R/solid.json"
python3 -I $E/_repro_ours_20261013/compare_probe_outputs.py --selftest      # 19/19
```

- 한정: Codex 탐침 재현 (합성 망 · 저장 증서 재구성 · 조성 산술) 이다 — 실침대 인자 끔 다섯 망은 Codex 도 우리도 안 풀었다 (원자 · 접촉 원자료가 1저자 WSL 에만 있다) · `verify_review.py` 는 Codex 스냅샷 해시를 단언하므로 우리 트리 (CLAUDE.md · 원장 · README 가 그 뒤 바뀜) 에 그대로 쓰지 않았다.

## 5. 다음

- 원장 `PS45E-01` · `02` · `03` (P2 · open) · `SELF-108` (60 % 규약) · `SELF-109` (전자 Physics 를 Tabor 로 표기).
- 우리 문서 고침 (수치 무변경): `docs/data/ps45_r45_network_g2_20261007/README.md` §σ_e (고체 64.7–64.9 % · Physics 표기 · 선택지 (가′) · (나) · (다)) · 요청서 머리 표지 · 전자 열 표지 (`make_sigma_tabor_figs.py` · `sigma_tabor_g2.csv`).
- 인자 끔 다섯 망 진단 = 결과 전 등록 `docs/reviews/ps45_sigmae_factor_off_registration_20261013.md` + 보고 전용 실행기 `scripts/ps45_sigmae_factor_off_variant.py` (봉인 파일 무변경 · 별도 출력 · manifest) → 1저자 WSL.
