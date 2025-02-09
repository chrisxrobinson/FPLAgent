.PHONY: build up down fastapi streamlit test

build:
	# Build all services
	docker-compose build

up:
	# Start all services
	docker-compose up

down:
	# Stop and remove containers
	docker-compose down

fastapi:
	# Run the FastAPI service
	docker-compose run fastapi

streamlit:
	# Run the Streamlit service
	docker-compose run streamlit

test:
	# Run tests
	poetry run pytest
