# Codex 판정 반입 — 50kg 4차년도 DEM 보고 초안 2 (11-01) = 조건부 수용 · D0.7 = §6 수동 조건의 한 건 GO

- 받은 ZIP (1저자 11-01): 업로드 이름 4336c781-codex_kg50_y4_draft2_review_20261101.zip · 13,261,008 B · sha256 043c6207297bc49a73d59a6c5dd88afe57a875438edaed17c1e329cec2a6f066 · 멤버 304 (전부 일반 파일 · 절대 경로 · `..` · 링크 0 · 세션 스크래치에 `python3 -I` zipfile 로 풂) · ZIP 의 MANIFEST.sha256 303 줄 = 받은 바이트 그대로 일치 (`sha256sum -c` 303/303) — ZIP 자체는 리포 밖.
- 리뷰 핀 = 065ad7004c8f970243951d366e3ced8c28af9197 (claude/stoic-knuth-NObVQ · 커밋 `065ad7004`) · 검토한 우리 요청 ZIP = codex-kg50-report-y4-draft2-065ad7004.zip · sha256 0851437db6d1893ba80699718fb115b99f9bb2aff870bec3e73f1b602b6b1c30 (evidence/packaging.json · evidence/intake.json) · 요청서 = `docs/50kg/report_y4/codex_kg50_y4_draft2_request_20261031.md`.
- 판정문 = `codex_review_kg50_y4_draft2_20261101.md` (ZIP 바이트 그대로 · sha256 0ffa8b52ee6b75466f5e673197cbaa0dc31725f54ee2f41cdd877615a705785e).  부속 상세 = evidence/guard_review/Q4_guard_review_20261101.md · evidence/physics_review/physics_registration_literature_review.md · evidence/figures_review/figures_content_review.md.
- 리뷰어가 실행하지 않은 것 (판정문 머리 · packaging.json): DEM · 수송망 solve · WSL · Slurm 제출 / 취소 · Bash 끝-끝 (Windows 초기화 오류) — 지킴이 실패 경로는 소스에 결속한 독립 제어 흐름 모형.

## 판정 (판정문 §1 · §8)

| 대상 | 판정 |
|---|---|
| 초안 2 | **조건부 수용 · 새 P1 없음** — 새 지적 P2 5 · P3 3 · 발표 전에 감쇠의 인과 · 상한 설명과 수송 인자 f 의 기준을 고칠 것 |
| D0.7 | **§6 수동 확인 조건을 유지하는 한 건 조건부 GO** · 지킴이 v2 단독의 무인 차단 · 실패 감시 보장 = **HOLD** · dt · 감쇠 물리 자격화 · 입도 효과 판정 · 압축 체크포인트 재개 = 승인 아님 |
| `K50Y4-02` · `K50Y4-03` | **닫힘** (1.35 GPa 최소 한정문 반영 · 발표 9쪽 정정 + 발췌 일치) |
| `K50Y4-01` | **부분 · 열림 유지** — 프레임 규칙 방향 수용 · 실제 재고 · 분석 계획 · 같은 물리 상태 미종결 |
| 수정 계획 #1–#12 | 내용 반영 충족 (새 f 정의 문제는 별도 = KG50Y4D2-03) |
| D1 원자료 → 주요 지표 / 그림 | 범위 안 수용 (원자료 · AM별 CSV 대조 7,445 항 · 그림 · JSON · CSV 대조 23,436 항 불일치 0 = 반복 행별 대조 수 · 독립 물리 시험 수 아님) |
| `KG50-20` · `KG50-04` · `DEMP-01` | 기존 열림 유지 (이번 검토로 물리 결함을 닫지 않음) |
| D0.7 승인값 전사 | 수용 (수령 기록 사이 15/15 · 서버 실물 인증과 구분) |
| 한 건 뒤 완주 · 5 일 안 종료 · 압축 재개 | 미보증 / 별도 검토 (D2 꼴 5.035 일 = 5 일보다 약 50.6 분 김) |

## 새 지적 ↔ 원장 (원장 ID = `K5D2-NN` · Codex 표기 KG50Y4D2-NN · 커밋 · 시트 표기 K50Y4D2-NN · ID 형식 = 앞부분 5 자 이내)

| 원장 | Codex · 부속 | 등급 · 상태 (11-01) | 무엇 |
|---|---|---|---|
| `K5D2-01` | KG50Y4D2-01 · PHY-01 · PHY-03 | P2 · claimed_fixed `c3714b547` | R_aff = γNv/(2A) = affine 가정의 감쇠 저항 규모 기준선 — 낙폭의 일반 상한 · 예측 아님 · D3 의 1.21 배는 감쇠 밖 기전의 증거 아님 (스프링–입자 묶음–스프링 반례 α 0.777007) · ⅔ = 이상화 조건에서만 · 등록 182.4/24.2/8.32 MPa = 결과 전 drag 상당압 |
| `K5D2-02` | KG50Y4D2-02 · PHY-02 | P2 · **open** | 등록 R5_abs (절댓값 합) ↔ R_drag_signed = D_z/F_top (부호 합) 분리 — 글은 `c3714b547` 에서 나눔 · 닫힘 조건 = 판독기가 두 값을 따로 출력 (scripts/kg50_q5_verdict.py 는 절댓값 합 하나만) |
| `K5D2-03` | KG50Y4D2-03 · figures P2 | P2 · claimed_fixed `c3714b547` | 보고 f = f_mc = f_gap × L_gap/L_mc (두께 재척도 · 새 망 해 아님) · 표지 · 식 · τ 연결 확인 · 남은 것 = 노트의 '자기상사 가정' 구절 (닫힘 조건 밖) |
| `K5D2-04` | KG50Y4D2-04 · Q4G-01 | P2 · **open** | 지킴이 v2 — 취소 요청 뒤 실제 차단 (시험 끝 · 같은 시도의 본 job) 미확인 · 이번 한 건 = §6 (a) 2 사람 확인 |
| `K5D2-05` | KG50Y4D2-05 · Q4G-02 | P2 · **open** | 지킴이 v2 — 신원 줄 전 실패 = 조용한 영구 대기 · 이번 한 건 = §6 (a) 3 별도 읽기 전용 상태 확인 |
| `K5D2-06` | KG50Y4D2-06 · figures P3 | P3 · claimed_fixed `c3714b547` | 그림 검사 = 현재 입력의 도형 · 문자 범위 / 겹침 검사 (입력 무결성 인증 아님) · 남은 것 = D0.7 자동 소비 전 JSON + CSV 결합 검사 |
| `K5D2-07` | KG50Y4D2-07 · LIT-01 | P3 · claimed_fixed `c3714b547` | 문헌 화살표 = 선택한 6편의 실험 · 모델 · Bazzoun 2026 · Shi 2019 = 모델 |
| `K5D2-08` | KG50Y4D2-08 · LIT-02 | P3 · claimed_fixed `c3714b547` | Tron 2023 약 36 % = 별도 조성 시험 (AM:SE 70:30→85:15 wt% · 그림 판독 · 성형 300 MPa · 측정 10 MPa) · 입도 효과 수치 아님 |

- 기존 항목: `K50Y4-02` · `K50Y4-03` → verified (claimed_fixed `ec460457d` = 초안 2 글 시트 136 · 137 행 · verified_sha = 리뷰 핀 · verified_by codex · verified_scope = 판정문 §1 표 · §4 Q1 인용) · `K50Y4-01` = open 그대로 + partial_note (남은 것) · `KG50-20` = open 그대로 · 제목 · note 문구만 판정문대로 (기준선 = 상한이 아님 · ⅔ 는 이상화 조건에서만 · D3 비의 해석 · 등록값 = 결과 전 drag 상당압 · 부호 합 ↔ 등록 R5_abs 분리 · ε 0.00085419 %p = 구 부피 항뿐).
- 원장 914 → **922** (claimed_fixed 346 → 351 · verified 242 → 244 · open 316 → 317 · wontfix 10).
- claimed_fixed 의 자리 확인 (11-01 반입 때 · 커밋 `c3714b547` 의 글 → 초안 3 `5a2595b54` · 시트 §0-3 자리 대조): 초안 2 · 3 글 시트 · 초안 2 README · D1 README · 생성기 표지 · 그림 SVG / CSV 에서 각 고친 문구 확인 · 기준선에 붙은 '상한' 은 부정문과 '하지 않을 말' 에만 (초안 3 0쪽의 접선 마찰 상한 μF_n 은 무관한 뜻) · 줄 번호 = 원장 evidence_tests.
- 지킴이 · 재개 도구 · R5 판독기 (docs/50kg/d07_guard/ · scripts/resume_ckpt.sh · scripts/kg50_q5_verdict.py) = 리뷰 핀 뒤 변경 없음 (`git log 065ad7004..ae1f64b93` 빔) → K5D2-02 · 04 · 05 open.

## 우리 확인 (11-01 반입 · 작업 트리 · 리뷰어 탐침은 읽기만 · 실행 안 함)

