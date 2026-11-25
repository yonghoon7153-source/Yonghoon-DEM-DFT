# Hermes cron 등록 (로컬 PC, 항상 켜져 있는 머신)

```bash
# 1) 스킬 설치 (repo → ~/.hermes/skills)
mkdir -p ~/.hermes/skills/research
ln -sfn "$PWD/hermes/skills/research/paper-agent" ~/.hermes/skills/research/paper-agent
hermes skills list | grep paper-agent

# 2) 자격증명 — Hermes 이메일 게이트웨이와 공유
#    ~/.hermes/.env : EMAIL_ADDRESS=yonghoon71@hanyang.ac.kr / EMAIL_PASSWORD=<앱 비밀번호> / EMAIL_IMAP_HOST=imap.gmail.com / EMAIL_SMTP_HOST=smtp.gmail.com / EMAIL_HOME_ADDRESS=yonghoon71@hanyang.ac.kr
export RA_ENV_FILE=~/.hermes/.env

# 3) cron 등록 (ra schedule --target hermes 출력과 동일)
hermes cron create "0 12 * * *" "paper-agent 스킬의 NOON 절차를 수행하라 (repo: $PWD). 완료 후 요약을 보고." --skill paper-agent --name ra-noon --workdir "$PWD"
hermes cron create "0 9 * * *"  "paper-agent 스킬의 MORNING 절차를 수행하고 디제스트 본문을 그대로 전달하라 (repo: $PWD)." --skill paper-agent --name ra-morning --workdir "$PWD" --deliver email

# 4) 게이트웨이 상주 + 확인
hermes gateway install && hermes cron list
hermes cron run ra-noon      # 즉시 테스트
```

- Hermes cron은 `~/.hermes/cron/jobs.json`에 저장되고 60초마다 tick 한다. 시간대는 머신 TZ(Asia/Seoul) 기준.
- Hermes 없이 돌리려면 `ra schedule --target crontab` (또는 launchd/systemd) 출력을 그대로 등록하고 `llm.backend`를 `anthropic` 또는 `claude-cli`로 바꾼다.
