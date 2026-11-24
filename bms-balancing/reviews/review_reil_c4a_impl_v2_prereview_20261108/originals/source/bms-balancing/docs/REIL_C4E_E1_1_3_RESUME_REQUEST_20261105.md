# REIL C4-E · E1-1–3 재개 요청 — 남은 d · e · f (읽기 경로 · E1-2 fetch · E1-3 run = E3a 66 호출) · 2026-11-05 KST

> **재개 요청서다 (이 문서를 쓰는 동안 실행 0).** 요청서 v3 (`docs/REIL_C4E_E1_1_3_APPROVAL_REQUEST_v3_20261104.md` · `0ffa7291…` · 사전 검토 전체 수용
> §114 · 그대로 둔다) 의 첫 실행 (§115 · §116) 은 E1-1 identity MATCH 뒤 멈췄다. 이 문서는 남은 d · e · f 를 **새 증거 폴더**에서 하자는 요청이다. **v3 와
> 다른 곳은 §2 의 R1–R8 뿐이다** — 초안 셋 · launcher · 다섯 모듈 · 봉인 · 커밋 관문 · 판정 · 멈춤 규칙 · 예산은 v3 그대로다. 검토 뒤 사용자의 재개 승인이
> 있어야 시작한다.

## 0. 왜 멈췄고 무엇을 바꾸나

- **본질:** E1-3 run 은 실제 REIL-UConn LFP 자료로 E3a 66 호출 (확증 fitting) 을 하는 단계이고, E1-2 fetch 는 그 자료를 받는 단계다. 둘 다 아직 0 회다.
- **멈춘 실제 까닭 (§117 에서 §116 정정):** d1 의 `add_repo` 는 이 세션에서 **사용자 승인 카드**를 거친다. 첫 실행에서 d1 호출은 01:20:38Z (d0 의 2 s 뒤) 에
  나갔고, 카드가 답 없이 남아 있다가 04:16:38Z 의 다음 사용자 메시지로 닫혔다 — 도구 반환 "Tool call not completed: an approval request was still unanswered
  when the message that follows arrived and was closed, so the action awaiting approval did not run." 그사이 f 의 시작 상한 (T_a + 7,200 s = 03:15:01Z) 이
  지났다. 같은 세션의 이전 `add_repo` 네 번 (2026-10-13 · 10-14) 도 반환까지 약 5–30 분 (승인 대기) 이 걸렸다.
- **그래서 재개는 d 를 시계 (a0) 앞으로 옮긴다:** 사용자가 재개를 승인한 직후 (사용자가 앱에 있을 때) d1 을 부르고 카드 승인을 받은 뒤 a0 를 찍는다.
  시계 안에는 사람의 응답을 기다리는 단계가 없다.

## 1. 첫 실행에서 인용하는 것 · 그대로 두는 것

- **인용 (다시 돌리지 않음):** E1-1 identity MATCH — `evidence/reil_c4e1_20261105/03_identity.*` (열여덟 · 커밋 `b5decbbe` · 판정기 43 항목 실패 0 = 수동
  판정 · launcher rc 0).
- **c 를 다시 돌리지 않는 까닭:** launcher 의 작업 폴더는 상수 `WORK = SP / "c4e1"` (launcher 74 행) 이고, 첫 실행이 만든 identity 의 pycache 폴더
  `SP/c4e1/pycache/03_identity` (빈 폴더) 가 있어 launcher 가 identity 를 거부한다 (`launch` 841 행 — "새 빈 폴더만"). 그 폴더를 지우거나 이름을 바꾸는 것
  · launcher 를 바꾸는 것은 범위 밖이다. fetch · run 은 `03_identity.json` 을 읽지 않는다 — fetch 사전 검사는 자료 폴더 없음 (567 행) · 원천 확인, run 은 자료
  두 파일 대조 (613 행) 와 `run/IDENTITY.json` 의 모듈 다섯 시작 · 끝 행 = 사전 대조 (`identity_link` 576 · 619 행) 다.
- **그대로 둔다 (지우기 · 이름 바꾸기 · 다시 쓰기 0):** `evidence/reil_c4e1_20261105/` 전체 · `SP/detach_probe_20261105` · `SP/c4e1/` 의 빈 폴더 넷 (`mpl` ·
  `pycache` · `pycache/03_identity` · `tmp`) · `SP/e113_commit_{b,c,g}.{cached,index}`.

## 2. v3 와 다른 곳 (전부)

