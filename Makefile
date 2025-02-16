.PHONY: build up down fastapi streamlit test db-shell db-backup db-restore db-query db-stats docker-clean docker-image-prune lint fmt check

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

db-shell:
	# Open local SQLite shell for the database
	sqlite3 ./data/fplagent.db

db-backup:
	# Backup the database locally
	sqlite3 ./data/fplagent.db ".backup './data/fplagent_backup.db'"

db-restore:
	# Restore from local backup
	sqlite3 ./data/fplagent.db ".restore './data/fplagent_backup.db'"

db-query:
	# Run common queries (example: make db-query QUERY="SELECT * FROM players LIMIT 5;")
	sqlite3 -header -column ./data/fplagent.db "$(QUERY)"

db-stats:
	# Show database statistics and table info
	sqlite3 ./data/fplagent.db ".tables; SELECT COUNT(*) as player_count FROM players; SELECT COUNT(*) as team_count FROM teams;"

docker-clean:
	# Remove unused containers, networks, images and build cache
	docker system prune -f

docker-image-prune:
	# Remove dangling images only
	docker image prune -f

lint:
	# Run all linting checks
	poetry run flake8 src tests
	poetry run black --check src tests
	poetry run isort --check-only src tests

fmt:
	# Format all code
	poetry run black src tests
	poetry run isort src tests

check:
	# Run all checks (linting and tests)
	make lint
	make test