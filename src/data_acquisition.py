import logging
from datetime import datetime

import requests

from . import models

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FPL_BASE_URL = "https://fantasy.premierleague.com/api"


def fetch_fpl_data():
    try:
        # Example endpoints - adjust as needed
        players_response = requests.get(f"{FPL_BASE_URL}/bootstrap-static/")
        players_response.raise_for_status()
        return players_response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching FPL data: {e}")
        raise


def safe_float(value, default=0.0):
    if value is None:
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def parse_and_store_data(data, db_session):
    try:
        # Clear existing data
        db_session.query(models.Player).delete()
        db_session.query(models.Team).delete()

        # Process player data
        for player_data in data.get("elements", []):
            player = models.Player(
                id=player_data.get("id"),
                name=player_data.get("web_name"),
                team=player_data.get("team"),
                position=player_data.get("element_type"),
                points=player_data.get("total_points"),
                form=safe_float(player_data.get("form")),
            )
            db_session.add(player)

        # Process team data
        for team_data in data.get("teams", []):
            team = models.Team(
                id=team_data.get("id"),
                name=team_data.get("name"),
                points=team_data.get("points"),
                form=safe_float(team_data.get("form")),
            )
            db_session.add(team)

        db_session.commit()
        return True
    except Exception as e:
        db_session.rollback()
        logger.error(f"Error storing data: {e}")
        raise


def fetch_and_store_data():
    db_session = models.init_db()
    try:
        data = fetch_fpl_data()
        success = parse_and_store_data(data, db_session)
        return success
    finally:
        db_session.close()
