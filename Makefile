.PHONY: lint
lint:
	python -m mypy --version
	python -m mypy ./talk_to_me/

.PHONY: black
black:
	python -m black --version
	python -m black ./talk_to_me/

.PHONY:	isort
isort:
	python -m isort --version
	python -m isort --profile black .
