SHELL := /bin/bash

SRC_DIR := .
VENV := .venv
PYTHON := $(VENV)/Scripts/python.exe
PIP := $(VENV)/Scripts/pip.exe
RUFF := $(VENV)/Scripts/ruff.exe
PYRIGHT := $(VENV)/Scripts/pyright.exe
PRECOMMIT := $(VENV)/Scripts/pre-commit.exe

.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| sort \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: venv
venv: ## Создать виртуальное окружение
	python -m venv $(VENV)

.PHONY: install
install: venv ## Установить зависимости
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

.PHONY: run
run: ## Запустить приложение
	$(PYTHON) task1.py --input_file input.txt --key key.xlsx --output_file output.txt

.PHONY: clean
clean: ## Очистить кэши
	rm -rf .ruff_cache .mypy_cache build dist *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

.PHONY: lint
lint: ## Запустить линтер (ruff check)
	$(RUFF) check $(SRC_DIR)

.PHONY: lint-fix
lint-fix: ## Линтер с автоисправлением
	$(RUFF) check --fix $(SRC_DIR)

.PHONY: format
format: ## Отформатировать код (ruff format)
	$(RUFF) format $(SRC_DIR)

.PHONY: format-check
format-check: ## Проверить форматирование
	$(RUFF) format --check $(SRC_DIR)

.PHONY: typecheck
typecheck: ## Проверить типы (pyright)
	$(PYRIGHT)

.PHONY: fullcheck
fullcheck: lint format-check typecheck ## Все статические проверки

.PHONY: fix
fix: lint-fix format ## Автоисправление + форматирование

.PHONY: precommit
precommit: ## Установить pre-commit hooks
	$(PRECOMMIT) install --hook-type pre-commit --hook-type pre-push

.PHONY: precommit-run
precommit-run: ## Прогнать все pre-commit хуки вручную
	$(PRECOMMIT) run --all-files
