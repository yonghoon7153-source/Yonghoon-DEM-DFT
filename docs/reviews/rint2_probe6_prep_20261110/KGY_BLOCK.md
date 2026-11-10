# kgy 에 붙여 넣을 블록 (⑥ SBE 수치 탐침 · σ 봉인 · 시도 1 · 시도 2)

- 붙이는 자리: kgy 의 bash 프롬프트 (R 런을 돌릴 그 계정). 블록은 통째로 붙인다.
- 시도는 둘이다 (1저자 11-10). **시도 1** = 짧은 확인: `ATTEMPT=1` · 반복 한도 30000. 한도에 닿아 끝나는 것이 정상이다 (반복당 초와 한도에서의 잔차를 얻고 kgy 에서 전 과정을 한 번 확인한다). **시도 2** = 본 한도: `ATTEMPT=2` · 반복 한도 1500000. 블록의 `ATTEMPT=1` 줄을 `ATTEMPT=2` 로 바꾸는 것 말고는 같은 블록이다. 한도는 블록 안의 표가 시도 번호로 정한다 (손으로 넣지 않는다).
- 시도 2 는 시도 1 의 로그 폴더 (`~/p6log_a1_<시각>`) 에 `DONE` 이 있어야 띄운다 (블록이 본다 · 그 폴더 meta 의 핀이 이번 `<PIN>` 이거나 그 앞 커밋이어야 한다). 시도 1 이 한도에 닿아 끝난 것 (러너 rc 1 · 판독 rc 3) 도 정상 끝이고 `DONE` 이 생긴다. 시도 1 이 `STOPPED` 로 끝났으면 (러너를 띄우기 전 멈춤 · 풀이 0) 사유를 고친 뒤 시도 1 블록을 그대로 다시 붙인다.
- `<PIN>` 은 본 세션이 커밋 · push 뒤 40 자리 커밋 번호로 채운다 (그 전에는 블록이 "PIN is not a 40-hex commit" 으로 멈춘다). 블록은 fetch 한 뒤 `<PIN>` 이 가지 끝과 같은지 본다 (다르면 멈춘다). 두 시도 사이에 원장 줄을 커밋하면 가지 끝이 바뀌므로 시도 2 의 `<PIN>` 은 그 새 끝이다.
- `BASE` 는 등록 R §10-1 (0) 의 기준 체크아웃 자리다. 같은 저장소의 작업 트리면 어느 것이든 된다 (11-09 현장 자격 블록은 10-24 에 만든 작업 트리를 기준으로 썼다 · `docs/reviews/rint2_siteq_prep_20261109/README.md` §3). 본 세션이 `<PIN>` 과 함께 확인해 채운다. 자리가 다르면 블록이 "BASE is not a git checkout" 으로 멈추고 아무것도 만들지 않는다.
- 블록은 작업 트리 · 로그 폴더를 새로 만들고 감시 셸을 nohup 으로 띄운 뒤, 감시 셸의 첫 판단 (`runner started` 줄 또는 `STOP` 줄) 을 최대 180 초 기다려 그 줄을 찍고 돌아온다. 그 뒤에는 접속을 끊어도 된다.
- 같은 날 다시 띄우면 출력 폴더 · 로그 폴더가 새 이름 (시각) 으로 따로 생긴다. 앞 시도의 폴더는 지우지 않는다.

