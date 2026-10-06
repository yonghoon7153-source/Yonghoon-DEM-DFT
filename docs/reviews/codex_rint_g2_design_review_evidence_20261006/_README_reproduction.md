# Codex Rint 2단계 G2 (면적 규약 ①′ v2 설계) 재검토 — 반입 · 우리 트리 재현 (2026-10-06)

- 판정문: `docs/reviews/codex_review_rint_g2_design_20261006.md` (= zip 의 같은 이름 파일 · 바이트 그대로 · 289 행 · 31,981 B) — **G2 설계 완결 HOLD** · 새 P2 6 · P3 4 · 새 생산 P1 입증 없음 · 검증 도구 · 합성 실패 시험 · 접촉 census 개발은 진행 가능 · ①′ 정량 채택 · ② 생산 진입은 조건 해제 뒤 (판정문 §0 · Q13).
- 받은 묶음: codex_rint_g2_design_review_20261006.zip (1저자 전달 · 업로드 이름 a1788d6b-codex_rint_g2_design_review_20261006.zip) · 207,134 B · sha256 d5414b6cf6098a4c96d044ebe1c0a8a4155f8906fb7bdea907b74b3429cefc89 · 15 항목 (정규 파일만 · 디렉터리 항목 · 경로 탈출 없음) · 묶음 안 bundle_manifest.json 의 14 항목 sha256 · 크기 14/14 일치.
- 원장: Codex 표기 `RINTG2-01`~`10` 은 원장 ID 형식 (`scripts/check_review_findings.py` 의 `ID_RE` — 하이픈 앞 최대 5 자) 을 넘는다 (`RINTG2` = 6 자) → 원장 `RINTG-01`~`10` (open · 제목 머리에 "(Codex 표기 RINTG2-NN)") · 기존 `RINT-06` · `07` · `08` · `09` · `10` · `15` · `16` · `21` 에는 판정문 Q12 판정을 note 로만 덧붙인다 (상태 그대로).
- 핀: `c859b9d08b98edf41d3fdc47e3ba202875c8ab97` (요청서 커밋) — 아래 8 파일 8/8 같다.

## 묶음 15 항목과 처리

| zip 항목 | B | sha256 (앞) | 처리 |
|---|---:|---|---|
| codex_review_rint_g2_design_20261006.md | 31,981 | ffbdabb5… | → `docs/reviews/codex_review_rint_g2_design_20261006.md` (바이트 그대로) |
| probe_design.py | 7,503 | 53397815… | → 이 폴더 (바이트 그대로) |
| evidence.json | 6,521 | cd4f06f1… | → 이 폴더 (Codex 원본 · Windows 실행 · 우리 재현값은 아래 표) |
| source_manifest.json | 1,149 | d6fc0a5b… | → 이 폴더 (핀 · 8 파일 Git blob) |
| README.md (묶음 설명) | 2,691 | 02a3577d… | 안 넣음 — 요지는 아래 재현 · 한정에 옮김 |
| build_bundle.py | 2,108 | de9821c0… | 안 넣음 — 포장 · 해시 · 숫자 대조 도구 (Codex: 과학 검사기 아님) |
| bundle_manifest.json | 2,618 | cc3b2132… | 안 넣음 — 위 14 항목 sha256 · 크기 |
| source/ 8 파일 (문서 5 · 코드 3) | 481,962 | 각 sha256 = `evidence.json` 의 `source_verification` | 안 넣음 — 우리 리포 파일 사본 · 핀 blob 과 같다 (아래 표의 blob id 로 복원) |

## 핀 대조 — zip source/ 사본 = 핀 blob 8/8

zip 사본의 바이트에서 Git blob 을 다시 계산해 `source_manifest.json` 과 `git rev-parse <핀>:<경로>` 둘에 대조했다.  HEAD 칸 = 재현 시점 브랜치 끝 (로컬 db74ea98 · 이 8 파일은 origin `d3b037136` 과 같다).

