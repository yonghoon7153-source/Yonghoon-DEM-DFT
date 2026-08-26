# Yonghoon Battery Lab Workbench
#
# `make sync` before you start, `make check` before you commit.

SHELL := /bin/bash
PY ?= python3
VENV := .venv
VENV_PY := $(VENV)/bin/python
WEB := apps/web

# The one address to remember: http://localhost:5003
# `make serve` listens here directly; `make dev` puts Vite here and proxies
# /api to PORT_API behind it.
PORT ?= 5003
PORT_API ?= 8000

.DEFAULT_GOAL := help
.PHONY: help setup setup-git sync venv install-api install-web install-bml \
        dev serve api web build test test-py test-web test-tools \
        lint lint-py lint-web check wiki-lint wiki-status clean fmt doctor feed

help: ## 사용 가능한 타겟
	@grep -hE '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	  | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

# install-bml 이 여기 없어서, make setup 을 끝까지 한 사람이 다음 줄에서
# `bml: command not found` 를 봤다.  설치 절차에 없는 한 단계는 반드시 빠진다.
setup: setup-git venv install-api install-web install-bml ## 클론 직후 1회
	@echo "준비 완료. 'bml' 로 실행하세요 (새 터미널이거나, 위가 알려 준 export 한 줄 뒤)."

setup-git: ## 공용 브랜치용 git 설정 (rebase + autostash + 커밋 기록 훅)
	git config pull.rebase true
	git config rebase.autoStash true
	git config push.default current
	git config merge.ours.driver true
	git config core.hooksPath .githooks
	@echo "git: pull.rebase=true rebase.autoStash=true hooksPath=.githooks"

sync: ## 세션 시작 — 안전하게 최신 상태로 (작업 중 변경은 자동 stash)
	git pull --rebase --autostash

venv:
	@test -d $(VENV) || $(PY) -m venv $(VENV)

install-api: venv ## Python 의존성 설치
	$(VENV_PY) -m pip install --upgrade pip --quiet
	$(VENV_PY) -m pip install -e packages/wrdkit[dev] --quiet
	$(VENV_PY) -m pip install -r apps/api/requirements-dev.txt --quiet

install-web: ## 프론트엔드 의존성 설치
	cd $(WEB) && npm install

install-bml: ## `bml` 명령을 PATH 에 등록 (1회)
	./tools/bml install

doctor: ## 환경 점검 (WSL 포함)
	./tools/bml doctor

dev: ## 개발 서버 — http://localhost:5003 (핫 리로드)
	@echo "→ http://localhost:$(PORT)"
	@trap 'kill 0' EXIT; \
	$(MAKE) api & \
	$(MAKE) web & \
	wait

serve: build ## 한 포트로 실행 — http://localhost:5003 (node 불필요)
	@echo "→ http://localhost:$(PORT)"
	WORKBENCH_PORT=$(PORT) $(VENV_PY) -m uvicorn app.main:app \
	  --host 127.0.0.1 --port $(PORT) --app-dir apps/api \
	  --timeout-graceful-shutdown 3

build: ## 프론트엔드 프로덕션 빌드 (apps/web/dist)
	cd $(WEB) && npm run build

api: ## FastAPI 개발 서버 (Vite 프록시 뒤)
	$(VENV_PY) -m uvicorn app.main:app --reload --port $(PORT_API) --app-dir apps/api

web: ## Vite 개발 서버
	cd $(WEB) && WORKBENCH_PORT=$(PORT) WORKBENCH_API_PORT=$(PORT_API) npm run dev

test: test-py test-web test-tools ## 전체 테스트

test-py: ## pytest (wrdkit + api)
	$(VENV_PY) -m pytest packages/wrdkit/tests apps/api/tests -q

test-web: ## vitest + 타입 체크
	cd $(WEB) && npm run typecheck && npm run test -- --run

test-tools: ## tools/ 회귀 테스트 (포트 소유 판정, lint 게이트, docs lint, 백업)
	bash tools/tests/test_bml_ownership.sh
	bash tools/tests/test_lint_gate.sh
	bash tools/tests/test_bml_shutdown.sh
	bash tools/tests/test_bml_client.sh
	bash tools/tests/test_bml_tunnel.sh
	bash tools/tests/test_worklog.sh
	bash tools/tests/test_bml_install.sh
	bash tools/tests/test_bml_data.sh
	bash tools/tests/test_data_untracked.sh
	$(PY) tools/tests/test_wiki_lint.py
	$(PY) tools/tests/test_backup.py

feed: ## 이 브랜치에서 무슨 일이 있었나 (커밋 <-> docs/log.md)
	@bash tools/bml feed

lint: lint-py lint-web wiki-lint ## 전체 린트

# `|| true` 를 붙이지 않는다. `bml check` 와 CI 는 같은 검사를 하드 실패로 돌리므로,
# 여기서 삼키면 `make check` 만 통과하고 push 후 CI 가 빨간불이 된다 — 공용 브랜치라
# 상대가 그 CI 를 물려받는다. (`fmt` 의 `|| true` 는 검증 경로가 아니라 의도된 것)
lint-py:
	$(VENV_PY) -m ruff check packages apps/api

lint-web:
	cd $(WEB) && npm run lint

check: test lint ## 커밋 전 필수
	@echo "check 통과."

wiki-lint: ## docs/ 위키 정합성 + CLAUDE/AGENTS parity
	$(PY) tools/wiki_lint.py

wiki-status: ## docs/ 스냅샷
	$(PY) tools/wiki_status.py

fmt:
	$(VENV_PY) -m ruff format packages apps/api || true
	cd $(WEB) && npm run format

clean:
	rm -rf $(VENV) $(WEB)/node_modules $(WEB)/dist
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
