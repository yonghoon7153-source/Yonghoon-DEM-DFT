# Yonghoon Battery Lab Workbench
#
# `make sync` before you start, `make check` before you commit.

SHELL := /bin/bash
PY ?= python3
VENV := .venv
VENV_PY := $(VENV)/bin/python
WEB := apps/web

.DEFAULT_GOAL := help
.PHONY: help setup setup-git sync venv install-api install-web dev api web \
        test test-py test-web lint lint-py lint-web check wiki-lint wiki-status \
        clean fmt

help: ## 사용 가능한 타겟
	@grep -hE '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	  | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

setup: setup-git venv install-api install-web ## 클론 직후 1회
	@echo "준비 완료. 'make dev' 로 실행하세요."

setup-git: ## 공용 브랜치용 git 설정 (rebase + autostash)
	git config pull.rebase true
	git config rebase.autoStash true
	git config push.default current
	git config merge.ours.driver true
	@echo "git: pull.rebase=true rebase.autoStash=true"

sync: ## 세션 시작 — 안전하게 최신 상태로 (작업 중 변경은 자동 stash)
	git pull --rebase --autostash

venv:
	@test -d $(VENV) || $(PY) -m venv $(VENV)

install-api: venv ## Python 의존성 설치
	$(VENV_PY) -m pip install --upgrade pip --quiet
	$(VENV_PY) -m pip install -e packages/wrdkit[dev] --quiet
	$(VENV_PY) -m pip install -r apps/api/requirements.txt --quiet

install-web: ## 프론트엔드 의존성 설치
	cd $(WEB) && npm install

dev: ## API(8000) + web(5173) 동시 실행
	@trap 'kill 0' EXIT; \
	$(MAKE) api & \
	$(MAKE) web & \
	wait

api: ## FastAPI 개발 서버
	$(VENV_PY) -m uvicorn app.main:app --reload --port 8000 --app-dir apps/api

web: ## Vite 개발 서버
	cd $(WEB) && npm run dev

test: test-py test-web ## 전체 테스트

test-py: ## pytest (wrdkit + api)
	$(VENV_PY) -m pytest packages/wrdkit/tests apps/api/tests -q

test-web: ## vitest + 타입 체크
	cd $(WEB) && npm run typecheck && npm run test -- --run

lint: lint-py lint-web wiki-lint ## 전체 린트

lint-py:
	$(VENV_PY) -m ruff check packages apps/api || true

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