| 파일 | 핀 git blob (= manifest = zip 사본) | HEAD |
|---|---|---|
| `docs/reviews/contact_resistance_pipeline_draft_v2_20261006.md` | blob `1992522fd152d387daba84fe2b7200ae6e07985c` | blob `c71c6bc33ab637ca43a41c55bfdedec2974cb600` — `a33ac26b1` 의 L158 한 줄 (T1 픽스처 증거 경로를 리포 경로로 정정 · 판정문 §0 이 적고 고정본 기준으로 심사) |
| `docs/reviews/contact_resistance_pipeline_draft_20261002.md` | blob `a77ad9a925e8d8cb47e9a46a31d3a8560649bb81` | 같음 |
| `docs/reviews/codex_review_rint_g1_lhs_network_20261005.md` | blob `01bf8dbdff76aa794d562e6330b9d2ccf9b93912` | 같음 |
| `docs/reviews/codex_review_rgl_reverify_20261005.md` | blob `50f081a8d373449268ac34f4c9bdc6f9be610c72` | 같음 |
| `scripts/step3_sigma.py` | blob `4b33c7a4526f2d55dfbdefa3257e36619a9e4136` | 같음 |
| `scripts/lens_geometry.py` | blob `53a20c31554740957c21a0fa52362df0b000cc97` | 같음 |
| `scripts/se_material.py` | blob `506caca0f8744ee89836a026685f0730ef478f94` | 같음 |
| `docs/reviews/codex_rint_g2_request_20261006.md` | blob `7a99b6c0ab6b4cf3a23913f1c3eba9c621313b5f` | 같음 |

⇒ 계산에 쓰이는 코드 세 파일은 핀과 HEAD 가 같다.  핀 이후 바뀐 것은 v2 초안 한 줄뿐이다.

## 우리 트리 재현 — 탐침 무변경 (Linux · Python 3.11.15 · NumPy 2.4.6 · SciPy 1.17.1)

- 실행: zip 의 `probe_design.py` 바이트 그대로의 사본을 리포 밖 빈 폴더 셋에서 `python3 -I -B` · OMP/OPENBLAS/MKL 스레드 1.  source/ 는 zip 사본이 아니라 **리포의 git blob** (`git cat-file blob`) 으로 채웠다 (핀 폴더의 source/ 는 zip 사본과 바이트 동일).
- 솔버 경로: CPU Jacobi-CG (`GPU_SOLVE` · `AMG_SOLVE` 기본 False · pyamg · cupy 없음) — Codex 와 같은 경로.  Codex 환경 = Windows · Python 3.12.14 · NumPy 2.3.5 · SciPy 1.16.3 · BLAS/OMP 스레드 1.
- 탐침이 쓴 파일은 각 폴더의 evidence.json 하나뿐 (실행 전후 파일 목록 대조) · stdout = evidence.json 내용.

| 실행 | source/ · manifest | rc | 대조 |
|---|---|---|---|
| 핀 | 핀 blob 8 · zip manifest 그대로 | 0 | Codex `evidence.json` 과 숫자 키 92 중 **87 비트 동일** · 나머지 5 = CG 끝자리 (아래) · 목록 원소 숫자 5 (`permutation` 4 · `actual_function_g_code` 1) 도 같다 · 문자열 차이 = 환경 3 칸 (python · numpy · scipy) 뿐 |
| HEAD | HEAD blob 8 · manifest 를 HEAD blob 으로 다시 만듦 (v2 초안 행만 다르다) | 0 | 핀 재실행과 숫자 97/97 비트 동일 · 다른 것 = `source_verification[0]` 의 v2 초안 blob · sha256 (L158) 뿐 · Codex 와는 핀과 같은 87/92 · 같은 5 |
| 음성 대조 | HEAD blob 8 · zip (핀) manifest | 1 | 첫 단계 AssertionError — v2 초안 blob `c71c6bc33ab637ca43a41c55bfdedec2974cb600` ≠ manifest blob `1992522fd152d387daba84fe2b7200ae6e07985c` (탐침의 blob 검사가 바뀐 파일 하나를 실제로 잡는다 · evidence.json 안 씀) |

