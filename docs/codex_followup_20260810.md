# Codex 업데이트 팔로우업 — 2026-08-10

토큰이 없어 Codex 에서 진행된 분량을 이쪽 노트에서 따라 읽은 기록.  세미나 대본이
"다음"으로 지목한 항목을 Codex 가 실제로 만들었고, 그 과정에서 **우리 쪽 앵커 하나가
지금 상태로는 성립하지 않는다**는 것이 드러났다.

## 1. Codex 가 올린 것 (4 커밋, 2 브랜치)

| 커밋 | 날짜 | 브랜치 | 내용 |
|---|---|---|---|
| `b9f1385c` | 08-08 | `Codex/friendly-meitner-lldvar` | PTFE–LiNiO₂ UMA pose-screen 패키지 (2,518 줄) |
| `dde6b77c` | 08-08 | 〃 | 그 패키지의 **VASP 검증 단계** 완성 (2,817 줄) |
| `b4f589c0` | 08-07 | 〃 | DFT 대시보드 회답 검증 1라운드 |
| `2be72b04` | 08-07 | 〃 | 〃 2라운드 |
| `ee445817` | 08-07 | `Codex/dem-mpm-crosscheck` | AGENTS.md worktree 계약 (이미 반영됨) |

세미나 대본과의 연결: `docs/seminar_20260806_script.md` 가 남은 것으로 **E_bind DFT**
(§393·§623) 와 **MLIP(MACE/UMA) 로 DFT 앵커 생산**(§403) 을 지목했다.  Codex 의 두
커밋이 정확히 그 두 줄이다 — 세미나에서 약속한 것의 이행.

## 2. 패키지가 지지하는 것 / 지지하지 못하는 것

`SCIENTIFIC_SCOPE.md` 가 스스로 그은 선이 매우 엄격하고, 우리 §F1 과 정확히 같은 태도다:

**UMA 단계가 줄 수 없는 것 (문서가 직접 열거)** — 인용 가능한 흡착·결합 에너지 ·
Li자리 vs Ni자리 본질적 선호 · dimer↔C10 접착의 정량 비교 · 무한사슬 PTFE 접착 ·
전하이동/Ni 산화·자기상태/C–F 절단/LiF 생성.  이유가 "수치 노이즈"가 아니라
**모델-물리 불일치** 라고 못박았다 (`oc20` 은 분산 없음 + 산화물 제외).

**VASP 단계**: PAW-PBE · ENCUT 520 · Dudarev U_eff(Ni)=6.2 · IVDW=11 · dipole 보정 ·
2×3×1 → 3×4×1 · 자기초기화 2종 · clean-slab + gas 참조.  그래도 `MANUAL_MAGNETIC_
AUDIT_REQUIRED` 로 남고, U·분산·coverage·슬랩두께 민감도는 미결이라고 명시.

**`RELEASE_VALIDATION.md` 는 계산 결과가 아니다** — 가짜 OUTCAR fixture 로 코드 경로가
통과·차단되는지만 본 회귀검증이고, 문서 첫 줄이 "여기 에너지는 과학적으로 인용 금지"
라고 스스로 적었다.  즉 **패키지는 준비됐고 아직 안 돌았다.**

## 3. ★ 발견 — SDCP E_bind 앵커는 지금 상태로 성립하지 않는다

CLAUDE.md 는 `A4′(SDCP) 🔶 잔여 = E_bind DFT만` 으로 적고 있고, SDCP 원고
(`manuscript_sdcp_sigma_e_mechanism.md` §277-278) 는 PTFE 반감의 접착 비용을 SDCP
계면-앵커링이 갚는다는 주장을 **"E_bind 재계산 대기"** 로 걸어 뒀다.  그 비교가
성립하려면 SDCP 쪽과 PTFE 쪽이 **같은 도구·같은 슬랩·같은 프로토콜**이어야 한다.
실제로는 셋 다 어긋나 있다:

| 축 | SDCP 쪽 (`claude/friendly-meitner`) | PTFE 쪽 (Codex 신규) |
|---|---|---|
| 도구 | **UMA-s-1p1 / oc20** (MLIP) | UMA 로 자세만 고르고 **VASP PBE+U+D3** 로 검증 |
| 슬랩 | LiNiO₂(104) **96 원자** (Li24 Ni24 O48) | **192 원자** 1×4 (Li48 Ni48 O96) |
| 산출 | `db/properties/sdcp_linio2_binding_phaseA.csv` — E_bind −5.196 … −1.6 eV | 아직 없음 (패키지만) |

세 가지가 동시에 걸린다:

1. **도구**: SDCP Phase A 의 E_bind 는 UMA 값이다 (`kb/projects/sdcp_linio2_binding.md`
   가 "task=oc20 로 rigid scan 정상화 … best E_bind = −4.75 eV" 라고 기록;
   7단계 "Top-1 → DFT single-point 검증" 은 **선택으로 남고 실행 안 됨**).
   그런데 Codex 의 scope 문서가 **"UMA 는 인용 가능한 결합 에너지를 지지하지 못한다"**
   고 명시했다.  같은 도구·같은 task 이므로 그 판정이 SDCP 쪽에도 그대로 적용된다.
   ⇒ **CSV 의 −5.196 eV 는 인용값이 아니라 자세 선별 점수다.**
