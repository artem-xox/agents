install:
	poetry install --no-root

ui:
	PYTHONPATH=${PWD} poetry run streamlit run src/ui/main.py

test:
	poetry run pytest ./

lint:
	poetry run ruff check .
	poetry run isort .
