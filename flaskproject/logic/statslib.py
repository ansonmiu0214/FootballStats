"""Dealing with getting football stats."""

# built-ins
from typing import Any

# external
import pandas as pd
from statsbombpy import sb


def get_competitions_df() -> pd.DataFrame:
    return sb.competitions(fmt='dataframe')


def get_events_df(*, match_id: Any) -> pd.DataFrame:
    return sb.events(match_id=match_id, fmt='dataframe')


def get_matches_df(*, competition_id: Any, season_id: Any) -> pd.DataFrame:
    return sb.matches(competition_id=competition_id, season_id=season_id, fmt='dataframe')
