"""Render schedule definitions for crontab / Hermes cron / launchd / systemd from config/agent.yaml."""
from __future__ import annotations

from .config import Config


def render(cfg: Config, target: str) -> str:
    root = cfg.root
    tz = cfg.timezone
    noon = cfg.get("schedule.noon", {})
    morn = cfg.get("schedule.morning", {})
    if target == "crontab":
        return "\n".join([
            f"# research-agent — `crontab -e` 에 추가 (CRON_TZ는 cronie/Vixie cron 지원; 아니면 서버 TZ를 {tz}로)",
            f"CRON_TZ={tz}",
            f"RA_ROOT={root}",
            f"RA_ENV_FILE=$HOME/.hermes/.env",
            f"{noon.get('cron', '0 12 * * *')}  cd {root} && {noon.get('job', 'ra noon')}    >> {root}/data/logs/noon.log 2>&1",
            f"{morn.get('cron', '0 9 * * *')}  cd {root} && {morn.get('job', 'ra morning')} >> {root}/data/logs/morning.log 2>&1",
            "",
        ])
    if target == "hermes":
        return "\n".join([
            "# Hermes Agent cron — 스킬이 절차를 수행하고 결과를 이메일로 전달",
            f"hermes cron create \"{noon.get('cron', '0 12 * * *')}\" \"paper-agent 스킬의 NOON 절차를 수행하라 (repo: {root}). 완료 후 요약을 [SILENT] 없이 보고.\" --skill paper-agent --name ra-noon --workdir {root}",
            f"hermes cron create \"{morn.get('cron', '0 9 * * *')}\" \"paper-agent 스킬의 MORNING 절차를 수행하고 디제스트 본문을 그대로 전달하라 (repo: {root}).\" --skill paper-agent --name ra-morning --workdir {root} --deliver email",
            "# 확인: hermes cron list / 즉시 실행: hermes cron run ra-noon",
            "",
        ])
    if target == "launchd":
        return _launchd(root, tz, noon, morn)
    if target == "systemd":
        return _systemd(root, noon, morn)
    raise ValueError(target)


def _launchd(root, tz, noon, morn) -> str:
    def plist(name, cron, job):
        m, h = cron.split()[:2]
        return f"""<!-- ~/Library/LaunchAgents/com.research-agent.{name}.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>com.research-agent.{name}</string>
  <key>ProgramArguments</key><array><string>/bin/bash</string><string>-lc</string><string>cd {root} && {job}</string></array>
  <key>EnvironmentVariables</key><dict><key>TZ</key><string>{tz}</string><key>RA_ROOT</key><string>{root}</string></dict>
  <key>StartCalendarInterval</key><dict><key>Hour</key><integer>{int(h)}</integer><key>Minute</key><integer>{int(m)}</integer></dict>
  <key>StandardOutPath</key><string>{root}/data/logs/{name}.log</string>
  <key>StandardErrorPath</key><string>{root}/data/logs/{name}.err</string>
</dict></plist>
"""
    return plist("noon", noon.get("cron", "0 12 * * *"), noon.get("job", "ra noon")) + "\n" + plist("morning", morn.get("cron", "0 9 * * *"), morn.get("job", "ra morning"))


def _systemd(root, noon, morn) -> str:
    def unit(name, cron, job):
        m, h = cron.split()[:2]
        return f"""# ~/.config/systemd/user/ra-{name}.service
[Unit]
Description=research-agent {name}
[Service]
Type=oneshot
WorkingDirectory={root}
Environment=RA_ROOT={root}
ExecStart=/bin/bash -lc '{job}'

# ~/.config/systemd/user/ra-{name}.timer
[Unit]
Description=research-agent {name} timer
[Timer]
OnCalendar=*-*-* {int(h):02d}:{int(m):02d}:00
Persistent=true
[Install]
WantedBy=timers.target
# systemctl --user enable --now ra-{name}.timer
"""
    return unit("noon", noon.get("cron", "0 12 * * *"), noon.get("job", "ra noon")) + "\n" + unit("morning", morn.get("cron", "0 9 * * *"), morn.get("job", "ra morning"))
