# Gabia 실행 명령

서버 저장소가 어느 브랜치에 있든 checkout/switch하지 않아. Codex 브랜치를 fetch한 뒤 **확정된 한 커밋의 이 패키지 폴더만** `/data/work/apps` 아래로 꺼내. 패키지와 결과 폴더 이름에 커밋을 붙이므로 나중에 브랜치가 움직여도 계산 계보가 섞이지 않아.

Gabia 저장소 안의 어느 폴더에 있든 아래 블록을 그대로 실행하면 저장소 루트를 스스로 찾아.

## 1. 패키지 받기

```bash
set -euo pipefail
REPO="$(git rev-parse --show-toplevel)"
cd "$REPO"
git status -sb
git branch --show-current
git fetch origin \
  +refs/heads/Codex/friendly-meitner-lldvar:refs/remotes/origin/Codex/friendly-meitner-lldvar

PKG_COMMIT="$(git rev-parse origin/Codex/friendly-meitner-lldvar)"
APP="/data/work/apps/ptfe_linio2_uma_${PKG_COMMIT:0:12}"
OUT="/data/work/runs/ptfe_linio2_uma_2026_08_08_${PKG_COMMIT:0:12}"
export OUT

if [[ -e "$APP" ]]; then
  test -f "$APP/PACKAGE_COMMIT.txt"
  test "$(cat "$APP/PACKAGE_COMMIT.txt")" = "$PKG_COMMIT"
else
  APP_TMP="${APP}.tmp.$$"
  mkdir -p "$APP_TMP"
  git archive "$PKG_COMMIT" tools/sdcp/ptfe_linio2_uma \
    | tar -xf - -C "$APP_TMP" --strip-components=3
  printf '%s\n' "$PKG_COMMIT" > "$APP_TMP/PACKAGE_COMMIT.txt"
  mv "$APP_TMP" "$APP"
fi

cd "$APP"
chmod +x run.sh watch.sh
printf 'Package commit: %s\nApp: %s\nOutput: %s\n' "$PKG_COMMIT" "$APP" "$OUT"
```

새 셸을 열었다면 아래 두 줄로 같은 실행 문맥을 다시 잡아.

```bash
cd /data/work/apps/ptfe_linio2_uma_<위에 출력된 12자리 커밋>
export OUT=/data/work/runs/ptfe_linio2_uma_2026_08_08_<같은 12자리 커밋>
```

## 2. 실행 전 환경 점검

```bash
./run.sh check
```

`pw.x` 또는 다른 UMA가 떠 있으면 여기서 중단돼. 그 프로세스를 임의로 죽이지 말고 상태를 먼저 확인해.

## 3. pilot만 실행

```bash
mkdir -p "$OUT/logs"
nohup ./run.sh pilot > "$OUT/logs/pilot.log" 2>&1 &
echo $! > "$OUT/pilot.pid"
echo "pilot PID $(cat "$OUT/pilot.pid")"
```

상태 확인:

```bash
watch -n 5 ./watch.sh
```

pilot이 끝나면 다음을 보내줘.

```bash
cat "$OUT/logs/pilot.log"
cat "$OUT/uma-s-1p1_oc20/PILOT.json"
```

## 4. pilot 검토 뒤 전체 screen

pilot을 먼저 같이 보고 진행해. 통과하면:

```bash
nohup ./run.sh screen > "$OUT/logs/screen.log" 2>&1 &
echo $! > "$OUT/screen.pid"
echo "screen PID $(cat "$OUT/screen.pid")"
```

중단돼도 같은 명령을 다시 실행하면 완료 record를 건너뛰고 이어가.

## 5. 결과 묶기

먼저 UMA 결과에서 VASP pilot 입력을 만들어.

```bash
cd "$APP"
./run.sh vasp-pilot
VASP_PILOT="$OUT/vasp_pilot"
VASP_PILOT_TAR="$(dirname "$OUT")/$(basename "$OUT")_vasp_pilot_inputs.tar.gz"
tar -C "$OUT" -czf "$VASP_PILOT_TAR" vasp_pilot
sha256sum "$VASP_PILOT_TAR"
```

pilot VASP 결과를 검토한 뒤 전체 후보 입력은 다음으로 만들어.

```bash
cd "$APP"
./run.sh vasp-all
VASP_ALL="$OUT/vasp_all"
VASP_ALL_TAR="$(dirname "$OUT")/$(basename "$OUT")_vasp_all_inputs.tar.gz"
tar -C "$OUT" -czf "$VASP_ALL_TAR" vasp_all
sha256sum "$VASP_ALL_TAR"
```

각 생성 폴더의 `VASP_README_KO.md`와 `vasp_vendor.conf.example`을 외주처에 같이
보내. POTCAR는 라이선스 때문에 들어 있지 않고, 외주처가 자기 라이브러리에서 조립해.

UMA 원자료 자체를 묶는 명령은 아래와 같아.

POTCAR 같은 라이선스 파일은 이 계산에 없지만, 산출물을 통째로 회수하기 쉽게 묶어.

```bash
cd "$(dirname "$OUT")"
RESULTS_TAR="$(basename "$OUT")_results.tar.gz"
tar -czf "$RESULTS_TAR" "$(basename "$OUT")"
sha256sum "$RESULTS_TAR"
```
