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

## Usage

To run the Streamlit app:
```
poetry run streamlit run src/app.py
```
To run the FastAPI app:
```
poetry run uvicorn src.fastapi_app:app --reload --port 8000
```

## Testing

Run tests with:
```
poetry run pytest
```

## Contribution

Contributions are welcome. Please fork the repository and create a pull request.