| # | v3 | 재개 | 까닭 |
|---|---|---|---|
| R1 | 순서 a → p → b → c → d → e → f → g | **d0–d3 → a → p → b → d4 → e → f → g** (c 없음) | d1 의 승인 카드를 시계 밖에서 · c 는 §1 |
| R2 | d3 이 `<E>/03_read_path.json` 에 쓴다 | d3 의 마지막 인자만 `SP/e113_resume_read_path.json` (형식 · 다섯 상태 · 반환 3 그대로) · b 뒤 **d4** 가 `<E>/03_read_path.json` 으로 복사 · 대조 → 커밋 관문 (x = `<D>_d`) | `<E>` 는 a0 뒤에 생긴다 |
| R3 | a0 의 시각 제한 없음 | **a0 ≥ 2026-11-06T00:00:00Z (09:00 KST)** · a0 의 D 가 20261105 면 a1 전에 멈춘다 | 이름 규칙 `^reil_c4e1_20[0-9]{6}$` 이 launcher (121 행) · 초안 셋에 고정 · D = a0 의 UTC 날짜 |
| R4 | p1 의 앞 검사 `! compgen -G 'SP/detach_probe_*' > /dev/null` | `[ "$(compgen -G 'SP/detach_probe_*')" = "SP/detach_probe_20261105" ]` (뒤는 그대로) | 첫 실행의 탐침 폴더 하나만 허용 |
| R5 | b1 — 이름 규칙에 맞는 항목 0 · `SP/c4e1` 없음 · `SP/e113_commit_*` 없음 | 항목 = 정확히 `["reil_c4e1_20261105"]` · `SP/c4e1` 안 = 정확히 빈 폴더 넷 (§1) · `SP/e113_commit_<D>_*` 없음 (나머지 그대로) | §1 의 남은 것 |
| R6 | 커밋 관문의 `<x>` = b · c · d · e · f · g | `<x>` = `<D>_b` · `<D>_d` · `<D>_e` · `<D>_f` · `<D>_g` (x4 · x5 의 글자 그대로) | 첫 실행의 `e113_commit_b` · `_g` 와 겹침 (x4 는 `set -C`) |
| R7 | `§NN` = §115 | `§NN` = 재개 승인을 적는 새 절 | — |
| R8 | d 가 어긋나면 멈춤 → g | d 가 어긋나면 (상태가 `attached` · `public_served` 밖 · 카드가 답 없이 닫힘 = `error`) **a0 전에 멈춘다** — `<E>` 없음 · 결과 § 만 | d 가 a 앞 |

## 3. 바뀐 줄 (펼친 꼴 · 나머지 줄은 v3 §4 · §7-3 의 글자 그대로)

자리표시자는 v3 §4 와 같다 (`BMS` · `SP` · `<E>` = `BMS/evidence/reil_c4e1_<D>` · `<P>` = `SP/detach_probe_<D>` · `<D>` = a0 의 UTC 날짜).

```
d0  date -u +%Y-%m-%dT%H:%M:%SZ
d1  [세션 도구] add_repo owner="REIL-UConn" repo="Multi-Objective-Optimization-for-Lithium-Ion-Battery-Degradation-Diagnostics" access="read"
d2  date -u +%Y-%m-%dT%H:%M:%SZ
d3  /usr/bin/python3.11 -I -c 'import json, sys; d = {"kind": "REIL_E113_READ_PATH", "utc_before": sys.argv[1], "utc_after": sys.argv[2], "input": {"owner": "REIL-UConn", "repo": "Multi-Objective-Optimization-for-Lithium-Ion-Battery-Degradation-Diagnostics", "access": "read"}, "status": sys.argv[3], "tool_result_summary": sys.argv[4], "clone_command_executed": False}; sys.exit(3) if d["status"] not in ("attached", "public_served", "refused", "declined", "error") else None; open(sys.argv[5], "x", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True) + "\n")' '<d0 의 출력>' '<d2 의 출력>' '<status>' '<요약>' SP/e113_resume_read_path.json
p1  [ "$(compgen -G 'SP/detach_probe_*')" = "SP/detach_probe_20261105" ] && mkdir <P> && cd <P> && date -u +%s > t0.txt && { setsid nohup sh -c 'echo $$ > pid.txt || { echo "stage=pid rc=$?" > fail.txt; exit 11; }; sleep 150; rc=$?; [ "$rc" -eq 0 ] || { echo "stage=sleep rc=$rc" > fail.txt; exit 12; }; date -u +%s > done.tmp || { echo "stage=done_write rc=$?" > fail.txt; exit 13; }; mv done.tmp done.txt || { echo "stage=publish rc=$?" > fail.txt; exit 14; }' > out.txt 2> err.txt < /dev/null & } && date -u +%s > t_ret.txt
b1  /usr/bin/python3.11 -I -c 'import os, re, sys; e = sorted(n for n in os.listdir("BMS/evidence") if re.fullmatch(r"reil_c4e1_20[0-9]{6}", n)); print(e); sys.exit(0 if e == ["reil_c4e1_20261105"] else 1)' && test ! -e <E> && /usr/bin/python3.11 -I -c 'import os, sys; w = sys.argv[1]; s = sorted(os.path.relpath(os.path.join(r, n), w) for r, d, f in os.walk(w) for n in d + f); print(s); sys.exit(0 if s == ["mpl", "pycache", "pycache/03_identity", "tmp"] else 1)' SP/c4e1 && ! compgen -G 'SP/e113_commit_<D>_*' > /dev/null && test -x SP/reil_c4env/venv/bin/python && mkdir <E>
d4  test ! -e <E>/03_read_path.json && cp SP/e113_resume_read_path.json <E>/03_read_path.json && cmp SP/e113_resume_read_path.json <E>/03_read_path.json
```