| 무엇 | 결과 |
|---|---|
| ZIP 안전 · 매니페스트 | 멤버 304 일반 파일 · 경로 이탈 0 · MANIFEST.sha256 303/303 |
| 리뷰어의 repo 사본 ↔ 우리 git (리뷰 핀) | evidence/source/repo 229/229 바이트 같음 · evidence/remote 12 중 10 같음 · 2 (remote/docs/sulfide_se_mechanical_anchors.md · remote/docs/data/kg50_decks_20261026_v2/manifest.json) = 끝 줄바꿈 하나 더 (내용 같음 · 리뷰어 remote_blob_metadata.json 의 blob id = 핀 blob 231d1befd3e5… · 85a7670b6f2a…) |
| f 표 (KG50Y4D2-03) | 우리 data/D1–D3/metrics_*.json tau_flux_row: f_gap × L_gap/L_mc = f_mc (세 침대 · 상대 차 < 1e-15) · D1/D3 비 f_mc 2.398620 · 2.132917 · f_gap 2.332935 · 2.074508 = 판정문과 같음 |
| 해석적 반례 (KG50Y4D2-01) | α = √(Δp/(2R_aff)) = 0.7770070 · k_t/k_b = 3.4844459 · 2α²R_aff = 9.25654 MPa · D3 비 1.2074798 · 초과 1.59054 MPa = 판정문과 같음 (우리 산술 · 리뷰어 analytic_probe.py 는 안 돌림) |
| 부호 합 / 절댓값 합 (KG50Y4D2-02) | v_z = (−0.01, +0.01) · γ 0.5 → 0 / 0.01 = 같음 |
| ε 소실 항 · 5 일 산술 | SE 5 개 0.00085419 %p · (200000+C+100000)/31570/24 = 3.412 · 5.035 · 5.774 일 · 1.07–1.19 배 3.623–3.985 · 5.360–5.917 · 6.151–6.796 일 · D2 꼴 5 일 초과 50.55 분 = 판정문과 같음 |
| 다시 하지 않은 것 | D1 원 덤프 재계산 (7,445 항) · 그림 대조 23,436 항 · 소비자 selftest 9/9 · PNG 13 육안 · 지킴이 모형 · 승인값 15/15 · Q6 문헌 원문 대조 — 리뷰어 기록만 반입 |

## 반입 때 짚은 것 (판정문 대조)

- `K5D2-02` 는 글 고침만으로 닫히지 않는다 — 판정문 닫힘 조건 = *"정의가 분리되고 판독기가 두 값을 따로 출력하면 닫힘"* (§8 2 행 = 정의 · 출력 분리) → open (partial_note).
- `K5D2-03` 의 판정 요지 = 보고 f 가 이미 f_mc 인데 화면이 '원 솔버 σ' 라고 설명한 것 (값은 그대로 · 표지만) — f 를 f_mc 로 바꾸라는 뜻이 아님.
- `K5D2-06` 의 최소 해결 둘째 문장 (D0.7 자료 자동 소비 전 JSON + companion CSV 의 출처 · case · step · 상태 · 유한성 결합 검사) = 아직 없음 (그 소비의 선행 조건으로 남김).
- 판정문 §6 (b): 요청서 · `-T` 기록의 *"G0–G3 통과"* = 정확히 G0 · G1 · G2 통과 · G3 = 비교 구간 원 로그 없음으로 생략 (도구 보고 문구를 그대로 옮긴 것) · 판 높이 일치 ≠ 입자 상태 전체 동일 · 새 `-T` 의 전체 stdout · 생성 덱 · 바이너리 · 체크포인트 실물은 미제공 → 승인값 = 수령 기록 사이 일치만.  원장 등재 안 함 (1저자 판단 몫).
- 판정문 §6 (a) 한 건 운영 조건 다섯 (NP 56 · r56/main1031 · 고정 after_settling 체크포인트 · 도구 · 승인값 · 영수증 대조 · 불일치 · 지연이면 본 job 유무 · 최종 종료까지 사람이 확인 · 결과 / 신원 줄 없을 때 별도 읽기 전용 상태 확인 · 끝 압력 · 낙폭 · R5_abs / signed drag 기록 · TIMEOUT / 미완주 처리와 원본 보존 경로를 미리 정함 · 압축 체크포인트 재개 우회 금지).
- 판정문 §5 (b): 보고 문구 *"정적 압력"* → *"이완 끝 판 압력"* (수렴 인증 없음) · §5 (c): 압축 덤프의 직접 drag 진단 = 다음 독립 확인 (R5_abs 와 signed drag 둘 다 · 말기 여러 프레임 추세 · 정지값으로 대체 금지 · D_z ≈ ΔP·A 만으로 원인 확정 아님).
- Q6 문헌: 리뷰어도 원문 숫자 재현을 못 한 것 = Yano 그림 수치 · Lin 3.28 · Kawaguchi SI 2.33 · Yadav 전문 · Tron −36 % digitize (부속 physics_review §Q6) · Stavola SI Table S8 산술 9.19143 · 8.43445 = 재현.
- 묶음 상대 경로 5 개 = `docs/reviews/doc_refs_allowlist.tsv` 에 external (sha256) 로 등재 (판정문의 evidence/ 기준 경로 넷 + 부속 physics_review 의 초안 2 폴더 기준 figs/ 경로 하나).

## 반입 범위

| 넣음 | 뺌 (이유) |
|---|---|
| 판정문 · MANIFEST.sha256 · evidence/ 의 작은 글 파일 (REPRODUCE.md · intake.json · packaging.json · prepare_input.py · raw_probe.py · remote_blob_verification.json · figures_review/ 9 · guard_review/ 15 · independent/ 4 · physics_review/ 4 · remote/source_blob_refs.json · source/ 의 PIN.txt · MANIFEST.sha256 · evidence/ledger_rows.json · evidence/report_20261001_page_with_1p35GPa.txt) = 45 파일 · 바이트 그대로 | evidence/source/repo/ 229 (= 리뷰 핀 git blob · 그림 · PDF · PPTX · OVITO · 로그 포함) · evidence/source/ 의 요청서 (= 리포 파일) · evidence/remote/ 보충 사본 12 · evidence/physics_review/cards/ 14 (litdb 정본 카드 사본) · 큰 기계 대조 기록 3 (independent/checks.json · figures_review/figure_numeric_audit.json · remote_blob_metadata.json) |

- 이 폴더 `.gitattributes` = `* -text` (줄 끝 변환 안 함 · 같은 꼴 = 반입 폴더 9 곳) → CRLF 파일 27 개도 MANIFEST.sha256 값 그대로 (아래 표의 (CRLF) 표지).  README_import.md 는 우리 글 (LF).
- 바로 다시 받기 = 받은 ZIP (리포 밖 · sha256 위) · 뺀 멤버 = 아래 표의 sha256 로 대조.

## 멤버 전체 (304 · sha256 = ZIP 안 바이트)

### 넣음 (45)

