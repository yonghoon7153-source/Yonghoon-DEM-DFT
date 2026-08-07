# Phase B 구현 기록 — network/Stage E 세대 분리 (2026-08-07)

Codex 코드리뷰(`Codex/dem-mpm-crosscheck @ d9880b73`, 2026-08-07) 의 **Phase B** 담당분.
리뷰 원문은 이 리포에 없다 — 전사 과정에서 남의 문서가 미묘하게 달라지는 것을 피하려고
**원본 소유자가 커밋**하는 쪽으로 남긴다.  여기서는 finding ID 로만 참조한다.

소유 선언 파일: `webapp/pipeline_service.py`(신규) · `webapp/app.py`(pipeline/analyze
wrapper/retry/batch 경로) · `webapp/test_pipeline_provenance.py`(신규) ·
`webapp/templates/{index,single}.html`(아래 ⑤ 때문에 **범위 확장**).
Phase A(F-01/F-06 인증·path containment)는 **맡지 않았다** — 배포 모델 결정 대기.

---

## 리뷰 주장 검증 — 이 브랜치에서 재현되는가

| finding | 확인 | 이 브랜치 실제 |
|---|---|---|
| F-01 인증 없음 | ✓ | `render.yaml` = `--bind 0.0.0.0 --workers 2`, auth 미들웨어 0 |
| F-02 preserve 가 실제로는 재계산 | ✓ | 백업 4874 → 삭제 4913 → `run_pipeline()`(solver 실행) → 복원 4919 → "network SKIPPED" 4968 |
| F-03 semaphore 프로세스 로컬 | ✓ | `threading.Semaphore(1)` module-global + workers 2 |
| F-05 실패가 success 로 | ✓ | parse 만 검사, 나머지는 rc 를 로그에만 넣고 `return {'success': True}` |
| app.py 규모 | ✓ | 10,440 줄 (리뷰와 동일) |

### ★ 리뷰가 놓친 잠복 버그 하나 (같이 고침)

`_NET_MERGE_KEYS` 는 **`analyze()` 의 지역 변수**(4815)인데 `run_pipeline` 이 그것을
2912/3020/3030 에서 읽는다 → 모듈 전역에 없으므로 **매 실행 `NameError`**.
bimodal 분기는 `except Exception: pass` 가 통째로 삼켜 **무증상**이었다.

⇒ `run_pipeline` 안의 network→full_metrics 머지는 **한 번도 동작한 적이 없고**,
σ 가 `full_metrics.json` 에 들어간 것은 오직 wrapper 의 Step 5 덕분이었다.
(AST 로 증명: 모듈 전역 여부 False · run_pipeline 안 할당 없음 · analyze 안 할당 4815.)
→ 모듈 전역으로 승격해 양쪽이 같은 목록을 쓰게 했다.

### ★ 리뷰가 놓친 두 번째 — Step 6 의 lock 은 도달 불가였다

`force_network=True` 여도 Step 5 가 **갓 계산된** network 를 머지하고 return 하므로,
Step 6 의 `with _network_solver_lock:` 블록은 **solver 가 파일을 못 썼을 때만** 도달하는
사실상 죽은 코드였다.  F-03 의 "정상 경로는 lock 밖" 은 이 구조 때문이다.

---

## 무엇을 바꿨나

### ① `webapp/pipeline_service.py` (신규)

단계 계약 · provenance · 프로세스간 lock 을 **한 곳에** 정의한다 (F-17: 같은 순서를 네
곳이 각자 구현해 drift 가 이미 발생했다).

- `snapshot_network` / `restore_network` — network 산출물 세대 보존
- `stamp_network_provenance` / `read_network_provenance` — `network_run_id` 도장.
  도장 없는 옛 산출물은 `run_id=None` 으로 **정직하게** 돌려준다 (지어내지 않는다)
- `run_stage(name, cmd, required=, expects=)` — rc **와** 기대 산출물을 함께 본다.
  ★ network CLI 는 물리망이 없으면 **파일을 안 쓰고도 exit 0** 이 될 수 있다
- `summarize` → `done` / `partial` / `failed`
- `network_lock()` — **파일 lock**(POSIX flock / Windows msvcrt), 미지원이면 경고 후 통과
- `atomic_write_json` — 같은 디렉터리 temp → fsync → `os.replace` (F-10 부분 대응)

### ② F-02 — 세대가 섞이던 순서를 뒤집었다

```
옛:  백업 → results 삭제 → solver 재실행 → 그 결과로 Stage E → 옛 network 복원
     ⇒ full_metrics 안에서 baseline=옛 세대, Stage E=새 세대  (수치가 같으면 숨는다)

새:  스냅샷 → results 삭제 → run_pipeline(preserve_network=True, snapshot=…)
        ↳ 복원을 **Stage E 보다 먼저** → solver **호출 0회** → 그 baseline 으로 Stage E
     ⇒ Stage E 는 항상 화면에 실제로 남을 baseline 을 본다
```

`network_run_id` 와 `stage_e_parent_network_run_id` 를 `full_metrics.json` 에 새기고,
publish 후 **둘이 어긋나면 로그에 즉시 찍는다** (F-02 회귀 감시).