2. **슬랩**: Codex `PROVENANCE.md` 가 96-원자 `sdcp_phaseB_*` 계보를 **"retired"** 로
   부르고 자기는 현행 192-원자 슬랩을 쓴다고 적었다.  두 값은 다른 표면 위의 값이다.
3. **프로토콜**: PTFE 는 U_eff(Ni)=6.2 + D3, SDCP 쪽 QE 입력은 `scf_u0.in` (U=0).

⇒ **좋은 소식**: Codex 가 만든 것은 "PTFE 반쪽"이 아니라 **양쪽이 함께 서야 할 기준선**
이다.  같은 패키지에 SDCP 분자를 태우면 도구·슬랩·프로토콜 세 축이 한 번에 정렬된다.
⇒ **해야 할 것**: SDCP 를 **192-원자 슬랩 + 같은 VASP 프로토콜**로 재계산.  그 전까지
원고의 접착-보상 주장은 **정성 방향까지만** 이고, CSV 값을 숫자로 쓰면 안 된다.
(원고가 이미 "E_bind 재계산 대기"로 적어 둔 것이 옳았다 — 이번 확인은 그 대기 사유를
"아직 안 했다"에서 **"세 축이 어긋나 있다"** 로 구체화한 것이다.)

⚠ 부수 확인: 슬랩은 **LiNiO₂** 이고 우리 AM 은 **NMC811** 이다.  Ni-endmember 프록시로
합당하지만 라벨은 유지해야 한다 — 이건 Codex 패키지의 흠이 아니라 원래 있던 근사다.

## 4. 우리 브랜치로 옮긴 것 / 옮기지 않은 것

Codex 의 대시보드 검증 2건은 `webapp/data.py`·`canonical registry` 대상 = **다른
워크스트림**(DFT 대시보드)이고 우리 브랜치엔 그 파일 자체가 없다.  다만 한 건은
코드가 달라도 **같은 결함**이라 옮겼다:

- **옮김 — Windows `os.replace` 간헐 실패.**  Codex 실측: 12 프로세스 × 100 건 × 10 회
  에서 `PermissionError [WinError 5]` 로 **992/1000** 만 저장.  락은 정상이었고(임계구역
  동시성 1) 원인은 백신·인덱서 같은 **외부 handle** 이라 락으로 못 막는다.  우리
  `pipeline_service.atomic_write_json` 도 무방비 `os.replace` 였고 Windows 는 실제 배포
  대상이다(F-18 이 이미 열려 있음).  → `_replace_retry` (PermissionError/EACCES 에만
  5회 지수 backoff, 그 외 OSError 는 즉시 올림, 소진 시 예외).  Codex 의 "24 건 한 번
  통과로는 못 잡는다"를 받아 회귀는 **주입식** 4건(20~23)으로 짰다 — 리눅스에선 이
  예외가 안 나므로 `os.replace` 를 대역으로 바꿔 검증한다.  47/47 PASS.
- **안 옮김 — `mkdir` stale lock 복구 없음.**  우리 `network_lock` 은 `mkdir` 이 아니라
  **flock/msvcrt 를 열린 파일 핸들**에 건다.  프로세스가 죽으면 OS 가 푼다 → stale lock
  자체가 생기지 않는다.  Codex 가 권고한 형태를 이미 쓰고 있다.

## 5. 브랜치 상태

`Codex/friendly-meitner-lldvar` 와 `claude/friendly-meitner-lldvar` (litdb 정본) 가
갈라져 있다 — Codex 쪽 4 · claude 쪽 11.  **양쪽이 함께 건드린 파일은 0개**라 병합은
충돌 없이 된다 (merge-base 대비 변경 파일 교집합 공집합 확인).  Codex 4 커밋은
`tools/sdcp/ptfe_linio2_uma/*` 와 신규 문서 2건만 건드린다.

⚠ litdb 규약상 정본 서랍은 `claude/friendly-meitner-lldvar` 하나다.  PTFE 패키지가
그쪽에 올라가야 SDCP 자산(`db/properties/sdcp_*`, `db/structures/sdcp_phaseB_*`)과
같은 트리에서 §3 의 재계산을 걸 수 있다.  **병합은 그 브랜치 소관이라 여기서 하지
않았다** — 이 문서는 팔로우 기록이다.

## 6. 다음

1. **(정본 브랜치)** Codex 4 커밋을 `claude/friendly-meitner-lldvar` 로 병합 — 충돌 없음.
2. **(§3 해소)** SDCP 분자를 Codex 패키지에 태워 **192-원자 슬랩 + 같은 VASP 프로토콜**로
   재계산.  그래야 PTFE↔SDCP E_bind 가 같은 자로 잰 값이 된다.
3. **(그 전까지)** `sdcp_linio2_binding_phaseA.csv` 의 E_bind 를 **자세 선별 점수**로
   라벨.  원고·세미나에서 숫자로 인용 금지, 방향(doped ≫ neutral)만.
4. **(우리 쪽)** 없음 — Windows 건은 반영·푸시 완료.
