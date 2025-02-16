import logging

import pandas as pd

from . import models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_player_data():
    """
    Connects to the database, queries the Player table, and returns a Pandas DataFrame.
    """
    session = models.init_db()
    try:
        players = session.query(models.Player).all()
        data = [
            {
                "id": p.id,
                "name": p.name,
                "team": p.team,
                "position": p.position,
                "points": p.points,
                "form": p.form,
            }
            for p in players
        ]
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        logger.error(f"Error loading player data: {e}")
        raise
    finally:
        session.close()


def compute_player_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes additional metrics such as points per game and adjusted form.
    """
    try:
        if df.empty:
            logger.warning("Player DataFrame is empty.")
            return df

        # Placeholder: assuming each player played 38 games for simplicity.
        df["games_played"] = 38
        df["points_per_game"] = df["points"] / df["games_played"]

        # Placeholder adjustment: multiply form by a factor
        df["adjusted_form"] = df["form"] * 1.1
        return df
    except Exception as e:
        logger.error(f"Error computing player metrics: {e}")
        raise


def analyze_team_performance():
    """
    Queries the Team table, computes summary statistics, and returns the results.
    """
    session = models.init_db()
    try:
        teams = session.query(models.Team).all()
        data = [
            {"id": t.id, "name": t.name, "points": t.points, "form": t.form}
            for t in teams
        ]
        df = pd.DataFrame(data)
        if df.empty:
            logger.info("No team data available.")
            return {}
        analysis = {
            "average_points": df["points"].mean(),
            "average_form": df["form"].mean(),
            "team_count": len(df),
        }
        return analysis
    except Exception as e:
        logger.error(f"Error analyzing team performance: {e}")
        raise
    finally:
        session.close()


# (Optional) Helper function to generate a basic plot of player performance
def plot_player_performance(df: pd.DataFrame):
    """
    Generates a scatter plot of players' points using matplotlib.
    """
    try:
        import matplotlib.pyplot as plt

        if df.empty:
            logger.warning("No data available to plot.")
            return None
        plt.figure(figsize=(10, 6))
        plt.scatter(df["name"], df["points"])
        plt.xticks(rotation=90)
        plt.title("Player Points")
        plt.xlabel("Player")
        plt.ylabel("Points")
        plt.tight_layout()
        return plt
    except Exception as e:
        logger.error(f"Error generating player performance plot: {e}")
        raise
