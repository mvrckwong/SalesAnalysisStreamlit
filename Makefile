# Run the streamlit application locally
run_app:
	streamlit run app\main.py

# Run the streamlit application using poetry
run_app_poetry:
	poetry run streamlit run app\main.py

# Run the streamlit application using docker
run_app_docker:
	docker compose -f "docker-compose.yml" down
	docker compose -f "docker-compose.yml" up -d --build

# Reload the requirements then output in the .devcontainer directory
reload_reqs:
	poetry export -f requirements.txt --output .\.devcontainer\requirements.txt --without-hashes