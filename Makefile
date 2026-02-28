lint:
	yamlfmt -lint .
	mbake format --check Makefile

format:
	yamlfmt .
	mbake format Makefile

.PHONY: lint format