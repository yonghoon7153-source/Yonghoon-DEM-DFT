# site_screen 자체 코드리뷰 (2026-08-11) — 10건 전부 실재 · 전건 수정

- 대상: `tools/sdcp/site_screen.py` · `watch_site_screen.py` · `run_site_screen_gabia.sh`
- 방식: 단일 패스 정독 리뷰 (8관점 순차). Codex Round-3 회답이 오면 **이 표와 병합**한다.
- 결과: 10건 보고 → 10건 전부 실재 확인 → 전건 수정. selftest 26개로 확장.

| # | 심각도 | 발견 | 수정 |
|---|---|---|---|
| 1 | ★★★ | **gate_version 이 relax 지문에 새어 들어감** — `dict(proto)` 재해시에 gate_version(+옛 지문)이 포함돼, 게이트 임계 한 글자만 고쳐도 GPU 이완 전부 재실행. **분리를 만들어 놓고 스스로 깨뜨린 것** | `make_protocol()` 로 지문 입력을 계산 항목만 담은 dict 로 고정. selftest #10: GATE 변경 → 지문 불변 assert |
| 2 | ★★★ | watch 가 **빈 run 을 '완료'로 보고** — 목표 미상 단계가 shortfall 을 안 올림. 없는 조각도 조용히 건너뜀 | rigid 목표 = atlas_rows 통과 수(정본), relax 목표 = score 가 남기는 `_shortlist.json`. 목표 미상 = 완료 증명 불가로 셈. 없는 조각 = 미시작 |
| 3 | ★★★ | **rigid 가 자세를 재생성** — score 시점 `--gap/--ndir` 로 make_pose 를 다시 불러, atlas 와 플래그가 어긋나면 게이트 통과 이력 없는 기하를 채점 (ndir 축소 시 IndexError) | rigid 도 relax 처럼 **저장된 atlas 구조만 읽음**. `--gap/--ndir` 를 score 에서 제거, 지문의 gap/ndir 는 atlas manifest 값 |
| 4 | ★★ | cmd_gate 가 순서 규약(슬랩 원본순서+분자 뒤)을 검증 안 함 — 종별 정렬 CONTCAR(우리 `_write_poscar` 산출물 포함)를 넣으면 전 게이트가 조용히 쓰레기. 감긴 좌표는 결합 전부 절단으로 오판 | 파일마다 슬랩 순서·분자 조성 검사(불일치 = 건너뜀·판정 아님). **결합 그래프 따라 MIC 로 펴서** 결합·이미지 검사 (원자0 기준 통짜 MIC 는 C10 장축>b/2 라 금지) |
| 5 | ★★ | extraction_check 가 clean↔복합체 대응을 검증 없이 인덱스 비교 — 다른 정렬이면 대량 오판, 짧으면 IndexError | 원소/순서 불일치 → `CLEAN_MISMATCH`(검사 불가·판정 아님) + 경고. selftest #12 |
| 6 | ★★ | cmd_gate 가 옛 키(`lost_substrate_O_neighbors`)를 출력 — 추출 근거가 항상 None 으로 찍힘 | `lost_substrate_O_coordination` + 면내 hop 도 출력 |
| 7 | ★★ | 재개 skip-check 의 `json.loads` 무방비 — 죽은 런의 반쪽 JSON 에서 재개 자체가 크래시 | `_load_record()`(JSONDecodeError → 없음) + `_atomic_json()`(tmp→rename) |
| 8 | ★ | 깨끗한 슬랩 이완을 조각×freeze 마다 반복 — 같은 것을 4번 GPU 이완 | `clean_cache[ff]` 로 1회. 로그는 run 루트에 |
| 9 | ★ | watch 가 shortlist 파라미터(2,5)와 freeze 문자열('1.00')을 하드코딩 — `--pairs 8` 이면 영원히 '중단', `--freeze 1.0` 은 0 표시 | relax_f* 디렉터리 자동 발견 + `_shortlist.json` 읽기(없으면 ≈추정 표시). `--freeze` 인자 제거 |
| 10 | · | 죽은 대입 `a.freeze_current` | 삭제 |

## 리뷰가 추가로 잡아준 것 (수정 중 발견)

- #4 의 unwrap 을 결합 검사에만 적용했더니 selftest 가 바로 잡았다 — **이미지 게이트도 감긴
  좌표를 보고 있었다** (감긴 원자 ↔ 자기 이미지 거리 0 → IMAGE_LATERAL 오발동).
  결합·이미지 모두 편 좌표(mpu)로 통일. 접촉 검사는 원래 MIC 라 무관.

## 파급

- **지문 조리법 변경** — 이 커밋 이전 레코드는 재개 시 1회 재계산된다. 캠페인 v1 은 완료·등재
  상태라 실사용 영향 없음. 이후로는 게이트 수정 → `regate` 만으로 끝난다(원래 의도).
- gabia 기존 run 에는 `_shortlist.json` 이 없다 — watch 가 `≈` 표시로 추정치를 쓴다.

## Codex Round-3 병합 대기

Codex 회답이 오면: (a) 같은 발견은 이 표에 병기, (b) 우리가 놓친 것은 행 추가 후 수정,
(c) 충돌하는 판단은 재현 코드로 판정. 정본 표는 이 파일 하나로 유지한다.
