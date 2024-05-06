OS := $(shell uname -s)

# Set path separator and commands based on the OS
ifeq ($(OS),Windows_NT)
    SEP := \\
    PY := python
else
    SEP := /
    PY := python3
endif

# Run the streamlit application locally
run_app_local:
	$(PY) -m streamlit run app$(SEP)main.py --server.port 8500

# Run the streamlit application using poetry
run_app_poetry:
	poetry run streamlit run app$(SEP)main.py --server.port 8503

# Run the streamlit application using docker
run_app_docker:
	docker compose -f "docker-compose.yml" down
	docker compose -f "docker-compose.yml" up -d --build

# Reload the requirements then output in the .devcontainer directory
reload_reqs:
	poetry export -f requirements.txt --output .$(SEP).devcontainer$(SEP)requirements.txt --without-hashes
