---
title: SETUP — Hermes Agent (로컬 상주 자동화)
tags: [research-agent, setup, hermes]
---

# Hermes Agent로 자동화하기

Hermes Agent(NousResearch, 오픈소스)는 상주 게이트웨이·cron·스킬·메모리를 갖춘 개인 에이전트다. 이 repo의 `hermes/skills/research/paper-agent/`가 그 스킬이고, `ra` CLI가 배관이다.

## 1. 설치
```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
source ~/.bashrc
hermes            # 최초 실행 → hermes setup (모델/제공자 선택: Anthropic API 키 또는 Nous Portal)
hermes model      # Claude 계열 모델 선택 권장 (분석 품질)
```
요구: Python 3.11+, Linux/macOS/WSL2. 항상 켜져 있는 머신(연구실 PC, HIT 서버 등)에 두는 것이 좋다.

## 2. 자격증명 (`~/.hermes/.env`) — 이메일 게이트웨이와 공유
```
EMAIL_ADDRESS=yonghoon71@hanyang.ac.kr
EMAIL_PASSWORD=<Gmail 앱 비밀번호 16자리>
EMAIL_IMAP_HOST=imap.gmail.com
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_HOME_ADDRESS=yonghoon71@hanyang.ac.kr     # cron --deliver email 대상
```
`ra`도 같은 파일을 읽는다: `export RA_ENV_FILE=~/.hermes/.env` (셸 rc에 추가).

> [!warning] Scholar alert 발신자는 `noreply`라서 Hermes 이메일 게이트웨이가 무시한다. alert는 `ra`의 IMAP 스캔이 가져온다. 게이트웨이는 **디제스트 발송·사용자 대화**용이다.

## 3. 스킬 등록
```bash
cd <repo>/research-agent
pip install -e ".[llm]"
mkdir -p ~/.hermes/skills/research
ln -sfn "$PWD/hermes/skills/research/paper-agent" ~/.hermes/skills/research/paper-agent
hermes skills list | grep paper-agent
```
`config/agent.yaml`은 기본 `llm.backend: hermes` — 스크립트는 큐만 만들고 Hermes가 스킬 절차대로 큐를 채운다.

## 4. cron 등록
```bash
ra schedule --target hermes     # 아래 두 줄을 출력 — 그대로 실행
hermes cron create "0 12 * * *" "paper-agent 스킬의 NOON 절차를 수행하라 (repo: <repo>). 완료 후 요약을 보고." --skill paper-agent --name ra-noon --workdir <repo>
hermes cron create "0 9 * * *"  "paper-agent 스킬의 MORNING 절차를 수행하고 디제스트 본문을 그대로 전달하라 (repo: <repo>)." --skill paper-agent --name ra-morning --workdir <repo> --deliver email
hermes gateway install          # 상주 서비스 (60초 tick)
hermes cron list && hermes cron run ra-noon
```
- 시간대는 머신 TZ(Asia/Seoul). jobs는 `~/.hermes/cron/jobs.json`, 출력은 `~/.hermes/cron/output/`.
- 디제스트 메일은 (a) `mail.backend: smtp`면 `ra morning`이 직접 보내고, (b) `mail.backend: hermes`면 cron의 `--deliver email`이 Hermes 응답을 보낸다. 둘 다 켜지 않도록 하나만 고른다(기본 smtp).

## 5. Cowork와의 관계
- Cowork 클라우드 작업이 먼저 처리한 논문은 `[RA-HANDOFF]` 메일로 온다 → NOON 절차 1단계 `ra noon`이 자동 병합.
- Hermes가 먼저 처리한 논문은 vault/DB에 있으므로 Cowork는 (데스크톱 링크 시) 그것을 읽고 중복 분석을 피한다.
- 둘 다 없는 시간대(컴퓨터 꺼짐 + 클라우드 작업 실패)에는 메일이 쌓였다가 다음 실행에 처리된다. 데이터는 유실되지 않는다.

## 6. 스킬 자가 개선
Hermes는 작업 후 스킬을 스스로 고칠 수 있다(`skill_manage`). `skills.write_approval: true`로 두면 변경이 `~/.hermes/pending/skills/`에 쌓이고 `/skills approve <id>`로 승인한다. 승인된 변경은 repo의 `hermes/skills/...`에도 반영해 커밋한다(symlink라 자동).

## 7. 문제 해결
| 증상 | 확인 |
|---|---|
| cron이 안 돎 | `hermes cron status`, `hermes gateway` 포그라운드 실행 로그 |
| alert 0건 | Scholar alert가 yonghoon71@hanyang.ac.kr로 오는지, IMAP 활성화, `lookback_days` |
| 큐가 안 비워짐 | `ra analyze --import-dir data/analysis/pending` 검증 오류 메시지(필수 키) |
| 메일 미발송 | `.env`의 앱 비밀번호, 587 STARTTLS 차단 여부, `data/logs/morning.log` |