Codex 와 다른 5 키 (핀 · HEAD 같음) — 전부 `actual_raster_order` 의 반복 솔브 끝자리다:

| 키 | Codex | 우리 | 상대차 |
|---|---:|---:|---:|
| `rows[0].sigma_eff_S_cm` | 0.0017728521965377632 | 0.0017728521965377382 | 1.4e-14 |
| `rows[1].sigma_eff_S_cm` | 0.0018568975000462676 | 0.001856897500046274 | 3.5e-15 |
| `relative_sigma_change` | 0.04740683045808214 | 0.04740683045810057 | 3.9e-13 |
| `rows[0].resid` | 9.929196490428454e-09 | 9.945726403974921e-09 | 1.7e-3 |
| `rows[1].resid` | 9.801807272078137e-09 | 9.828538600982548e-09 | 2.7e-3 |

두 팔 모두 `cg_info` 0 · `unconverged` False · 잔차 < rtol 1e-8 그대로 · 순열 σ 변화는 판정문의 +4.740683 % 그대로 (유효 11 자리까지 같다).

**sid 16 셀의 자리** (실제 `rasterize` · 핀 blob · 별도 확인): 바뀐 16 셀은 전부 z = 1.95 µm 한 층 — 두 구 (중심 z 1 · 2.9 µm · R 1 µm · 겹침 0.1 µm) **모두의 안 (겹침 렌즈)** 이고 브리지 공 (0.24 µm) 밖 · xy 반경 0.255–0.292 µm.  렌즈 셀 32 중 16 은 브리지 (혼합 쌍 = AM_P · sid 2) 가 두 순서 모두 덮고, 나머지 16 이 `_ball` 의 나중 입자를 따라 [0,1] = sid 2 (AM_P 가 나중) ↔ [1,0] = sid 1 (AM_S 가 나중) 로 바뀐다 → sid1 4172 → 4188 · sid2 4244 → 4228 (±16 · evidence 와 같다).

## 판정의 핵심 값 — 우리 핀 재실행에서 읽은 값

| 원장 (Codex 표기) | 양 | 우리 재현 |
|---|---|---|
| `RINTG-01` (RINTG2-01) | σ_OFF [0,1] / [1,0] · 변화 · 바뀐 sid 셀 | 0.0017728521965377382 / 0.001856897500046274 S/cm · +4.740683 % · 16 |
| `RINTG-02` (RINTG2-02) | a · A_true (`intersection_disc_area` 같음) · P_true/G · P_spread/G · 차 | 0.141067359797 µm · 0.0625176938064 µm² · 1.0796 · 1.2304 · +13.968136 % |
| `RINTG-02` | 2 Ω 패치 둘 병렬 · 하나 제거 · 전 면적을 남은 패치에 재정규화 | 1 · 2 · 1 Ω |
| `RINTG-03` (RINTG2-03) | `interface_face_g` · 문서식 몫 · 올바른 몫 · 중심 로그 FD · 비 | 0.00032679738562091506 · 0.0334640522875817 · 0.8366013071895424 · 0.8366013071636756 · 24.999999999999996 (25 배) |
| `RINTG-03` | 직렬 bulk 3 · A 1 · B 2 Ω — 전체 로그비 · A 만 적분 | −0.6931471805599453 · −0.23104906018664842 |
| `RINTG-04` (RINTG2-04) | β 맞음 / 막 삭제 · β 오차 · 차/f (L/a 5 → 80) | −0.03125 / 0.75 · 0.78125 · 2.357308 → 2.343753 |
| `RINTG-05` (RINTG2-05) | support/참 원판 면적비 (b 0.24 · a 0.1411 µm) | 2.894472361809041 |
| `RINTG-08` (RINTG2-08) | 올바른 경계 · 문자식 경계 · 거리 2.12 µm 접촉 판정 | 2.075 · 2.15 µm · False / True |
| `RINTG-09` (RINTG2-09) | 면 G (반셀 0.0001 Ω 포함) · 직접 G | 0.00999999000001 · 0.01 S |
| Q1 | 근축면 · 브리지 중심 · 차 (R 6 · 2 µm · δ 0.05 µm) | 5.987578616352201 · 5.975 · 0.0125786163522017 µm |
| Q6 | J_n 양쪽 · jump · r·J_n | −6.4 / −6.400000000000001 · −0.6400000000000001 · −0.6400000000000001 |