| 멤버 | 바이트 | sha256 |
|---|---:|---|
| codex_review_kg50_y4_draft2_20261101.md | 27188 | 0ffa8b52ee6b75466f5e673197cbaa0dc31725f54ee2f41cdd877615a705785e |
| evidence/intake.json (CRLF) | 66668 | 8410d50010af0b2fa8faf1a18d674cf2b2479b932844e1803c7649ec31f05320 |
| evidence/packaging.json (CRLF) | 868 | cf5780bf7e11ea4903838fb6a966cf9bcc3f9ef1ddedcdebf1eb078b2e7078df |
| evidence/prepare_input.py (CRLF) | 705 | 7d275411a36f6f7ae0328597c40bbcee4bbbaf9c336780a467345322cc1ef8a3 |
| evidence/raw_probe.py | 9473 | e1e9e064ed9972c44ebdb3f9b3f49d42ae9baec4ac94743dd333a39dde9a85c9 |
| evidence/remote_blob_verification.json (CRLF) | 53 | 7b9093e3ae78a6817dbda3f6169dd77df6d89a1a989c0627169d1c061e9afef3 |
| evidence/REPRODUCE.md (CRLF) | 3471 | ec36b0d419e14999295f44da7f8e26a84b19c15b4fcdf7ac190157257a51f0c5 |
| evidence/figures_review/audit_figures.py (CRLF) | 9948 | 9954cc59146501782e71138c5924036dfc213bfa9da15a088fd96e9bd5cae175 |
| evidence/figures_review/audit_figures_stdout.txt (CRLF) | 4304 | 21897dee451c34e898626ab8e0396dbbf993a422449c41f110679495ae9c0054 |
| evidence/figures_review/figcheck_local.txt (CRLF) | 254 | 635a2e43de7be5ea085155ee37f0ded6fb37ab5737851ccbaa2ac4060404b361 |
| evidence/figures_review/figures_content_review.md | 11037 | af7b1b105582eae9851957db15560ea76ea5b8f387d33a9f96742e590fe1a4b8 |
| evidence/figures_review/figure_checker_probes.json (CRLF) | 4440 | 76aea86c193852ffc31fea1e74fbcae6802d7cf74cec08acf555d3613618750f |
| evidence/figures_review/portable_audit_stdout.txt (CRLF) | 4304 | 21897dee451c34e898626ab8e0396dbbf993a422449c41f110679495ae9c0054 |
| evidence/figures_review/portable_checker_stdout.txt (CRLF) | 6654 | 36a7bbea0548c24651cffe50c9cdca2b6d61be3cbae7446a62d97e71122601ee |
| evidence/figures_review/probe_figure_checker.py (CRLF) | 3521 | 76606a01ac2d71bc87eef3ecd44dc9c6f6d70cf87028b4bf0c1d12f4a5ff84fc |
| evidence/figures_review/probe_figure_checker_stdout.txt (CRLF) | 6654 | 36a7bbea0548c24651cffe50c9cdca2b6d61be3cbae7446a62d97e71122601ee |
| evidence/guard_review/Q4_guard_review_20261101.md | 13775 | b6671c64b0441b66bc03223cb051b20fbb07eb893dc0daed5379e79697d1a931 |
| evidence/independent/d1_raw_recalculation.json (CRLF) | 2421 | a2a27516fca46c92f89f36e1bc9dc393f35911996fe756302870cdaf0aba56ef |
| evidence/independent/logs_recalculated.json (CRLF) | 3410 | 286525f3a9d953e6280f92e083ec2e1a823c2a8b548e9a0409c7556715b16cec |
| evidence/independent/tool_fingerprints.json (CRLF) | 4783 | d94ba052272fa84b50a8f948ff7fe63df9ee81d3151b3b7c0c30a7003b552795 |
| evidence/independent/tool_pin_comparison.json (CRLF) | 3385 | 1a1cfdf0126740cf929296db5186ef9556e897d2a9af7d6476f6fe44ebf5e18e |
| evidence/physics_review/analytic_probe.json (CRLF) | 1743 | ab0da2bbaac0f78ec30c4a2b0406339a89a05f6ef44756bc9aa446ba86224b75 |
| evidence/physics_review/analytic_probe.py | 1624 | bc1b11e6aa889fc06f2c76ef86d1459db385ab962b8d1c49218f1459fea12005 |
| evidence/physics_review/cards_source_metadata.json | 5668 | 0f2be9e9ac1b044851f0c186b16fbe45693176c02eaec5e34489aafc0be50ea5 |
| evidence/physics_review/physics_registration_literature_review.md | 19306 | 6f5b65f3d1e7b60e8149ec739e9e7e4aba92baf166550b45b07cac8d412e5280 |
| evidence/remote/source_blob_refs.json | 878 | d3d7a823a969d11af5cf6209a147b45bffac9586208153f3b9adaff756490080 |
| evidence/source/MANIFEST.sha256 | 33125 | 3ea415548d59832da8a40900525c959cb871c0d2ac86d175836e2821e290cfe9 |
| evidence/source/PIN.txt | 431 | c6bf54f9a597434feb22810ffefc78c417aa56cc3a2d2dc0cd455d735917119e |
| evidence/guard_review/evidence/attempts_and_identity.txt.numbered.txt (CRLF) | 3294 | 991dcabb22f22ba3cf173afa563b83ed2bedabfb23cdb4cc6e8e1114e1b4677a |
| evidence/guard_review/evidence/attempt_r56_1030_152123_2568313.main_inputs.reconstructed.sha256 | 712 | 29ff619a666f29131a9d582f27e555590316e8516dcf9d0a7d2af01715bde6fa |
| evidence/guard_review/evidence/attempt_r56_1031_215830_2483798.main_inputs.reconstructed.sha256 | 712 | a22a9b9fa18782f1a02b5728c05272ef735f46fd3dba8f2441b0213b2b6a94c9 |
| evidence/guard_review/evidence/bash_execution_unavailable.txt | 1042 | 07a5d4ee82019c4c28d1e0d4beff3fe053d44531edc608618dc99adee8b7d5e3 |
| evidence/guard_review/evidence/d07_guard_v2_1031.sh.numbered.txt (CRLF) | 8461 | 088215dfc40154d45e9aa0aff02dc35c7b212bb63c07fc9bcca008e2f152dd1c |
| evidence/guard_review/evidence/failure_path_models.json (CRLF) | 6624 | 67f0d9e2bfda4267b8d2c3e84c825c204f41d7f0ec98a009fbfc759f36484c27 |
| evidence/guard_review/evidence/findings.json | 2454 | 32fac002f3d8a9381dfba34507b91dd7cf53fc2669b7b9a0d0b9244690ca8a91 |
| evidence/guard_review/evidence/portable_model_stdout.txt (CRLF) | 116 | 1ca2fd3717e5049960da76c5aef869f6b1f0384d160cb9778c2be3fb360a963b |
| evidence/guard_review/evidence/portable_verification_stdout.txt (CRLF) | 1217 | 682f5a743456bd0a7fea57700a33b6014c491abb9d20ef681569a0dade4b2a65 |
| evidence/guard_review/evidence/rendered_runner.synthetic.sh (CRLF) | 1275 | 41ce1d9b5e74fc33d11761860fa63527666cfe44734e3febff4561bb724ee767 |
| evidence/guard_review/evidence/report_resume_r56_1031_215830.md.numbered.txt (CRLF) | 5179 | 29cf553ac5dc0f5f49034f9901df8aba6d038508a36ff9a293dd889c9624e27f |
| evidence/guard_review/evidence/verification.json (CRLF) | 7693 | cc3d3417e892e6e8ab73dcc0ba22d4ac0d2c965719e7a274e9edf55256ca1750 |
| evidence/guard_review/probes/model_guard_failure_paths.py | 3931 | f10aa6a0d4d20e9343ef1fcb5df5b6168f59fe2a08fb79a7698767c4f856f33a |
| evidence/guard_review/probes/verify_guard_evidence.py | 5456 | 20499edd2eebdb98aa48b3fdb4709dbc5eb4fb22e840ac1170b50166c2e8eeaf |
| evidence/source/evidence/ledger_rows.json | 18584 | 7656d4a71a71d17038ed67724a2913d26a6d3a74727bdfd8e96e4775eab9803a |
| evidence/source/evidence/report_20261001_page_with_1p35GPa.txt | 1265 | f539ee29abf41f22db9158e781ebfbda49a9615d83ce696c11344be1ce4dc587 |
| MANIFEST.sha256 (CRLF) | 44934 | 30e0a91b72efa1fcbcafc99a1bb22e7d86862bc033c446a397e69e787df63621 |

### 뺌 — litdb 정본 카드 사본 (정본 = litdb 정본 가지 · 서랍 하나) (14)

| 멤버 | 바이트 | sha256 |
|---|---:|---|
| evidence/physics_review/cards/bazzoun2026_dem_fem_rnm_ionic.md | 9819 | 56064b95757ac7235ee5a2f4c97291c32231f265c7693c5bd69f0829d0bef4fd |
| evidence/physics_review/cards/calpa2019_small_li7p3s11_liquid_phase_composite_cathode.md | 32064 | f48adc5227825ea9dcfddba7e87b8a4f294ea9148d27f5ec03f0de17be3bbe1b |
| evidence/physics_review/cards/kawaguchi2026_se_size_soc_dependent_cathode_resistance.md | 42879 | 43c85f90340cd8f568f908d30fa3048617e1b6a3d4ec4f725bbeeebf58b1f882 |
| evidence/physics_review/cards/lei2026_se_particle_size_effects_review.md | 58803 | c9db782bf6a34ffd3cdfe686da0e5ba82225ca94ef1648025ca940b3b75ec551 |
| evidence/physics_review/cards/lin2025_submicron_lpscl_cathode_li_kinetics.md | 47008 | 2e0801c9a96c8697a679f33b9a334d5dc330f3626d3eb6283b74c95d7d91fcf1 |
| evidence/physics_review/cards/minnmann2021_jes_charge_transport_bottlenecks.md | 96904 | 7d1abb97625d2139851c1f8236ed2e3cda68a53b3ded9ac81cf9c3dd7dc10077 |
| evidence/physics_review/cards/minnmann2024_microstructure_porosity_visualization.md | 35945 | 92422d7057144f08ac8727f2ead02ae8ba828b812f9f48bfba3a94f69d4b34ce |
| evidence/physics_review/cards/schlautmann2023_se_particle_size_composite_transport.md | 64231 | 7820f86316eef89dd8a18582a701a94585bf62ff19741dac321dc2d90c902997 |
| evidence/physics_review/cards/shi2019_high_am_loading_particle_size_assb.md | 115258 | 2fdb441a9dae98c6fb8b51ed6bcfb5cf6d10abd4054abbc3a65ca78da23d07f6 |
| evidence/physics_review/cards/stavola2023_thick_nmc111_lpscl_lithiation_gradient_tortuosity.md | 56396 | b33bcde86749d6a0a1a03e60cc8e107a65ae957a0b812913a067b928db47c0fa |
| evidence/physics_review/cards/tailored_cathode_microstructure_low_pressure_assb.md | 43624 | b308f49a1040f25873d92a7f5386a75012bcbe8a232e94e1c7e82f011d131f06 |
| evidence/physics_review/cards/tron2023_rational_cathode_composite_optimization_lpscl.md | 33556 | 8029129589f1388dde0c0c9c11879e4ca620c444f165385cf52a48732935eb8f |
| evidence/physics_review/cards/yadav2021_lpscl_sieved_psd_impedance_tortuosity.md | 40724 | fe2153712f0f308b665164096bcaf23f5e1e078be7f7df3b18e6e51e3c9a4eac |
| evidence/physics_review/cards/yano2026_se_psd_width_ionic_tortuosity_dem.md | 61153 | 162f3027feb73bcea62eda6c3eed59fd99dc7be3e15673527d9af6ab62e157ea |

### 뺌 — 리뷰 핀 065ad7004 의 git blob 보충 사본 (우리 대조 = 같은 바이트) (10)

