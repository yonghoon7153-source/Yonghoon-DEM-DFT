---
description: 최신성 점검(daily_refresh) 후 낡은 것만 골라 갱신한다 — KST 00시 자동 실행용
---

# /daily — 하루 한 번 최신성 점검·갱신

## 왜 있나

2026-08-25 실측: 대시보드 카드가 08-20 에서 멈춰 있었고, 그중 b2o3 카드는 **이미
뒤집힌 판정**("판정 보류 · 보류 대상 Ea 0.199")을 계속 말하고 있었다. 그 값은 08-23 에
철회됐다. **화면이 낡으면 끝난 논의를 다시 하게 된다.** 낡음은 조용히 진행되므로
사람이 눈치채길 기다리면 안 된다.

## 절차

### 1. 점검부터 — 판단하지 말고 사실만 모은다

```bash
python3 tools/claude/daily_refresh.py --verbose
```

전부 ✅ 면 **아무것도 고치지 말고 한 줄로 보고하고 끝낸다.**
고칠 게 없는데 손대는 것이 이 명령의 가장 흔한 실패 방식이다.

### 2. ⛔ 로 뜬 것만 처리한다

| 점검 | ⛔ 일 때 할 일 |
|---|---|
| `dashboard` | kb 최신 카드를 읽고 **그 판정이 대시보드에 있는지** 본다. 없으면 카드 추가, 이미 있는데 내용이 뒤집혔으면 **문구를 고친다**(지우지 말고 무엇이 바뀌었는지 남긴다). `webapp/data.py: dashboard_highlights()` |
| `canonical` | 레지스트리 값과 원자료가 어긋났다. **원자료가 정본이다** — 왜 바뀌었는지 확인한 뒤 레지스트리를 맞춘다. 철회면 `status: retracted` + `retracted.why` · `usable_instead` 를 반드시 적는다 |
| `governance` | `db/governance/*.json` 그래프가 깨졌다. dangling 참조·어휘 밖 status 를 고친다 |
| `kb-lint` | `python3 tools/kb_wiki.py index` 재생성 후 `lint` 0 errors 까지 |
| `convention` | 물리 규약(MSD 창 2–50 ps, 자유절편 D 등)이 파일 간에 갈라졌다. `tools/convention_check.py` 가 짚는 곳을 맞춘다 |
| `requests` | 요청 대장의 이모지와 문장이 어긋난다. **원문(kb/reports/…)을 고친다** — 화면이 한쪽을 고르면 안 된다 |
| `fairchem` | 번들 sha256 불일치. 누가 손댔거나 파일이 깨졌다. **고치지 말고 사람에게 보고** — 공식 스냅샷을 임의로 수정하면 안 된다 |
| `litdb` | 어느 인덱스에도 없는 digest 가 있다. DFT 축이면 `litdb/INDEX.md`, DEM 축이면 `python3 tools/litdb/build_index.py` 로 `INDEX_DEM.md` 재생성 |
| `git` | 미커밋 변경. 내용을 보고 **의미 있는 커밋 메시지**로 커밋·푸시한다 |

### 3. 고쳤으면 반드시 재검

```bash
python3 tools/claude/daily_refresh.py && python3 -m pytest webapp/tests -q
```

### 4. 커밋

브랜치 `claude/friendly-meitner-lldvar` 에만. 커밋 메시지에 **무엇이 낡아 있었는지**를
적는다 — "갱신" 만 적으면 다음 사람이 왜 바뀌었는지 모른다.

## ⛔ 이 명령이 하면 안 되는 것

- **값을 만들어내지 않는다.** 계산 결과가 없으면 "없다" 고 적는다.
- **서버 계산을 걸지 않는다.** gabia/kgy 는 사람이 판단한다 (`server_status.sh --jobs`).
- **철회된 값을 되살리지 않는다.** 원장에 retracted 면 그대로 둔다.
- **판정을 새로 내리지 않는다.** 낡은 표기를 최신 판정에 맞추는 것까지가 범위다.
  새 판정이 필요하면 그렇게 보고하고 멈춘다.
- 전부 통과면 **아무것도 안 한다.**