- **d:** d3 의 `status` · `요약` 은 v3 §4 · §7-2 그대로 (요약은 비밀 검사 뒤 · 계정 정보 형태가 있으면 적지 않고 그 사실만). 카드를 사용자가 거절하면 `declined`,
  도구가 접근 오류를 돌려주면 `refused`, 카드가 답 없이 닫히거나 반환을 못 받으면 `error` (d1 을 다시 부르지 않는다).
- **d4:** b9 뒤 · e1 전. 반환 0 이면 커밋 관문 (x = `<D>_d` · `<목록 x>` = `<E>/03_read_path.json`).
- 바뀐 네 줄의 앞 검사 (b1 의 두 python · p1 의 비교 · `SP/e113_commit_20261106_*` 부재) 는 이 문서를 쓰며 현재 상태에서 읽기만으로 돌려 보았다 — 모두 반환 0.

## 4. 그대로인 것

- **글자 그대로 쓰는 줄 (자리표시자만):** a0–a2 · p2–p6 · b2–b9 · e1–e7 · f1–f7 · g1 · g3 · x1–x6 · 이름 확인. b2 의 identity helper 복사는 c 가 없어도
  둔다 (b8 의 sha 스물 · b9 의 줄 수 · 끝 기록의 복사본 넷을 그대로 두기 위해서).
- **고정 바이트:** 초안 셋 (`e107d566…` · `ad986c19…` · `0827723f…`) · launcher v6 (`2c707123…`) · 신뢰 목록 · S1 둘 · 봉인 · identity helper (`92bb3bca…`).
- **커밋 단위 · 수:** a 2 (문서) · b 14 · d 1 · e 17 · f 25 · 27 · g 1 (c 없음) · r `07_g3_return_<i>.txt`.
- **예산:** T_a (a0) → g3 의 push 반환 ≤ 21,600 s · R = 1,800 s · f 는 T_a + 7,200 s 안에 시작 (wrapper 가 막는다). d 는 a0 앞이라 예산 밖이다.
- **판정 · 멈춤 · 잔류 (R1) · F3 · 끝 기록 · g3 의 재시도 · 절차 Git:** v3 §5–§8 그대로.
- **실행 방식:** §115 와 같다 — 펼침 도구가 v3 (`0ffa7291…`) 와 이 문서의 sha 를 대조한 뒤, §3 의 줄은 이 문서에서 · 나머지는 v3 에서 자리표시자만 바꿔 펼치고,
  펼친 문자열을 도구 출력에 먼저 남긴 뒤 그대로 `bash -c` 로 실행한다.

## 5. 밝힐 것

1. **E1-1 은 2026-11-05 의 결과다.** 재개 시점에 venv 의 환경 identity (`env_profile`) 를 다시 확인하지 않는다 (launcher 가 막고 · 바꾸는 것은 범위 밖 —
   §1). fetch · run 의 launcher 사전 검사와 run 의 `IDENTITY.json` 모듈 대조는 그대로 돈다.
2. 새 폴더의 `06_end.json` 은 c 의 파일을 "없음" 으로 적는다 (예상된 것 · E1-1 은 §1 의 인용).
3. launcher 가 run 에 넘기는 승인 문구는 고정 "상태 문서 §NN (사용자 E1-1–3 승인 · …)" 이다 — 여기서 §NN 은 재개 승인 절이다.
4. `SP/c4e1/` 은 첫 실행의 빈 폴더 넷 위에서 쓴다 (`mpl` · `tmp` 는 자식 env 의 `MPLCONFIGDIR` · `TMPDIR`).
5. d1 은 사용자가 앱에서 `add_repo` 카드를 승인해야 반환된다. 사용자 승인이 2026-11-06T00:00:00Z 전에 오면 d 는 곧바로 하고 a0 만 그 시각 뒤로 미룬다.

## 6. 하지 않는 것

C4-A / B · COMSOL · launcher · 다섯 모듈 · 봉인 · 초안의 변경 · 설치 · 환경 재구축 · 첫 실행 폴더 · 작업 폴더의 정리 · c 의 재실행.