### ③ F-05 — 단계 계약

`run_pipeline` 이 `{'success','status','log','network_run_id','failed_stages'}` 를 돌려주고,
wrapper 가 `failed` → `meta.status='error'` 로 내린다.  `partial`(선택 단계만 실패, 예:
Stage E 실패지만 baseline 은 살아 있음)을 `done` 과 구분한다.

### ④ F-03 — 세 호출부가 같은 파일 lock

`run_pipeline` · `/retry-network` · batch 세 곳이 모두 `_ps.network_lock()` 을 잡는다.
쓰이지 않게 된 `threading.Semaphore` 는 **제거**했다 — 남겨두면 "직렬화되고 있다" 는
잘못된 안심을 준다.  ⚠ 파일 lock 은 **한 호스트 안에서만** 유효하다.

### ⑤ F-04 — 취소는 취소가 아니다 (라벨을 사실에 맞춤)

`/analyze-cancel` 은 계산을 멈추지 못한다 (thread·subprocess 가 계속 돌고 끝나면 결과를
덮어쓰고 Supabase 까지 동기화한다).  옛 구현은 `status='done'` 으로 적어 **완료처럼**
보이게 했다.  → 별도 상태 `detached` + "계산은 계속됩니다" 문구로 바꿨다.

⚠ **이 때문에 범위를 넓혔다**: `index.html`/`single.html` 의 폴링이 `done`/`error` 에서만
멈춰서, 새 상태를 넣으면 **무한 폴링**에 빠진다.  내 변경이 만든 문제이므로 두 폴링에
`detached` 분기를 추가했다 (`single.html` 에는 빠져 있던 `error` 분기도 함께).

### ⑥ 중복 제거

analyze wrapper 의 Step 6-7 (network + Stage E 를 **두 번째로** 수행) 을 삭제.
남겼다면 이번 변경 뒤 force 경로에서 solver 가 두 번 돌았다.  Step 1-7 = 224 줄 → 82 줄,
bimodal/standard 분기의 network+StageE 블록 = 48+53 줄 → 8+5 줄.

---

## 검증

```
webapp/test_pipeline_provenance.py            18/18 PASS   (신규)
webapp/test_predictor_ui_and_sigma_grain.py   ALL PASS     (기존, 영향 없음)
webapp/app.py                                 AST OK · import OK · 135 routes
webapp/static/js/viewer3d.js                  node --check OK
templates/{index,single}.html <script>        블록별 node --check OK
```

핵심 회귀 (가짜 실행기로 **호출 횟수를 실제로 센다**):

- preserve → `network_conductivity.py` **0회**, Stage E 1회
- preserve → 옛 network 파일이 **바이트 그대로**(sha256 동일), baseline σ = 옛 값
- preserve → Stage E 가 **그 baseline** 을 봤다 (1.0 → 2.0, 새 solver 값 999 아님)
- preserve → `network_run_id == stage_e_parent_network_run_id`
- force → solver **정확히 1회**, 새 run_id 로 둘 다 갱신
- rc=0 인데 산출물 없음 → 단계 실패 → `status='failed'` (done 아님)

`webapp/test_temp_pressure_wiring.py` 는 이 컨테이너에 scipy 가 없어 import 단계에서
멈춘다 — 내 변경과 무관한 환경 문제 (리뷰도 Windows 에서 Flask 부재로 같은 상황).

---

## 남은 위험 (이번에 **안** 고친 것)

1. **F-01/F-06 (Phase A)** — 공개 Render 라면 릴리스 블로커.  인증 없이 `/delete`,
   archive 변경, predictor 학습이 호출된다.  archive path containment 누락도 그대로.
2. **F-07** batch/predictor 상태가 프로세스 로컬 — workers=2 에서 불일치.
3. **F-08** Supabase 재귀/pagination 삭제, rename/move 원격 미갱신, MPM lab 영속성.
4. **F-09** startup restore 가 worker 마다 중복 실행 + 비원자적 다운로드.
5. **F-04 진짜 취소** — 지금은 라벨만 정직해졌다.  실제 중단은 job ID + process group +
   단계 경계 플래그가 필요하다.
6. **F-10** `meta.json` 등 나머지 쓰기는 아직 비원자적 (이번엔 wrapper 경로만 전환).
7. **F-11/F-13** 단위·seed·grid provenance — Phase D.
8. ⚠ **파일 lock 은 단일 호스트 가정**.  다중 호스트 배포로 가면 무효다.

## Codex 교차검증용 체크포인트

- `webapp/test_pipeline_provenance.py` 를 그대로 돌려 6개 핵심 항목을 확인
- 실제 케이스로: 재분석 2회(preserve) 후 `network_conductivity.json` 의 sha256 이 변하지
  않고 `full_metrics.json` 의 두 run_id 가 같은지
- `force_network=True` 1회 후 두 run_id 가 **함께** 새 값으로 바뀌는지
- 필수 단계를 일부러 깨뜨렸을 때 케이스가 `done` 이 되지 않는지