| 멤버 | 바이트 | sha256 |
|---|---:|---|
| evidence/remote/scripts/analyze_contacts.py | 80829 | a383ada7aef3d13ba08bd84728a20b6207f9b124a01ce3852c01ae2518ca1aa9 |
| evidence/remote/scripts/coverage_physics_vs_hertzian.py | 85482 | 1bf4ee8c0061e69760596b05318e0b750605e85ad16f34176e74f31db80b6253 |
| evidence/remote/scripts/dem_analysis_core.py | 102925 | 39fb19cb7eb962f11fe88546fa0ad93c4a9074846be13d15b27c2eae44fb620f |
| evidence/remote/scripts/kg50_d3_cell_verdict.py | 31933 | 44c2577d6d0f901d0d6ae48eef049f631e82c497db1f81b4b6dabbd7eda90938 |
| evidence/remote/scripts/lhs_union_webapp.py | 27536 | 3f06e9d36060a366d79e1abb76b5fe07e23b51d63666f51ba3afeabf64211408 |
| evidence/remote/scripts/network_conductivity.py | 180968 | a525e2db98fd044f0aa9353b028a3d5c7164c006a8e870dda24e7a0991d9751e |
| evidence/remote/scripts/parse_liggghts.py | 14646 | 4fe3f1f32ebc4168978c7278b7a1d37b072d64fbf00e97d0933351337d223425 |
| evidence/remote/scripts/tau_flux.py | 125811 | c0a7da6e1b73bea97136f06803810dbe159bf5c4395d8d218a90217a58ef0f78 |
| evidence/remote/webapp/app.py | 705589 | 3e82140f47c7e87b138f8a6f24b8f8575bc7476e91b8369b20cdf698b69b4bc1 |
| evidence/remote/webapp/pipeline_service.py | 128719 | 8026169f61e8bddcceea3dfb42758bb6a4e599a28271d8159c387dfc2a79d4ef |

### 뺌 — 리뷰 핀 065ad7004 의 git blob 사본 (우리 대조 = 같은 바이트) (229)

