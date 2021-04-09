XCHANGE_VERSION := 1.1.1
XCHANGE_PATH := ./xchange/xchange-v$(XCHANGE_VERSION)

$(XCHANGE_PATH)/venv:
	cd '$(XCHANGE_PATH)' && python setup_xchange.py

.PHONY: xchange-linux-case%
xchange-linux-case%: $(XCHANGE_PATH)/venv
	cd '$(XCHANGE_PATH)' && ./xchange-linux 'case$*'

.PHONY: case%
case%:
	poetry run python 'case$*.py'