```bash
bash <<'P6'
set -u
PIN='<PIN>'
ATTEMPT=1
BASE="$HOME/dem-mt"
BR=claude/stoic-knuth-NObVQ
stop() { echo "[p6] STOP: $* (runner not started)"; exit 2; }
case "$ATTEMPT" in
  1) MAXITER=30000;;
  2) MAXITER=1500000;;
  *) stop "ATTEMPT must be 1 or 2 (nothing written)";;
esac
printf '%s' "$PIN" | grep -Eqx '[0-9a-f]{40}' || stop "PIN is not a 40-hex commit (nothing written)"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
W="$HOME/dem-p6-$(printf %.9s "$PIN")"
O="$HOME/sdcp/ca1_probe6_a${ATTEMPT}_${STAMP}_arm1"
L="$HOME/p6log_a${ATTEMPT}_${STAMP}"
T="$W/docs/reviews/rint2_probe6_prep_20261110/tools"
for p in "$O" "$L"; do if [ -e "$p" ]; then stop "$p already exists (nothing written)"; fi; done
[ -f "$HOME/dem-venv/bin/activate" ] || stop "venv not found (nothing written)"
[ -d "$HOME/sdcp/kit_SBE_vgcf100" ] || stop "kit not found (nothing written)"
git -C "$BASE" rev-parse --git-dir > /dev/null 2>&1 || stop "BASE is not a git checkout - fix the BASE line (nothing written)"
for d in "$HOME"/p6log_*; do
  [ -d "$d" ] || continue
  if [ -e "$d/DONE" ] || [ -e "$d/STOPPED" ] || [ -e "$d/WATCHER_FAILED" ]; then continue; fi
  stop "earlier log folder $d has no end marker (DONE / STOPPED / WATCHER_FAILED): a watcher still runs there or died - look at its status.log (nothing written)"
done
git -C "$BASE" fetch -q origin "$BR" || stop "git fetch failed (nothing written)"
TIP="$(git -C "$BASE" rev-parse FETCH_HEAD)"
[ "$TIP" = "$PIN" ] || stop "PIN is not the tip of $BR after the fetch (tip $TIP) - use the tip or fix the PIN line (only git fetch ran)"
if [ "$ATTEMPT" = 2 ]; then
  OK1=0
  for d in "$HOME"/p6log_a1_*; do
    [ -f "$d/DONE" ] && [ -f "$d/meta.txt" ] || continue
    P1="$(sed -n 's/^pin=//p' "$d/meta.txt")"
    if [ "$P1" = "$PIN" ] || git -C "$BASE" merge-base --is-ancestor "$P1" "$PIN" 2>/dev/null; then OK1=1; fi
  done
  [ "$OK1" = 1 ] || stop "attempt 2 needs an attempt-1 log folder with DONE whose pin is this PIN or an earlier commit of it (only git fetch ran)"
fi
if [ -e "$W" ]; then echo "[p6] reusing worktree $W"; else
  git -C "$BASE" worktree add -q --detach "$W" "$PIN" || stop "git worktree add failed"
fi
[ "$(git -C "$W" rev-parse HEAD)" = "$PIN" ] || stop "worktree HEAD differs from PIN"
[ -f "$T/run_probe6.sh" ] || stop "watcher not found in the pinned worktree"
umask 022
mkdir "$L" || stop "cannot create $L"
setsid nohup bash "$T/run_probe6.sh" "$W" "$O" "$L" "$PIN" "$MAXITER" > "$L/nohup.out" 2>&1 < /dev/null &
echo "[p6] watcher launched - attempt $ATTEMPT, maxiter $MAXITER, log folder $L"
M=""
i=0
while [ "$i" -lt 90 ]; do
  sleep 2
  i=$((i + 1))
  M="$(grep -e 'runner started' -e 'STOP:' "$L/nohup.out" 2>/dev/null | head -n 1)"
  if [ -n "$M" ]; then break; fi
done
grep -e 'pre-launch' "$L/nohup.out" 2>/dev/null | head -n 1
if [ -z "$M" ]; then
  echo "[p6] still checking after 180 s (no runner-started or STOP line yet) - look again with: tail -n 3 $L/status.log"
else
  echo "$M"
fi
echo "[p6] progress:  tail -n 3 $L/status.log"
echo "[p6] stop early: kill -TERM \$(cat $L/watcher.pid)"
echo "[p6] when done: the file $L/DONE appears - send back $L/probe6_bundle.tgz and the last 3 lines of $L/status.log"
case "$M" in *STOP:*) exit 2;; esac
P6
```

## 블록이 멈추는 조건 (`[p6] STOP: ... (runner not started)` · 종료 코드 2 · 러너는 돌지 않았다)