| 멤버 | 바이트 | sha256 |
|---|---:|---|
| evidence/source/repo/docs/report_making_principles.md | 8483 | c40856bdf009f60d266ede856ef3b8b457c0525689f5a0fc28d4605132612376 |
| evidence/source/repo/docs/resume_ckpt_procedure_20260927.md | 72152 | 08e116818b21cb6bc4f14e8e8c7d5c50949e32ae08f324402f2126e8471c3f12 |
| evidence/source/repo/scripts/resume_ckpt.sh | 146223 | 2dc7f693263708d7788ab721386182c6109a8f9278797ecc43f5165d6715f1e8 |
| evidence/source/repo/docs/50kg/kg50_q5_dt_damping_registration_draft_20261027.md | 54669 | 951053d34b899594d74f737870bb7f2a4cb7b66bc36a3e2a8ecf165472fdc6a0 |
| evidence/source/repo/docs/reviews/claims.json | 484386 | efe76794e308d468bf7fbdbcc5e4c871ae0e5c53174e6ac794ef2a61675080ce |
| evidence/source/repo/docs/reviews/findings.json | 2379410 | 7efc0467e1610e463230c82ee56916ee9eb05501627fa1f0554af2e426159389 |
| evidence/source/repo/docs/50kg/d07_guard/d07_guard.sh | 5075 | 4b1227ef76e8d248065537c147b650ad863c1d002a53d382fc553895d4bbc474 |
| evidence/source/repo/docs/50kg/d07_guard/d07_guard_block.txt | 5412 | 1b21663e3f29d4bf902e481ce615fbb11b3e676d6c64e5b2338162f8c898bbee |
| evidence/source/repo/docs/50kg/d07_guard/d07_guard_v2.sh | 7695 | 4124533440e5dd9bf5768571ec02185d578e5f1d0178ec3a78e2d3c8ac3fdcf4 |
| evidence/source/repo/docs/50kg/d07_guard/d07_guard_v2_1031.sh | 7838 | ff18a4fadcdaf4acc6190e60d3534096f2a9a4075e73e6e33808d25dc4a427b4 |
| evidence/source/repo/docs/50kg/d07_guard/d07_guard_v2_block.txt | 8175 | 0e38a110f50b8c312877d82c6c86c78bb9c0d257c24e72d262903fb0d8ba6f19 |
| evidence/source/repo/docs/50kg/d07_guard/README.md | 12898 | b96c44ad882e445a283216c6042bd6375cc77ac49950822ac292a34d2b459ec2 |
| evidence/source/repo/docs/50kg/d07_guard/sim_guard.sh | 3472 | 5431443d93b5e8e84bcd1f9083c40b34323401986c8586329f74f2248f673fc6 |
| evidence/source/repo/docs/50kg/d07_guard/sim_guard_v2.sh | 10119 | 6af27695597c865eb2d5f64b5383d6c840b4fb3280f8df28fe6a7cfdc965e9a9 |
| evidence/source/repo/docs/50kg/d07_guard/sim_v2_mutation_20261031.txt | 6996 | 9e3d0d5b55f86b67db159990ad1b3d26bf7531920c340f7b94ac30ceeea4da60 |
| evidence/source/repo/docs/50kg/d07_guard/sim_v2_results_20261031.txt | 14647 | 17c46ecffb2f6292e268d03f4e2743bfcf23ffc25ec85e6faf5074aebeea052d |
| evidence/source/repo/docs/50kg/report_y4/build_kg50_report_y4.py | 90441 | b1a3eeb9b7226a4ad6062136a1d5041f7a88b89f8866321f24787398d4f5b0bb |
| evidence/source/repo/docs/50kg/report_y4/checks_draft1.json | 13019 | cd48f4b995fe48cd49b8f43ecd91b6aa375d4b5c6c84d865a660161f778f573f |
| evidence/source/repo/docs/50kg/report_y4/codex_kg50_y4_draft2_request_20261031.md | 16316 | bebadd1272896a1808a1bf0a88e77b2f40b4b2be3ef475014d9078840f446f0f |
| evidence/source/repo/docs/50kg/report_y4/draft2_fix_plan_20261030.md | 8840 | 002e7d03d4ec4f4c0ae1a49968f598c2a3cf851f88282bb7b19cb6f998bad730 |
| evidence/source/repo/docs/50kg/report_y4/kg50_report_y4_draft1.pdf | 498103 | 5a219ff24020a588b04118d1f9c29eae694faab6a3155c9de2a52ee0db83a260 |
| evidence/source/repo/docs/50kg/report_y4/kg50_report_y4_draft1.pptx | 539769 | 551312593f9c8af0ce9319b16b22c8ec4a9eeaad946db77a8003f770f7fbe8c1 |
| evidence/source/repo/docs/50kg/report_y4/kg50_y4_sources.py | 20590 | 88b0a84ffa7c9e7499ccdd493f90f9cc692f71bfc4bd1efac488e40f671e51e5 |
| evidence/source/repo/docs/50kg/report_y4/lit_se_size_map_20261030.md | 19261 | 517adcc89df64224e68bbe8a0a576e39c9a5b6965e728cec6564092ba2832ea4 |
| evidence/source/repo/docs/50kg/report_y4/README.md | 13955 | fdfba9b37f8bfe7f50fad06d92662a9ec155cf84644de3762753e6709929b8c5 |
| evidence/source/repo/docs/50kg/report_y4/storyline_draft1.md | 24305 | ef8de71a3d9a5b585fb01ac82b786a8000c08860e313d69febad12ebd899503f |
| evidence/source/repo/docs/50kg/d07_guard/t_test_20261031/attempts_and_identity.txt | 3126 | 4f7f25e4b63be6c714465c65d4ce0f1096f0f6d5670a4a8149f0bc3e5eb99a25 |
| evidence/source/repo/docs/50kg/d07_guard/t_test_20261031/README.md | 2312 | 6102ebc4ed5d752f3ad2fb4ee4f42863249968cefdc76a65e7539f418e999b36 |
| evidence/source/repo/docs/50kg/d07_guard/t_test_20261031/report_resume_r56_1031_215830.md | 4976 | ffa61cedc409463f2cbc6c448b3f5451cbc900dbbb1c2653a7888a784dc69a7e |
| evidence/source/repo/docs/50kg/report_y4/draft2/make_draft2_figs.py | 81052 | 349c94471b7ddf98ea0460a85d2abb09d07470c092a0402b4019da3ebc4ecfa9 |
| evidence/source/repo/docs/50kg/report_y4/draft2/metrics_all.csv | 2437 | 839c1e9f4f7bf6de1c052253d345802ac38cf6fda4af7b251ec27988d983c716 |
| evidence/source/repo/docs/50kg/report_y4/draft2/ovito_render_spec.md | 4091 | 4ef5a3baa1a3a04af3bf6fce3a2c12e2589aa33dba91a71f7c00b3061568de86 |
| evidence/source/repo/docs/50kg/report_y4/draft2/README.md | 22304 | f9c36c3c956b44d9aa43077a26739986d8597e9e429f06fe5ceacd547867552b |
| evidence/source/repo/docs/50kg/report_y4/draft2/run_draft2_metrics.py | 51840 | 674cff2128351ff607ca5f40857f5c4fda33f6dd304987c383973c47eeec81c1 |
| evidence/source/repo/docs/50kg/report_y4/draft2/slide_text_draft2.md | 61346 | 688d32d52c9f555b6bc954882dd3dd55301105a1ae6987daa50f2da59b85021f |
| evidence/source/repo/docs/50kg/report_y4/figs/make_figs_p1.py | 13734 | bd47da984daae31cbb8acfaff54defc85f3358bc47358d45ef0cf9b025a196e9 |
| evidence/source/repo/docs/50kg/report_y4/figs/make_fig_dem_eq_monomodal.py | 11817 | 21d2ea957de88cd0152c072161d4fd06993ddc74d9e403c9abf6229565f67f04 |
| evidence/source/repo/docs/50kg/report_y4/figs/make_fig_p2_aux.py | 10663 | d6dfa88fcbb63696171948d090e13c29b50aae579bf283865d6276dd11a97afc |
| evidence/source/repo/docs/50kg/report_y4/figs/p1_figs_meta.json | 4385 | c39e2292c3ef4eef08466a80bf5e43250f0a5d63d9d43620a899a556db37a5c0 |
| evidence/source/repo/docs/50kg/report_y4/figs/p1_sections.csv | 75811 | 72ff090d1cc273b21d25503053d39ad0619d6c512f22a3e6a2d1a6a24579659d |
| evidence/source/repo/docs/50kg/report_y4/figs/p1_sections.png | 364245 | 39c006c1c3ec7c12c5bf7b67e8375c332b194e0330838bc11ad0070b50e75e9a |
| evidence/source/repo/docs/50kg/report_y4/figs/p1_sections.svg | 1048790 | e44b10c3370d2848df431b493451117db1047da3da9be972e587b6960e4beeab |
| evidence/source/repo/docs/50kg/report_y4/figs/p1_size_ratio.csv | 204 | 8fd02f5d5333f9c4b31c54985bd410f1d3488304881b894e0bf33c7d3a4cba53 |
| evidence/source/repo/docs/50kg/report_y4/figs/p1_size_ratio.png | 24311 | 6efe860df3e8f9b1b20ab1f2974429d91da9f3d4514e715b17f337f0309a3803 |
| evidence/source/repo/docs/50kg/report_y4/figs/p1_size_ratio.svg | 10598 | c4b0339b502d897ea3963c94928d47190e52cad4f071614e5facff56a63adff9 |
| evidence/source/repo/docs/50kg/report_y4/figs/p2_aux_compaction.csv | 471094 | 093b58e759a66c0095029ba261b46469197a987df9c7eecbc06845c39d585f5f |
| evidence/source/repo/docs/50kg/report_y4/figs/p2_aux_compaction.png | 119289 | 1cd6db43518b903e37162503b665e989cb0fa7ded842ee0106809beb0c4e8b7c |
| evidence/source/repo/docs/50kg/report_y4/figs/p2_aux_compaction.svg | 219644 | fce34bcbdf7a0c6699160c9c60a6bb83a1f06341eb6ddccb4b3c8ae8a2e16fd0 |
| evidence/source/repo/docs/50kg/report_y4/figs/p2_aux_meta.json | 1601 | 8ab17eca92d3d41ca67b13ad864fb29a26764e61d50fb1b3c4a6159bc112dd2d |
| evidence/source/repo/docs/50kg/report_y4/render/kg50_report_y4_draft1-1.png | 492651 | 616c5948b0b286d1e1f7f236f35a71c95f42e7c2f67fa594fd1e5f53ca7f8c0c |
| evidence/source/repo/docs/50kg/report_y4/render/kg50_report_y4_draft1-2.png | 237729 | dc90ac7a28156bcfc04a311e9b9a6388b8119f731f28261e624ad3b8490c5dde |
| evidence/source/repo/docs/50kg/report_y4/render/kg50_report_y4_draft1-3.png | 122101 | 4f93d219b84ccd6240b3b750f4d559a3e9faff5a753cdad43c2301eacf9a0042 |
| evidence/source/repo/docs/50kg/report_y4/render/kg50_report_y4_draft1-4.png | 140014 | 05207413069f254f11d661bad24d0a6ed295fd02dd5f4c65f447e1ef4cce807d |
| evidence/source/repo/docs/50kg/report_y4/render/kg50_report_y4_draft1-5.png | 144519 | fbfec3a1cbc5c34c5bcaf14fe2eb0f74b133d8b5ea7706501b93f4005c50a8f9 |
| evidence/source/repo/docs/50kg/report_y4/render/kg50_report_y4_draft1-6.png | 130187 | 4c0acf775cc2bd8b0970ddfdb8893aeb45560755787b405dc6548ef1dc6e5438 |
| evidence/source/repo/docs/50kg/report_y4/render/kg50_report_y4_draft1-7.png | 124799 | 23dc0691d84e4926cbfd2fb2992ba5cbabfc361983ebe09d3cff7b182f64e5bc |
| evidence/source/repo/docs/50kg/report_y4/draft2/figcheck/after_fix_20261031.txt | 2032 | 0a7db190d5573c380cdad3d873ba6391367a1fdca47f742ee6dc51347e8a846b |
| evidence/source/repo/docs/50kg/report_y4/draft2/figcheck/before_fix_20261031.txt | 16623 | ad2fde0cdbd1cf190312b6329b02a82cb8bf264a5cc6cba5a466aab30f19153c |
| evidence/source/repo/docs/50kg/report_y4/draft2/figcheck/determinism_csv_20261031.txt | 2200 | 9aa3b35fc20aeff03a072e5cc78286651e8c8b3c0370c8c23439a50b52c44d97 |
| evidence/source/repo/docs/50kg/report_y4/draft2/figcheck/mutation_old_limits_20261031.txt | 18610 | 23f2005e883b350f2666bbde67663beb4d2fe3ea60c39b6d206e34df38897c0b |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/diag_relax_drop_vs_N.csv | 2029 | 575239a7e5a5aa298bcd9604d7ab5edb46757c5e5b7fb4450e9de9b95546281b |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/diag_relax_drop_vs_N.png | 77836 | 892e4278313e1d0bfcb3cc8ce2d9932cbdd8b4c77b87c3e33de04aaece8cdb0a |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/diag_relax_drop_vs_N.svg | 19476 | 26a3769051a4be229c985104b0d701980cc226154d5ee94ea7d2c40c8aaf6ec8 |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/figs_meta.json | 8832 | d3d890cbf967e910abb9b1d5d14d77a3dbbffe48ac59c6a6edea7663111512e7 |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p1_bed_strip.csv | 396 | 4cb0867b0e2727f2d6657fb60498e325f6861a67adbf409617169b716d36e8dc |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p1_bed_strip.png | 576009 | cadc00700c6b86ace2002f80c3a2c05434a490cec1cce049a05aa9fd1c6347af |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p1_bed_strip.svg | 3344268 | 24b452644ff406ecd3d3cfe75d0a62f455ecb84bc2a66bfb557e2eae769b172f |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p2_compaction.csv | 400881 | 03fbae5f69aa11444c1333888c9360b8394b19938c62d9673337729d8c8dd54d |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p2_compaction.png | 121188 | 03ab984fdb0ca2b9788ac94e2b12680e89a5c8fd1254fb7ea239eb78a9faa367 |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p2_compaction.svg | 283758 | 239f9125b57c61c41ef4a11b17cf3501806c465180db03ee8bcc6e00342f7aa0 |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p2_relaxation.csv | 10528 | a71dc276a8381d98b5f0b68a25acbce99959479798dacd63069f3e6994fe354e |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p2_relaxation.png | 119909 | 7ab8186d0269ea49a3116899ceee07edfbd923a0c8bc56383ca97fb845dae6e4 |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p2_relaxation.svg | 32319 | aa2ae8ec81a0255204f1af42ce12f70f0da7920547c4b8dd794250987880ecbc |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p3_contacts.csv | 418 | 0c288c691b38cf98227d213bc680773a777cdb44e5c2941bcc05c3c2e3264c57 |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p3_contacts.png | 90878 | 83f27d9a2aa095526b29715e8ba7175d6b8cb91297d8e14f0527753660198633 |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p3_contacts.svg | 26428 | 9385d4f089a587b6ccea9eafae1f4e5c325382f6f56cd127dcf2ff7960b0dfdf |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p3_overlap_threshold.csv | 518 | 6d6396e95e084059fd90b050abfe7600a86a93de9af08fce85da21ab7cbf1f67 |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p3_overlap_threshold.png | 53951 | 35befaa6e0ca22352e128d11478d46628168542763112928d0e5ed31e1fc034e |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p3_overlap_threshold.svg | 19220 | 526866a8d60a89b40bc41e64b64387fe77f074ae3bfe6f80b126a4faeb92fb41 |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p3_per_am.csv | 1246 | 96f7308ded97ed3317f7f20b8f80364223a7f254a5890c23bd6ea8bbb979c108 |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p3_per_am.png | 83818 | ac2c50a036155d69e98e350c174a8bcd8bbaa6f3c9ff730a852e69fb214196bb |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p3_per_am.svg | 27519 | 4946bf026c0760cab82a4db311d550da0c2fa332cb8df283cfe09ae323b385d0 |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p4_f_connect.csv | 303 | 1fec21359c2fa2c096a440b0a4b96902f312402a1442b15a19d9a9df21de4bdc |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p4_f_connect.png | 87076 | c5395a275be2b22362cdf65822eaeb94e1d716dd12d20220ffeb186ea20ccdb8 |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p4_f_connect.svg | 20969 | 7493d005f715c45572299e048beeaf06e34e50158d336734857c47418e5ab9e7 |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p4_tortuosity.csv | 307 | b0182cbbd43c25cbf817f6d04e5c21c075ea22bb69f05fbac7390ad5d3a2e597 |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p4_tortuosity.png | 88185 | b670ad86cbd51effd9c71ef2880a2275bb19bcf5adf4bf6bfd44345b78f3ee25 |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p4_tortuosity.svg | 22982 | 7a5e6ce988b172379869df9db5f0c9df675bb54dbe98168879ce8c272da157e6 |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p6_z_stress.csv | 4724 | 01be1ad015930fc068f29db8c036eb2525cee159fd2547a76fe5bf12b017da0f |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p6_z_stress.png | 120298 | 34518c7336015f78f29756f3a6558aaf3d701d929d3d45b7fd684916c51ed72b |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p6_z_stress.svg | 34714 | 1310ff8a9c02711c238185a8a7bc6396486d3f2f67429e3726ea447537688f14 |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p6_z_structure.csv | 4325 | 66ca77e5100e73f910633824e61433b177a2dcaa0bdeac00f427c303b2982191 |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p6_z_structure.png | 99057 | 7ebc9fe7632a593e43875903b7c4ef0638aa6c7f113714397a06db772bfaf879 |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p6_z_structure.svg | 25674 | dbe3a2de7a5030b2e748da5b789b7f47e91a4bf8f61782362d014b54eda0cd35 |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p7_lit_direction.csv | 3895 | 734d43b781561606f2f1a3bf23fa3c5c343d1ac5340fe10b6335869161fe4ef2 |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p7_lit_direction.png | 121432 | c9cd5f646e81cce281dbcf324b62839c19a09abaa1c74f96b986c1f42ecc4c9e |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p7_lit_direction.svg | 35446 | 718d859032b81dabc1f72da1a9e0319cc6f7d65861b512904da7f6aba255b54a |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p7_summary_heat.csv | 4121 | 74980b36471e30d157938c640da4b18492d158b958c86790a0e3ff5c1ce14ece |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p7_summary_heat.png | 169825 | 82f48eebd55e9aa30938f8cf492b7d7845d06d51aaad7ced6bb09ee981fd5b16 |
| evidence/source/repo/docs/50kg/report_y4/draft2/figs/p7_summary_heat.svg | 36131 | cc61ef0f325499fa5679efc9470cd16b4f65d7d502e85642378b2afbc05cc823 |
| evidence/source/repo/docs/50kg/report_y4/draft2/ovito/D1_end_2785002_um.xyz.gz | 2574379 | 5e7dcfe16abba3f368c45933fc0981958a1b5048d99c01f5c2dc26e4cbfeb1b5 |
| evidence/source/repo/docs/50kg/report_y4/draft2/ovito/D2_end_4015002_um.xyz.gz | 337087 | d1edca65b3168394c04414d936a8f017c6ab9bb4d6a0600c557ead983d8515a2 |
| evidence/source/repo/docs/50kg/report_y4/draft2/ovito/D3_end_4575002_um.xyz.gz | 116765 | e489bccd1edf895adcbf359f2afec85a1266b96a7bad756ae40e7c85958f8e6e |
| evidence/source/repo/docs/50kg/report_y4/draft2/data/D1/curve_D1.csv | 132280 | 91fb279549d3d6a2f4a21ec2064e26675ec12e74b5fb8c6fcad50939587fc9e1 |
| evidence/source/repo/docs/50kg/report_y4/draft2/data/D1/metrics_D1.json | 17596 | 17ed9e5f11bff72497cc7a71dc60160effcba302f92a2ebff97b2fa0d2e37fbd |
| evidence/source/repo/docs/50kg/report_y4/draft2/data/D1/per_am_D1.csv | 110539 | 4a1cb5087d904c6c0c61b6175d4f972fe5b77be3a72ca715583671e069581cf4 |
| evidence/source/repo/docs/50kg/report_y4/draft2/data/D1/section_D1.csv | 142403 | 10ebb22fcefff721cc6661b557ce3a830ab20f03db5c4f54ffb9f178a3af0526 |
| evidence/source/repo/docs/50kg/report_y4/draft2/data/D1/zprof_D1.csv | 1675 | 3180daf1c96601b14ec1086d536468f4cd04655814cc9a06a221d3d7df677ce4 |
| evidence/source/repo/docs/50kg/report_y4/draft2/data/D2/curve_D2.csv | 205581 | 4929d1f63d2abc29a6fc89a94fd79a6964eecd1c725f9838ea6e9b8ee515f849 |
| evidence/source/repo/docs/50kg/report_y4/draft2/data/D2/metrics_D2.json | 18521 | a2eb2a0c0c2fcee080ea4adb1293e551f6e1258dcdbf63f896f2748b284b1b7e |
| evidence/source/repo/docs/50kg/report_y4/draft2/data/D2/per_am_D2.csv | 107867 | 3cefd4b6d21139477a07e2d148583ca00736e93d5fcff69b87f59a4e7bc409a2 |
| evidence/source/repo/docs/50kg/report_y4/draft2/data/D2/section_D2.csv | 40702 | 6175d6ee6e0062dd3eabc48b2852b26cbe7f84ee57db183f2bd73ec5a4048de8 |
| evidence/source/repo/docs/50kg/report_y4/draft2/data/D2/zprof_D2.csv | 1678 | 2e3f36ed5122fe9faa5ec3d98eebfefbc56b170b9591b5720079d97e7447bbc8 |
| evidence/source/repo/docs/50kg/report_y4/draft2/data/D3/curve_D3.csv | 238407 | 35e68cbbcf5696395fdcad5682f9cb12bad0fbb6024c3923674e8d728a13f2e5 |
| evidence/source/repo/docs/50kg/report_y4/draft2/data/D3/metrics_D3.json | 18731 | a714c9e49b6104a22b8cd7e25669747a008906867f1f81827e354af350edf1f0 |
| evidence/source/repo/docs/50kg/report_y4/draft2/data/D3/per_am_D3.csv | 112236 | 6bf68e7cf7f47ebba038754a72f5d2f3d7eafc8904908294aff2883e4c538b17 |
| evidence/source/repo/docs/50kg/report_y4/draft2/data/D3/section_D3.csv | 21101 | 327592451d5bf4f574577c13fdf0c7075089b7dc3ec496f47d09b76579dfe1f2 |
| evidence/source/repo/docs/50kg/report_y4/draft2/data/D3/zprof_D3.csv | 1671 | 8a380b156bf197a59df6dab23287475e274cc6891f59ef09db6608864b69f36e |
| evidence/source/repo/docs/50kg/report_y4/figs/dem_eq_monomodal/kg50_dem_force_A_labeled.png | 104048 | c66f8d4cbe3c49ef3ad5a16bd24be8082c67db3eedc60439cc2b29f5c13c3b7c |
| evidence/source/repo/docs/50kg/report_y4/figs/dem_eq_monomodal/kg50_dem_force_A_labeled.svg | 97475 | e4e7ee7e92d69062fa369db669e5dfb6ccde39d4778259a5678d0db9b1ec3545 |
| evidence/source/repo/docs/50kg/report_y4/figs/dem_eq_monomodal/kg50_dem_force_A_nolabel.png | 72518 | eb6d9ebd711e8e534e17d7caaa8701adafde318ca7b0d3d77a6a983407a6a027 |
| evidence/source/repo/docs/50kg/report_y4/figs/dem_eq_monomodal/kg50_dem_force_A_nolabel.svg | 79315 | c7988422fb04d76e4224da9403e74f62aa0172a4f78025efe591716a8c63d144 |
| evidence/source/repo/docs/50kg/report_y4/figs/dem_eq_monomodal/kg50_dem_force_B_labeled.png | 90671 | 2615b39ad6423174e090649c7d378aeddaeead96d0485468b2cdabcec7a413f2 |
| evidence/source/repo/docs/50kg/report_y4/figs/dem_eq_monomodal/kg50_dem_force_B_labeled.svg | 77642 | 7be8a621169d2531de72fdccfa984306c6192db9bb7d77154706b6e49f9a27c7 |
| evidence/source/repo/docs/50kg/report_y4/figs/dem_eq_monomodal/kg50_dem_force_B_nolabel.png | 58612 | 7940fe6e9a1449bafb0cec533a2d92e96aca36ed5a5ae98ebe935349eb15b7c8 |
| evidence/source/repo/docs/50kg/report_y4/figs/dem_eq_monomodal/kg50_dem_force_B_nolabel.svg | 59714 | 61b1b6818e6e06cd8f9bf631b5b079e2e074d84eb903417d24824c4a919d1959 |
| evidence/source/repo/docs/50kg/report_y4/figs/dem_eq_monomodal/layout.json | 1723 | 7e7eaa4d79245c0f9d13bc5589cf5d462842741348e49d509d1052d36defbb66 |
| evidence/source/repo/docs/data/kg50_d1_end_20261031/.gitignore | 80 | 2c0cb03c51ff5cfd044b261aea0026844c34f89a1fef639f815a46c601fa1701 |
| evidence/source/repo/docs/data/kg50_d1_end_20261031/kg50_d1_b50_log.liggghts | 735278 | 6a90f706da68e3d5041ff063d0ffd4f61e9d89a5823f29e0755a23ed679bc1b5 |
| evidence/source/repo/docs/data/kg50_d1_end_20261031/README.md | 6568 | fe5270b4bad7583aea637ff9a22aaa6f26ac8655423074020a6249d487f2c97f |
| evidence/source/repo/docs/data/kg50_d2_end_20261030/kg50_d2_b50_log.liggghts | 1102372 | 5d6721508615f2ffbd71a5c179a394f09c46f4993ac449496166ac08509dd198 |
| evidence/source/repo/docs/data/kg50_d2_end_20261030/README.md | 2904 | 969751c45d150eba470719933aa1da4f36bc6a366b1d0298909267781d59710c |
| evidence/source/repo/docs/data/kg50_d3_cell_verdict_20261027/kg50_d3_b50_s1_log.liggghts | 1267117 | 40ba638167250cd742cdbeb113f71f83851619103be36ac79eaab7572c7ffe22 |
| evidence/source/repo/docs/data/kg50_d3_cell_verdict_20261027/README.md | 4886 | 5f2aa7fd6186497b768a2e2b66e04db9832eac69c869b582be213e4884cc9c58 |
| evidence/source/repo/docs/data/kg50_decks_20261027_v3_b50/manifest.json | 6597 | e3adcb397fc9beb80e8812e549700fb9b2c0ebbfec50d0462827e5d7d1e12264 |
| evidence/source/repo/docs/data/ps73_damping_branch_20261007/README.md | 47791 | 30e7d2c375251e7147e34c1f02cf07b5baad98916ce9615f3e49d6843fc47f29 |
| evidence/source/repo/docs/data/kg50_decks_20261026_v2/kg50_d3_b50_s1/input_kg50_d3_b50_s1.liggghts | 12703 | 7589c8ac6440cbafa41a5cc79a07d58a05708971fc4bd9e44db2d951d7728278 |
| evidence/source/repo/docs/data/kg50_decks_20261027_v3_b50/kg50_d07_b50/input_kg50_d07_b50.liggghts | 12859 | 2555640c7792df6954006392d05b8fd83f09687bd49e315ae0d8ffaa9ba65ab2 |
| evidence/source/repo/docs/data/kg50_decks_20261027_v3_b50/kg50_d1_b50/input_kg50_d1_b50.liggghts | 12812 | 514afdb705613dab876c9c0ff5c1f2fef3fad3e029d71778875c08b89edfde91 |
| evidence/source/repo/docs/data/kg50_decks_20261027_v3_b50/kg50_d2_b50/input_kg50_d2_b50.liggghts | 12785 | f8ac9932a6cb4a0b45c9b6cb846bc637dd746ccf036f32590036c70ab6508825 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/codex_review_kg50_d07_scoped_go_20261030.md | 18068 | abe6dda63a44e6154093db47f211699ce09a2783455e37b62e887c333b9a536c |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/PACKAGE_MANIFEST.sha256 | 14752 | bd3935e1b396e37ce4370730ae43c6045b75711358b6915a7332cbb9973810f7 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/README.md | 2627 | 53e02513b680f47fd46ad3cf4ef051a2824ed34f685ff609e8232a2b564888cf |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/README_import.md | 5036 | 69dcfeea662f871e55da16605b47f51e9f0f7055c1761de1b7e729198aa7e607 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/REVIEW_SCOPE.json | 1004 | 0d27e7b9304110c12da19c790ad82e0734ac4bef53187f9f59b9b7757e3ab076 |
| evidence/source/repo/docs/reviews/codex_kg50_y4_draft1_review_20261030/codex_review_kg50_y4_draft1_20261030.md | 25779 | 1b6a8edb012293852f7ef3e2f9f7aa0c908848ea6a826b7b5f1a1f2fb7fd9394 |
| evidence/source/repo/docs/reviews/codex_kg50_y4_draft1_review_20261030/README_import.md | 3777 | 7a0f95bca7f909c8b5283521ea6c85609dee90dfcf6f5ea3ee550f7105407494 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/codex_kg50_d07_scoped_go_request_20261030.md | 7769 | 3785a06d74fa99e62dd7e25cc551262bbe956c435844f955f3d152705819e5e0 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/intake.json | 13767 | 9f01e9dea29b12ae69c55340e3e65f882f0ae41b50694ee4c0f74d31c6b272af |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/intake.py | 2350 | 6096883f815acbd83b615d0dee813c5c27067f48fb609b9a7b1bfa133d0dc9dc |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/MANIFEST.sha256 | 2779 | 7abb331461ae109165f109afd5abde833fac82a234c85ed11221e4016bfccc3e |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/original_log_intake.json | 374 | f64fb58467947d1b1877df6073f65954dae3110afcf1c666eda9a20d86403568 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/PIN.txt | 2231 | deb48c9ad185216e0c7eb13a8cfdd260eaab8a3cea25f52ff00641cd18de4e9e |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/probe_gate_model.py | 1719 | 4e8fa14ba399eb305e32381d74256079cc228e9c2d99427b1d2efe848a177f32 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/probe_submit_gate.py | 3962 | 712392557029204ccae68548d55931775710a30c05785e09c99338464133f864 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/remote_meta.json | 6521 | b3bbf4eebf57b8f2e08bd48442fb49d9ce0144c12aa8ad6367112f7f9e639cc5 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/remote_pin.json | 228 | c425349182a31e8b4d63c7990144e76c81b47ab27ac64ae91542fc3f24c55f10 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/reproduce.py | 10807 | b74ef2d18911f8447c9d0ba12cc37397675600159c0611495db3517509b5e54f |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/_repro_ours_20261030/g13_check.py | 5204 | 52385680f1794f108c4f6140c774f79420937a5c28c3c40ff2bd11046f640e51 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/_repro_ours_20261030/g13_insert_deck_1-170.json | 3073 | 284c3b8ae02fcaf77c2581b76c871f83ea406499f94444d987519511eefb77db |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/_repro_ours_20261030/g13_main_deck_1-166.json | 3066 | 33d51dc41702d4a46ba93788961d2094976689fc99ff9c5d8fc011d92f5cf2c0 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/_repro_ours_20261030/g13_main_deck_1-167_negative.json | 3105 | bc5f1ebca3d08839cd4794bf90cf26e1002a610573df18b6f2047f9bdd127354 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/_repro_ours_20261030/reproduce_checks.json | 10643 | 06e029d61d835ce4cb4a8238605eca3f4137575d7a62d30c404f56c18d1a9eb6 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/_repro_ours_20261030/reproduce_stdout.txt | 162 | 36ed92a53ae7ab31095ffeabc19af77fba07344d3d44845782a0db140972a9fb |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/evidence/compare_transform.py | 3459 | a58a85249c3c5f11cdf69080f35df0134a6be96b35d7c42cf22892a5fc463654 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/evidence/diff_D07.txt | 2292 | 3e118703879e81788c5021b55840cfcd3fec4cd4320af2aa3758a3d700a815f2 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/evidence/diff_D2.txt | 2276 | d9fac801b0ceb35b378c176b4a00d9da55aa091ee9586c7a09efcc98622bba75 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/evidence/transform_compare.json | 3994 | aaa1ed9a7ffbfcffb64d17bf5800fe024932eb2a0e6c20da16da06a6de726641 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/actual_deckcheck.json | 530 | 3750b3bf19d4303fa40f42e595e804f9fdc2260ad4c4ece5c76188a894f8d46b |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/checks.json | 10643 | 06e029d61d835ce4cb4a8238605eca3f4137575d7a62d30c404f56c18d1a9eb6 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/deckcheck_exact.py | 83068 | 29720e4e1f7c036e071940c034b78f018acc222f16016a6a713feb22fa4b2a93 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/dt_res_only.json | 1310 | 9cd9aa0a9faaafd1a3dc68ad029192b9a85cca7731224e307e3c4572c5a83989 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/dt_res_only.liggghts | 12526 | 40ef748b963e40c255dde1b8c48a87b9377024f867ca9f7f21f2d06abd404350 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/duration_res_only.json | 585 | 16c58972b1af2dd811228fb51c5410879d6091b62fea45de68ff5a2f42013c0a |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/duration_res_only.liggghts | 12526 | 86d6c4d65af91375828fdfc7055a57888946587864f3ee68824a1c702f1ff7a3 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gravity_res_only.json | 969 | c888edcb8707aaa2e647e27242b82fc4ebbacb7ae8b3993a438606672c684bc4 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gravity_res_only.liggghts | 12527 | 7d70b01081ba7bc45025a44adee9321d403c059508100ff49346cb84a0111697 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/harness_initial_checks.json | 9739 | 77aff43cf56ecf1d581e3f83a42bd99e57ffd71141dc6fc75cfc98addbd0b2ab |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/new_call_duration_change.json | 530 | 5d1b076f6713469f76b26ef5ac32f968104f95a0731cb119765825f67ca3924d |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/new_call_trial.liggghts | 8065 | 94db4187093b417468ac7a2da6a0b43e5312e04507539251be45cbe2b8011ea1 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/new_resume_210001.liggghts | 12526 | 86d6c4d65af91375828fdfc7055a57888946587864f3ee68824a1c702f1ff7a3 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/new_source_210001.liggghts | 12859 | a599d911dc9b9dcad212695f458a9d10154d69d8cd0c3ed9de3f2e17babb1dee |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/original_log_recomputed.json | 1076 | 87e5fd5a77c9f675b2f6b88b679603fe523aec07fcf88d7373c600ea194dcd3f |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/receipt_verification.json | 1414 | 6b447fea35b0456d4def5f181f5f0cd0b0bd214631c7cddc9a2269ff0d08f437 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/static_run_trace.json | 1152 | b6162d9cfa4cbc07bc8296d81239ee3d24a0454eb6a20ae38970ad775ee305ec |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/transform_stdout.txt | 247 | 1b57d857b4103b962f9218f5af7fd53fcd29b195ee5154ff75783e8d8080b754 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/trial_log_recomputed.json | 1150 | e4dc6a7759341d125f766ce9ec773a475ed640e47a1eabb30749238fdcce82a1 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/trial_regenerated.liggghts | 8065 | 94db4187093b417468ac7a2da6a0b43e5312e04507539251be45cbe2b8011ea1 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/input/kg50_d07_b50_ins1_log.liggghts | 13475 | b1b298bbd54f77a1adf47745e6b1eed14ab2a35bbb5aea9c473b6e9ff46657f5 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/input/kg50_d07_T_1030.tgz | 16401 | 5e5461c331cc8c060ac6fce22080142c614b09af07413ab5fe676456d2a2d549 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_model/results.json | 895 | a6f1ef7506e605b885dacbab47ebfd2853f347a07ad6dfae8a030b398747d8ef |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_probe/gate_verbatim.sh | 3708 | f1dadfcbeb46cd8fa1bc56fd6bf55af194080871372df236c587c070d926337a |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_probe/results.json | 1294 | ff38bd496ed3eab6cb4f8cc2eb89deeecb4ccf42c9b6fbcc5fabb758c40f03f3 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/transform/diff_D07.txt | 2292 | 3e118703879e81788c5021b55840cfcd3fec4cd4320af2aa3758a3d700a815f2 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/transform/diff_D2.txt | 2276 | d9fac801b0ceb35b378c176b4a00d9da55aa091ee9586c7a09efcc98622bba75 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/transform/transform_compare.json | 3994 | aaa1ed9a7ffbfcffb64d17bf5800fe024932eb2a0e6c20da16da06a6de726641 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_probe/baseline/FAKE_checkpoint.bin | 37 | 0b209df6317bcf7a627deeb1757788031e1035e67174f718b68c24adef7ce5f2 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_probe/baseline/FAKE_helper.py | 39 | 24625186aed5d432300c2c1d12d406375e3249b73a6920c01b15140393f979d8 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_probe/baseline/fake_sbatch_calls.txt | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_probe/baseline/input_kg50_d07_b50_r56.liggghts | 12526 | 8e129f421a8491975f83527f79c8418318b2af30baeedd7440cfcede2d45c5e5 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_probe/baseline/input_kg50_d07_b50_r56t.liggghts | 8065 | 94db4187093b417468ac7a2da6a0b43e5312e04507539251be45cbe2b8011ea1 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_probe/baseline/report.md | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_probe/baseline/run_kg50_d07_b50_r56.sh | 1757 | aad9ac227a3d5dec24dd0515f262299d81a4da283112dfb0cdf42e0b5e379750 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_probe/baseline/run_kg50_d07_b50_r56t.sh | 1761 | c00746e68b8420b45d41ec2a6a20dc72161f9974cc6a30a403b994991e24146f |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_probe/baseline/safe_gate.sh | 4904 | 81449be67ecbf28e7d98b19291bba2ffdde5da9bf2df740b8a7aa8aa413f6676 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_probe/baseline/stdout.txt | 175 | c0b4b1bd76cb624df265056e4cdcf881296fc99e77fa3f1b07e48d438015e6ef |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_probe/changed_after_trial/FAKE_checkpoint.bin | 37 | 0b209df6317bcf7a627deeb1757788031e1035e67174f718b68c24adef7ce5f2 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_probe/changed_after_trial/FAKE_helper.py | 39 | 24625186aed5d432300c2c1d12d406375e3249b73a6920c01b15140393f979d8 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_probe/changed_after_trial/fake_sbatch_calls.txt | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_probe/changed_after_trial/input_kg50_d07_b50_r56.liggghts | 12546 | 39aa73a8dafaac328424cf3ddf96f9bc1adffa6e5c1bde1c59f1b039895d77f4 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_probe/changed_after_trial/input_kg50_d07_b50_r56t.liggghts | 8065 | 94db4187093b417468ac7a2da6a0b43e5312e04507539251be45cbe2b8011ea1 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_probe/changed_after_trial/report.md | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_probe/changed_after_trial/run_kg50_d07_b50_r56.sh | 1757 | aad9ac227a3d5dec24dd0515f262299d81a4da283112dfb0cdf42e0b5e379750 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_probe/changed_after_trial/run_kg50_d07_b50_r56t.sh | 1761 | c00746e68b8420b45d41ec2a6a20dc72161f9974cc6a30a403b994991e24146f |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_probe/changed_after_trial/safe_gate.sh | 4959 | 4b1d14d804ca56a8a8de4cc2ceebbb0c1803541a634091c4a3f87ee279f118f7 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_probe/changed_after_trial/stdout.txt | 175 | ab982fc57c30ead0e7a2355c8771ea0e623239e4be0ac7938fa5182b10df3d96 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_probe/new_call_unreviewed_duration/FAKE_checkpoint.bin | 37 | 0b209df6317bcf7a627deeb1757788031e1035e67174f718b68c24adef7ce5f2 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_probe/new_call_unreviewed_duration/FAKE_helper.py | 39 | 24625186aed5d432300c2c1d12d406375e3249b73a6920c01b15140393f979d8 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_probe/new_call_unreviewed_duration/fake_sbatch_calls.txt | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_probe/new_call_unreviewed_duration/input_kg50_d07_b50_r56.liggghts | 12526 | 86d6c4d65af91375828fdfc7055a57888946587864f3ee68824a1c702f1ff7a3 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_probe/new_call_unreviewed_duration/input_kg50_d07_b50_r56t.liggghts | 8065 | 94db4187093b417468ac7a2da6a0b43e5312e04507539251be45cbe2b8011ea1 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_probe/new_call_unreviewed_duration/report.md | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_probe/new_call_unreviewed_duration/run_kg50_d07_b50_r56.sh | 1757 | 55f6992a7dc711cfaee828e38cab460ee293a65ae605b0fe3bf83f69de80f2f9 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_probe/new_call_unreviewed_duration/run_kg50_d07_b50_r56t.sh | 1761 | c00746e68b8420b45d41ec2a6a20dc72161f9974cc6a30a403b994991e24146f |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_probe/new_call_unreviewed_duration/safe_gate.sh | 5004 | 7ab93a47ccca04d3a518c3098b03960fd38986ded75a5a3236c667b24e3da1f6 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_probe/new_call_unreviewed_duration/stdout.txt | 175 | 76d4cf8655a2437fa76f75a161f55dee4e08fc56b66487051e928a578c7aec82 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_probe/baseline/attempt/main_inputs.sha256 | 874 | 3377a5c53d1ee3b230390c2f931eb1c5733374eca905805d00b02c50573050dc |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_probe/changed_after_trial/attempt/main_inputs.sha256 | 929 | 58d39cd2728121fcc702dc36e88578b4002ca5ed191434525a1eac6ba5900d14 |
| evidence/source/repo/docs/reviews/codex_kg50_d07_scoped_go_20261030/evidence/independent/gate_probe/new_call_unreviewed_duration/attempt/main_inputs.sha256 | 974 | 819b6d01d3e54f88d45a90beda5897275a6797b8d908b393fd76f4befb8fba41 |

