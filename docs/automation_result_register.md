# 결과회수 자동화 + 자동 동기화 파이프라인 (MCP/CD)

원격(V100) 계산 → webapp 자동 반영까지의 4-층 자동화.  "이런거 된다는데 우리도
되나?"에 대한 답 = **3층은 이미 살아있고, 등록 훅(③) 한 조각만 새로 깔았다.**

| 층 | 내용 | 상태 | 근거/사용법 |
|----|------|------|-------------|
| **① 동적 로딩 = db변경→사이트 자동반영** | 요청마다 데이터 폴더 스캔 | ✅ 상시 | `app.py:_mpm_lab_list()`·`list_cases()` — 폴더만 떨구면 다음 새로고침에 뜸 |
| **② push→Render 자동배포 (CD)** | 커밋 → 사이트 갱신 | ✅ 설정됨 | `render.yaml` (gunicorn). Render 대시보드에서 repo 연결 시 자동 |
| **③ 결과회수 자동화** | 원격 계산완료 → db 등록 훅 | ✅ **이번에 추가** | `webapp/mpm_lab_register.py` (아래) |
| **④ Trust 게이트 자동 배지** | 수렴·잔차·물리범위 → 배지 | ✅ DEM 있음 / MPM은 등록시 데이터 임베드 | `_build_trust_card`(DEM Stage-E) + 등록 훅이 `meta.trust` 채움 |

핵심: **①이 있으므로 ③이 폴더만 올바르게 쓰면 사이트는 자동으로 갱신된다.**
등록 훅은 그 "올바른 폴더 쓰기"(라우트와 동일 meta) + trust 계산을 담당.

---

## ③ 등록 훅 — `webapp/mpm_lab_register.py`

Flask 무의존(순수 stdlib + 선택 requests).  `/mpm-lab/upload` 라우트와 **같은
`build_meta`/`register_local`** 을 import → 웹 업로드든 CLI 훅이든 meta.json 이
바이트-동형(single source of truth, drift 불가).

### 등록 경로 3종 (호스트 토폴로지에 맞게 택1)

```bash
# ⓐ 로컬/공유 파일시스템 (webapp 이 같은 디스크/NFS 를 읽을 때 — WSL·공유마운트)
python webapp/mpm_lab_register.py --payload out/mpm_payload.json \
    --name "DBE_2C_N10" --dest /shared/dem/webapp/mpm_lab

# ⓑ 실행중 원격 webapp 으로 HTTP push (Render 등 — 파일시스템 접근 불가)
python webapp/mpm_lab_register.py --payload out/mpm_payload.json \
    --name "DBE_2C_N10" --url https://dem-analyzer.onrender.com/mpm-lab/upload

# ⓒ 로컬 등록 후 원격 호스트로 rsync(ssh) — V100 → webapp 호스트
python webapp/mpm_lab_register.py --payload out/mpm_payload.json \
    --name "DBE_2C_N10" --dest ./_stage --rsync user@webhost:/srv/dem/webapp/mpm_lab
```

- `--dest` 기본값 = `$WEBAPP_MPM_LAB_FOLDER` 또는 `webapp/mpm_lab`.
- `--url` 은 서버가 자기쪽 `build_meta` 로 등록(4xx 즉시실패, 5xx/네트워크만 2·4·8·16s 백오프 재시도).
- `--rsync` 의 ssh 키/자격은 사용자 환경(원격 실행 컨테이너엔 ssh 없음).  `--dry-run` 으로 명령만 확인.

### V100 배치 스크립트 끝에 붙이는 훅 예시

```bash
# ... STEP1~4 계산이 out/mpm_payload.json 을 생성한 뒤 ...
python webapp/mpm_lab_register.py \
    --payload out/mpm_payload.json \
    --name "${CASE}_${RATE}_N${CYCLE}" \
    --url "$WEBAPP_URL/mpm-lab/upload"   # 또는 --dest $SHARED/mpm_lab
```
→ 성공 시 `✓ 등록: <pid>  porosity 12.7%  trust=ok` 출력.  사이트는 새로고침만
하면 목록에 등장(②의 재배포조차 불필요 — 데이터-폴더 변경은 ①로 즉시 반영).

---

## ④ trust 필드 (등록시 자동 계산, `meta.json` 에 임베드)

`compute_trust(mpm_metrics)` 는 **payload 가 이미 기록한 실제 값만** 읽는다
(fabricate 없음):

```json
"trust": {
  "overall": "ok" | "warn" | "na",
  "converged": true,
  "n_warn": 0,
  "badges": [
    {"key": "sigma_e",  "label": "σ_e (전자)",   "status": "ok", "resid": 1e-9},
    {"key": "thermal",  "label": "κ (열전도)",   "status": "ok", "resid": 1e-8},
    {"key": "porosity", "label": "공극률 물리범위", "status": "ok", "detail": "12.7%"}
  ]
}
```

- 판정 소스: STEP3 `cg_resid`/`ion_resid`, thermal/pore/rxn 의 `resid`·`kcl_err`,
  payload 가 심어둔 `'⚠UNCONVERGED'` 마커, 그리고 porosity 물리범위(0<ε<60%,
  0%/None = 과압축 sentinel → warn).
- `overall='na'` = STEP3 미실행(`--no-thermal`/`--no-step3`) → 수렴 판정 대상 없음(구조 배지만).
- 목록/요약 UI 가 `meta.trust.overall` 을 읽어 ✓/⚠ 배지를 붙일 수 있음(데이터는 준비됨;
  MPM 목록 배지 렌더는 별도 UI 작업 = 파이프라인 ④의 프론트-측, 필요시 추가).

---

## 안 되는 것 / 주의

- **Render 디스크는 ephemeral** — `--url` HTTP push 로 올린 payload 는 재배포/재시작 시
  사라질 수 있음.  영속이 필요하면 Render Persistent Disk 를 `WEBAPP_MPM_LAB_FOLDER`
  로 마운트하거나, 공유 오브젝트 스토리지 뒤에 두어야 함(현재 미구성).
- 대형 payload(35MB/건)를 **git 에 커밋하지 말 것** — ②(CD)는 코드/템플릿 갱신용이지
  결과 데이터 운반용이 아님.  결과는 ③(등록 훅)으로.
- 원격 실행 컨테이너(이 세션)엔 ssh/scp 없음 → `--rsync` 명령은 사용자가 V100 에서 실행.