- fetch 전 (`nothing written`): ATTEMPT 가 1 · 2 가 아님 · PIN 이 40 자리 hex 가 아님 (`<PIN>` 을 안 채운 것 포함) · 출력 폴더나 로그 폴더가 이미 있음 · venv · 킷 없음 · BASE 가 git 저장소가 아님 · 앞 로그 폴더 (`~/p6log_*`) 가운데 끝 표지 (DONE · STOPPED · WATCHER_FAILED) 가 없는 것이 있음 (감시 셸이 아직 돌거나 죽었다 · 그 폴더의 status.log 를 먼저 본다) · fetch 실패.
- fetch 뒤 (`only git fetch ran`): PIN 이 가지 끝이 아님 · 시도 2 인데 시도 1 의 DONE 폴더 (핀 = 이번 PIN 이거나 그 앞 커밋) 가 없음. 그 뒤 작업 트리 단계의 멈춤 (worktree add 실패 · HEAD 다름 · 감시 셸 없음) 은 작업 트리를 만들었을 수 있다.
- 감시 셸이 띄워진 뒤의 멈춤은 블록이 감시 셸의 STOP 줄을 그대로 찍어 준다 (아래).

## 화면에 나오는 것

- 블록: `[p6] watcher launched - attempt <N>, maxiter <M>, log folder <L>` → 감시 셸의 발사 전 줄 (`pre-launch: attempt N, GPU memory in use ... MiB of ... MiB, disk free ... GB (kit root) and ... GB (log folder)` · 멈춤 기준은 없다) → 감시 셸의 `runner started - maxiter ...` 줄 또는 `STOP: <사유> (runner not started)` 줄 → 진행 보는 명령 · 일찍 멈추는 명령 · 끝난 뒤 보낼 것. 180 초 안에 둘 다 안 나오면 "still checking" 줄과 다시 보는 명령을 찍는다 (감시 셸이 러너의 규율 검사를 미리 한 번 돌린다 · 그 검사 = 게이트 기계에서 약 90 초 · kgy 실측 없음).
- 감시 셸 (`nohup.out` · `status.log`): `[probe6]` 로 시작하는 줄만. 시작 · 발사 전 · 진행 줄 (시작 직후 한 번 + 10 분마다 · 경과 초 · 단계 · 로그 줄 수 · 호스트 메모리 · GPU 메모리) · 러너 종료 코드 · 판독 결과 표 · 묶음 자리와 sha256 · `DONE`. 발사 전 줄의 GPU 메모리가 이미 크면 다른 작업이 GPU 를 쓰고 있다는 뜻이다.
- 판독 결과 표: 반복 수 (주 풀이 · 이어 풀기) · 잔차 · 판 전류 불균형 · 수렴 여부 (증서 ⓐⓑⓒⓓ 통과 표지 · 상태 이름) · 백엔드 · 미지수 수 · 시간 · 메모리 · 환경 지문 (판) · 파일 sha256 · 시도 번호.
- 감시 셸이 러너를 띄우기 전에 멈추면 `STOP: <사유> (runner not started)` 한 줄이 화면 (블록이 찍어 준다) · nohup.out · status.log 에 남고, 로그 폴더에 `STOPPED` 표지 (사유 · `runner_started=0`) 가 생긴다. 그 줄을 그대로 보내 주면 된다. 감시 셸이 로그 폴더를 받기 전의 멈춤 (경로 글자 · 로그 폴더가 새것이 아님 · 인자 수) 만은 표지 없이 nohup.out 의 줄로 남는다. 그때는 다음 블록이 "has no end marker" 로 멈추므로, 그 줄을 본 세션에 보낸 뒤 그 폴더에 `STOPPED` 파일을 손으로 만든다 (`echo 'reason=see nohup.out' > <L>/STOPPED` · 폴더는 지우지 않는다).

## 화면에 안 나오는 것