## 다시 돌리는 법

⚠ 이 폴더에서 직접 돌리지 말 것 — 탐침은 자기 옆 evidence.json 을 덮어쓰고 (Codex 원본이 사라진다), 이 폴더에는 source/ 가 없어 import 도 실패한다.

```bash
# 리포 루트에서.  RUN = 리포 밖 빈 폴더.
PIN=c859b9d08b98edf41d3fdc47e3ba202875c8ab97
E=docs/reviews/codex_rint_g2_design_review_evidence_20261006
RUN=$(mktemp -d)
cp "$E/probe_design.py" "$E/source_manifest.json" "$RUN/"
python3 -I -B -c 'import json,sys; [print(r["path"]) for r in json.load(open(sys.argv[1]))["files"]]' "$E/source_manifest.json" |
while read -r p; do mkdir -p "$RUN/source/$(dirname "$p")"; git cat-file blob "$PIN:$p" > "$RUN/source/$p"; done
(cd "$RUN" && OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -I -B probe_design.py > stdout.txt); echo "rc=$?"
# Codex 값과 대조 (숫자 키 = 사전 키에 달린 int/float · bool 제외)
python3 -I -B - "$E/evidence.json" "$RUN/evidence.json" <<'EOF'
import json, sys
def flat(x, p=''):
    if isinstance(x, dict):
        for k, v in x.items(): yield from flat(v, f'{p}.{k}' if p else k)
    elif isinstance(x, list):
        for i, v in enumerate(x): yield from flat(v, f'{p}[{i}]')
    else: yield p, x
a, b = (dict(flat(json.load(open(f, encoding='utf8')))) for f in sys.argv[1:3])
num = [k for k, v in a.items() if isinstance(v, (int, float)) and not isinstance(v, bool) and not k.endswith(']')]
print(len(num), 'numeric keys,', sum(a[k] == b[k] for k in num), 'bit-identical')
for k in a:
    if a[k] != b[k]: print(' ', k, a[k], '->', b[k])
EOF
```

HEAD 로 돌리려면 `PIN=HEAD` 로 두고, 복사한 manifest 의 `git_blob` 을 `git rev-parse HEAD:<경로>` 로 바꿔 쓴다 (v2 초안 행만 바뀐다 · 그대로 두면 위 음성 대조처럼 AssertionError).

## 한정 (Codex 그대로)

- 합성 입력 · 해석식 · 작은 FV 솔브다 — 새 ①′ 구현의 통합 시험이 아니다 (v2 는 아직 설계).  rc 0 은 수치가 기록됐다는 뜻이지 v2 시험 PASS 가 아니다.
- Codex 미실행: 실침대 · MPM · GPU · 194 재실행 · 새 r2 구현 · T2/T3 고운 격자 해 · 물성 원문 전수 조사 · 기존 T1-2 두 구 막 fixture 전체 재현 (0.6474 / 0.6999 등은 이번 신규 실측 목록이 아니다).
- 묶음 README 의 기록: 리뷰 도중 탐침의 `interface_face_g` 인자를 잘못 준 첫 호출이 TypeError 로 멈춰 탐침 호출 인자만 고쳤고, 솔버 잔차 키를 실제 반환 키 `resid` 로 맞춘 뒤 전체를 종료코드 0 으로 다시 돌렸다 — 생산 소스는 무수정 (blob 대조가 확인).
- `HOLD` 는 설계 완결 · 정량 채택 판정이다 — 반례 시험 개발 금지가 아니고, 원장 상태나 생산 코드를 자동으로 바꾸지 않는다.  판정문 안 GitHub 링크는 핀 고정이다.
