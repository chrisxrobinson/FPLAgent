# FPLAgent

FPLAgent is a Gen AI Agent for Fantasy Premier League.

## Project Overview

This project contains two main components:
- A FastAPI backend (for future enhancements)
- A Streamlit frontend (current UI)

## Installation

Ensure you have Poetry installed. Then run:

```
poetry install
```

Additionally, install SQLite Browser locally if you plan on managing the database:
```
brew install --cask db-browser-for-sqlite
```

## Usage

To run the Streamlit app:
```
poetry run streamlit run src/app.py
```
To run the FastAPI app:
```
poetry run uvicorn src.fastapi_app:app --reload --port 8000
```

### Database Shell & Commands

Because the SQLite database is stored locally in ./data/fplagent.db, you can manage it directly:
- Open a shell:
  ```
  make db-shell
  ```
- Backup the database:
  ```
  make db-backup
  ```
- Restore from backup:
  ```
  make db-restore
  ```
- Execute custom queries:
  ```
  make db-query QUERY="SELECT * FROM players LIMIT 5;"
  ```
- Show database statistics:
  ```
  make db-stats
  ```

## Testing

Run tests with:
```
poetry run pytest
```

## Contribution

Contributions are welcome. Please fork the repository and create a pull request.