- 러너와 payload 의 화면 출력은 블록 화면 · nohup.out · status.log 에 한 줄도 나오지 않는다. 전부 로그 폴더의 runner.log 로 간다. 판독기는 runner.log 에서 아는 줄의 수 (반복 한도 · rtol · dof · 잔차 · 초 · 미수렴 줄의 info · 잔차 · 증서 실패 줄의 상태 · ⓐⓑⓒⓓ · 불균형) 만 다시 적고, 실패 표지가 든 줄은 수를 `#` 하나로 가린 글로 보고 JSON 과 걸러 낸 로그에 넣는다 (그 둘은 묶음에 들어간다 · 정상 런에도 가린 줄이 몇 줄 있다).
- σ (전자 전도도) · 판 전류 · 저항 · 소산 몫 · 증서의 목표량 구간의 값은 화면 · status.log · 묶음 어디에도 없다. 다만 상태 이름 (예: `VALID_ZERO_TOPOLOGY` = σ 0) 과 가린 실패 줄에 남는 부호 · 낱말 (`-#` · `nan` · `None`) 은 σ 의 상태를 말한다 (README §8).
- 묶음에 드는 것: 판독기의 허용 칸 값 (반복 수 · 잔차 · 불균형 · 수렴 표지 · 백엔드 · 미지수 수 · 신원 대조 결과) · 영수증 칸 (digest · code_sha · 팔 수 · 백엔드 기대 · rtol · vox · PTFE 규약) · 파일 이름 · 크기 · sha256 · 시간 · 메모리 · GPU 표본 · 환경 지문 · meta · 실제로 돈 명령. 팔 JSON · 영수증 · runner.log 는 묶음에 없고 출력 폴더 · 로그 폴더에 그대로 있다.
- runner.log 와 출력 폴더의 팔 JSON 은 열어 보지 않는다 (σ 가 들어 있다). 보고에 필요한 수치는 묶음에 다 있다.

## 끝난 뒤 보낼 것

- 로그 폴더의 `probe6_bundle.tgz` 한 파일과 `status.log` 끝 세 줄. 묶음은 수십 KB 부터다 (표본 파일이 10 초에 한 줄이라 30 시간 런이면 약 1 만 줄 · 압축 전 약 0.6 MB · 산술).
- 러너가 실패했거나 한도에 닿았어도 묶음은 만들어지고 `DONE` 이 생긴다. 출력 폴더 · 로그 폴더 · 킷 런 폴더에 남은 파일은 지우지 않는다.
- 로그 폴더의 끝 표지: `DONE` = 러너가 돌았고 기록이 끝났다 (러너 실패 · 한도 · 일찍 멈춤 포함). `STOPPED` = 러너를 띄우기 전에 멈췄다 (풀이 0). `WATCHER_FAILED` = 러너를 띄운 뒤 감시 셸 자신이 뜻밖에 끝났다 (러너 그룹은 끝냈다 · 기록 불완전 · 잠금 `~/.probe6.lock` 이 남는다 · 본 세션에 알린다). 표지가 없으면 아직 도는 중이거나 감시 셸이 죽었다 (status.log 를 먼저 본다).

## 중간에 멈추려면

- 블록이 찍어 준 `stop early` 줄을 그대로 친다 (로그 폴더의 watcher.pid 에 적힌 감시 셸에 TERM). 감시 셸이 러너의 프로세스 그룹 전체에 TERM 을 보내고 10 초 뒤 남은 것에 KILL 을 보낸 다음 기록 · 묶음 · `DONE` 을 남긴다. 러너만 직접 죽이지 않는다.
- 일찍 멈추면 남는 것: 전체 초 · 메모리 · GPU 표본 · 풀이 시작 줄부터 멈출 때까지의 초 (보고의 `solve_to_end_s`). 남지 않는 것: 반복 수 · 잔차 · 판 전류 불균형 (그 값은 풀이가 끝나야 팔 JSON 에 쓰인다). 다만 주 풀이가 이미 한도에 닿은 뒤 (이어 풀기 중) 에 멈췄으면 payload 가 찍어 둔 "CG not converged" 줄의 info (= 한도) 와 상대 잔차는 남는다 (감시 셸이 러너에 `PYTHONUNBUFFERED=1` 을 줘서 그 줄이 버퍼에 갇히지 않는다).
- 일찍 멈춘 시도도 끝난 시도다 (풀이가 시작됐으면 · meta `solve_started=1`). 다음은 원장의 다음 번호 줄이다.
- `kill -TERM` 을 두 번 쳐도 된다. 끝 기록 중에 온 신호는 미뤄져 보고 · 묶음 · `DONE` 이 남는다 (status.log 에 "held until the record was complete" 줄). `DONE` 뒤에는 watcher.pid 가 지워져 그 줄은 파일이 없다는 말로 끝난다 (다른 프로세스를 겨누지 않는다).
