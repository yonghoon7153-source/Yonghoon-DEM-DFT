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

---

# Codex 교차검증 병합 (2026-08-11, `333a428e` 대상)

Codex 가 10건을 **전부 실재로 확인**하고 selftest·빈-run 회귀를 직접 재현했다. 다만
**"전건 폐쇄"는 과했다** — 아래가 그 판정이다. 우리 표기를 `부분 폐쇄`로 낮춘다.

| # | Codex 판정 | 잔여 |
|---|---|---|
| 1 | 부분 · **새 P0** | gate 분리 뒤 **옛 gate 판정이 rigid 캐시에 남아 relax shortlist 에 재진입** |
| 2 | 부분 | watcher 가 label 집합이 아니라 **개수**만 비교 · target=0 이 shortfall 을 안 올림 |
| 3 | 핵심 폐쇄 | 기존 OUT 에 `atlas --dry-run` 재실행 시 새 rows + 옛 XYZ 결합 가능 |
| 4 | 부분 | **basin PCA/COM 서술자는 아직 wrapped 좌표** · 조성 Counter 는 동원소 순열을 못 잡음 |
| 5 | 부분 | `CLEAN_MISMATCH` 가 경고일 뿐 `ranking_eligible` 을 안 막음 |
| 6 | **미폐쇄** | 순수 hop 은 `LATERAL_HOP_OR_RECONSTRUCTION` 인데 출력 분기가 그 값을 안 받음 → 터미널에 안 보임 |
| 7 | 부분 | verdict·handoff·regate 는 여전히 직접 `json.loads` · regate 는 비원자 write |
| 8 | 핵심 폐쇄 | clean FIRE 수렴 반환값 미확인 · resume 시 옛/새 reference 혼재 가능 |
| 9 | 부분 | **shell runner 의 `watch)` 는 아직 `1.00/0.85` 하드코딩** (Python watcher 만 고쳤다) |
| 10 | 폐쇄 | — |

## ★ 즉시 고친 것 — DFT 인계 MAGMOM 순열 (외주 발송 차단이었다)

Codex 지적을 실측으로 확인했다:

```
POSCAR 순서: Li48 Ni48 O96 C10 F22
비영 모멘트 인덱스 1–189 (48개)   ← 원본(층별 뒤섞임) 순서
POSCAR 상 Ni 슬롯 48–95           ← 종별 정렬 순서
⛔ 48개 중 36개가 Li·O 에 걸려 있었다
```

`_magmom_configs` 가 **원본 순서** 리스트를 반환하고 호출부에서 `_write_poscar` 의 `order` 로
재매핑하도록 고쳤다. 수정 후 비영 48 = Ni 48 **완전 일치**, 총자화 0.0 확인.
**이대로 외주에 보냈으면 12잡 전부 무의미했다.**

같이 고친 것 (전부 Codex 지적):
- **`IVDW=11` 은 D3 zero damping** 이지 D3(BJ)(=12) 가 아니다 → 주석 정정. 값은 2026-08-08
  수령분과 맞추려 11 유지. 그 JSON 의 `D3(IVDW=11)` 표기도 틀렸다.
- **`LCHARG=.TRUE.`** — 요청서가 U-ramp(`ICHARG=1` 승계)를 허용하는데 `.FALSE.` 면 그 경로가 막힌다.
- **SDCP doped 라디칼 씨앗** — 분자부 모멘트가 전부 0 이라 doublet 이 닫힌 껍질로 붕괴할 수
  있었다. 술포네이트 O 에 총 1 μB 를 나눠 준다.

## 남은 차단 (발송 금지 · 판정 보류)

Codex 가 정리한 순서를 그대로 받는다:

1. **P0** stale-gate/rigid-cache 결합 끊기 — 현재 label/fingerprint exact-set 게이트
2. ~~MAGMOM 재매핑~~ ✅ · canonical AFM 정의 통일(그쪽 `afm_net2` 는 magnitude bias 방식이라 **우리 flip 방식과 다른 것**)
3. relax shortlist 의 `min(E)` 제거 + **방향(direction) quota·집계** — roll 변형을 독립 표본으로 세지 말 것
4. clean exact mapping + `geometry_pass` / `analysis_eligible` 분리
5. watcher expected freeze/label/fingerprint 검사 · shell watcher 를 Python watcher 호출로 단일화
6. regate·모든 JSON write 원자화 + non-dict schema 검사
7. 실제 12-job bundle 을 git 에 (현재 `REQUEST.md` 만 있고 입력·manifest·runner 가 없다)
8. 최신 코드로 UMA 재집계 후 JSON·XYZ·log·manifest 동반 반환

**선언 금지 (Codex 최종 판정 수용)** — 아래 셋 중 어느 것도 아직 말하면 안 된다:
`전건 수정 완료` · `site preference 판정 완료` · `외주 12잡 발송 가능`.

정본 판정은 유지: `ptfe_c10/f0.85` = **ORIENTATION_DEPENDENT / NOT_RESOLVED**,
SDCP 3쌍 = `n_pair=3, n_distinct_direction=1` 로 intrinsic 판정 불가.

## 반영 못 한 지적 하나 (기록)

`selftest 26개` 라는 표기는 Codex 말대로 **테스트 계약이 아니다**(코드가 개수를 assert 하지
않고, 그쪽 실행에선 30줄이 찍혔다). "selftest exit 0" 으로만 말하고 개수는 쓰지 않는다.