### 뺌 — 리포 docs/50kg/report_y4/codex_kg50_y4_draft2_request_20261031.md (핀 판 같은 바이트) (1)

| 멤버 | 바이트 | sha256 |
|---|---:|---|
| evidence/source/codex_kg50_y4_draft2_request_20261031.md | 16316 | bebadd1272896a1808a1bf0a88e77b2f40b4b2be3ef475014d9078840f446f0f |

### 뺌 — 큰 기계 대조 기록 (100 KB 넘음) (3)

| 멤버 | 바이트 | sha256 |
|---|---:|---|
| evidence/remote_blob_metadata.json | 217662 | 3228026afc668954c70991ceb58fdacd607832cb93bb73232bd04c4f6af61c50 |
| evidence/figures_review/figure_numeric_audit.json | 3224018 | 478b20c98d5b0cd9a426443a17e99b11669a17405fd078dbfab9474f1738f675 |
| evidence/independent/checks.json | 792853 | b6316677fc2e9c382373f5b8ff276a5b81afeb1cbc1aee6aa685382729c0e2e6 |

### 뺌 — 핀 blob 의 보충 사본 · 끝 줄바꿈 하나 더 (내용 같음) (2)

| 멤버 | 바이트 | sha256 |
|---|---:|---|
| evidence/remote/docs/sulfide_se_mechanical_anchors.md | 9220 | 6d83d536c168226c683de2d9c148a1c80e0155c1edd706a0cb9eeeff336644fe |
| evidence/remote/docs/data/kg50_decks_20261026_v2/manifest.json | 15889 | 8e99b38e6702a06922b3522b78b927e731e0e9c0921d7fbaf10cc855ce5276aa |
