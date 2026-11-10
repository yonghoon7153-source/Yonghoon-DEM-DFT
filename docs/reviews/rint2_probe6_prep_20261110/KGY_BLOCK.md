# kgy 에 붙여 넣을 블록 (⑥ SBE 수치 탐침 · σ 봉인 · 시도 1)

- 붙이는 자리: kgy 의 bash 프롬프트 (R 런을 돌릴 그 계정). 블록은 통째로 붙인다.
- `<PIN>` 은 본 세션이 커밋 · push 뒤 40 자리 커밋 번호로 채운다 (그 전에는 블록이 "PIN is not a 40-hex commit" 으로 멈춘다).
- `BASE` 는 등록 R §10-1 (0) 의 기준 체크아웃 자리다. 같은 저장소의 작업 트리면 어느 것이든 된다 (11-09 현장 자격 블록은 10-24 에 만든 작업 트리를 기준으로 썼다 · `docs/reviews/rint2_siteq_prep_20261109/README.md` §3). 본 세션이 `<PIN>` 과 함께 확인해 채운다. 자리가 다르면 블록이 "BASE is not a git checkout" 으로 멈추고 아무것도 만들지 않는다.
- 블록은 작업 트리 · 출력 폴더 · 로그 폴더를 새로 만들고 감시 셸을 nohup 으로 띄운 뒤 바로 돌아온다. 접속을 끊어도 된다.
- 같은 날 다시 띄우면 출력 폴더 · 로그 폴더가 새 이름 (시각) 으로 따로 생긴다. 앞 시도의 폴더는 지우지 않는다.

```bash
bash <<'P6'
set -u
PIN='<PIN>'
MAXITER=1500000
BASE="$HOME/dem-mt"
BR=claude/stoic-knuth-NObVQ
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
W="$HOME/dem-p6-$(printf %.9s "$PIN")"
O="$HOME/sdcp/ca1_probe6_${STAMP}_arm1"
L="$HOME/p6log_${STAMP}"
T="$W/docs/reviews/rint2_probe6_prep_20261110/tools"
stop() { echo "[p6] STOP: $*"; exit 2; }
printf '%s' "$PIN" | grep -Eqx '[0-9a-f]{40}' || stop "PIN is not a 40-hex commit (nothing written)"
for p in "$O" "$L"; do if [ -e "$p" ]; then stop "$p already exists (nothing written)"; fi; done
[ -f "$HOME/dem-venv/bin/activate" ] || stop "venv not found (nothing written)"
[ -d "$HOME/sdcp/kit_SBE_vgcf100" ] || stop "kit not found (nothing written)"
git -C "$BASE" rev-parse --git-dir > /dev/null 2>&1 || stop "BASE is not a git checkout - fix the BASE line (nothing written)"
if [ -e "$W" ]; then echo "[p6] reusing worktree $W"; else
  git -C "$BASE" fetch -q origin "$BR" || stop "git fetch failed (nothing written)"
  git -C "$BASE" worktree add -q --detach "$W" "$PIN" || stop "git worktree add failed"
fi
[ "$(git -C "$W" rev-parse HEAD)" = "$PIN" ] || stop "worktree HEAD differs from PIN"
[ -f "$T/run_probe6.sh" ] || stop "watcher not found in the pinned worktree"
umask 022
mkdir "$L" || stop "cannot create $L"
setsid nohup bash "$T/run_probe6.sh" "$W" "$O" "$L" "$PIN" "$MAXITER" > "$L/nohup.out" 2>&1 < /dev/null &
sleep 5
echo "[p6] started - log folder $L"
tail -n 3 "$L/nohup.out"
echo "[p6] progress:  tail -n 3 $L/status.log"
echo "[p6] stop early: kill -TERM \$(cat $L/watcher.pid)"
echo "[p6] when done: the file $L/DONE appears - send back $L/probe6_bundle.tgz and the last 3 lines of $L/status.log"
P6
```

## 화면에 나오는 것

- 블록: `[p6]` 줄 (로그 폴더 자리 · 진행 보는 명령 · 끝난 뒤 묶음 자리) 과 감시 셸의 첫 세 줄.
- 감시 셸 (`nohup.out` · `status.log`): `[probe6]` 로 시작하는 줄만. 시작 · 진행 줄 (시작 직후 한 번 + 10 분마다 · 경과 초 · 단계 · 로그 줄 수 · 호스트 메모리 · GPU 메모리) · 러너 종료 코드 · 판독 결과 표 · 묶음 자리와 sha256 · `DONE`. 시작 직후 진행 줄의 GPU 메모리가 이미 크면 다른 작업이 GPU 를 쓰고 있다는 뜻이다.
- 판독 결과 표: 반복 수 (주 풀이 · 이어 풀기) · 잔차 · 판 전류 불균형 · 수렴 여부 (증서 ⓐⓑⓒⓓ 통과 표지 · 상태 이름) · 백엔드 · 미지수 수 · 시간 · 메모리 · 환경 지문 (판) · 파일 sha256.
- 멈추면 `STOP: <사유> (runner not started)` 한 줄. 이때는 러너가 돌지 않았다. 그 줄을 그대로 보내 주면 된다.

## 화면에 안 나오는 것

- 러너와 payload 의 화면 출력은 한 줄도 화면에 나오지 않는다. 전부 로그 폴더의 runner.log 로만 간다.
- σ (전자 전도도) · 판 전류 · 저항 · 소산 몫 · 증서의 목표량 구간 같은 값은 화면 · `status.log` · 묶음 어디에도 없다. 팔 JSON 과 영수증은 출력 폴더에 그대로 있고 묶음에는 그 파일들의 sha256 만 들어간다.
- runner.log 와 출력 폴더의 팔 JSON 은 열어 보지 않는다 (σ 가 들어 있다). 보고에 필요한 수치는 묶음에 다 있다.

## 끝난 뒤 보낼 것

- 로그 폴더의 `probe6_bundle.tgz` 한 파일 (수십 KB) 과 `status.log` 끝 세 줄.
- 러너가 실패했어도 묶음은 만들어진다. 출력 폴더 · 로그 폴더 · 킷 런 폴더에 남은 파일은 지우지 않는다.

## 중간에 멈추려면

- 블록이 찍어 준 `stop early` 줄을 그대로 친다 (로그 폴더의 watcher.pid 에 적힌 감시 셸에 TERM). 감시 셸이 러너와 그 자식을 끝내고 기록 · 묶음을 남긴다. 러너만 직접 죽이지 않는다.
