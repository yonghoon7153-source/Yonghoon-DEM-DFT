# にほんちず — 일본 지도 노트
#
# `make sync` 로 시작하고, `make check` 뒤에 커밋한다. 평소 실행은 `nihon` 한 줄.

SHELL := /bin/bash
PORT ?= 5004

.DEFAULT_GOAL := help
.PHONY: help setup setup-git install install-nihon sync dev build preview check geo feed shots clean

help: ## 사용 가능한 타겟
	@grep -hE '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	  | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

setup: setup-git install install-nihon ## 클론 직후 1회
	@echo "준비 완료. 'nihon' 으로 실행하세요."

setup-git: ## 공용 브랜치용 git 설정 (rebase + autostash + 커밋 기록 훅)
	git config pull.rebase true
	git config rebase.autoStash true
	git config push.default current
	git config core.hooksPath .githooks
	@echo "git: pull.rebase=true rebase.autoStash=true hooksPath=.githooks"

install: ## 의존성 설치
	npm ci --no-audit --no-fund

install-nihon: ## `nihon` 명령을 PATH 에 등록 (1회)
	./tools/nihon install

sync: ## 세션 시작 — 안전하게 최신 상태로 (작업 중 변경은 자동 stash)
	git pull --rebase --autostash

dev: ## 개발 서버 — http://localhost:5004
	npx vite --port $(PORT) --strictPort --host

build: ## 빌드 → dist/ (데이터 검증 포함)
	npm run build

preview: ## 빌드 결과 미리보기 — http://localhost:5004
	npx vite preview --port $(PORT) --strictPort --host

check: ## 커밋 전 검사 (데이터 · 타입 · 빌드)
	npm run data:check
	npm run typecheck
	npm run build

geo: ## 지도 데이터 재생성
	node scripts/build-geo.mjs

feed: ## 커밋 ↔ docs/log.md 짝 맞추기
	./tools/nihon feed

shots: ## 스크린샷 QA (Playwright 필요)
	node tools/shots.mjs

clean: ## 빌드 산출물 제거
	rm -rf dist
