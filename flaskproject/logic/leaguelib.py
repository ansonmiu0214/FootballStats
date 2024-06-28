"""Dealing with getting league reference data."""

# built-ins
import http.client
import json
import urllib.parse
from typing import Any


_SEASON = 2023


class LeagueAPI:
    def __init__(self):
        self._conn = None
        self._host = 'v3.football.api-sports.io'
        self._headers = {
            'x-rapidapi-key': '46e3603952bbef534e2356d69f0a1ed6',   # TODO: remove!
            'x-rapidapi-host': self._host,
            'season': _SEASON,
        }

    def __enter__(self):
        self._conn = http.client.HTTPSConnection(self._host)
        return self

    def get(self, url: str):
        """Fetch the specified 'url' and return the parsed JSON response."""

        assert self._conn is not None

        safe_url = urllib.parse.quote(url, safe='/?=')
        self._conn.request('GET', safe_url, headers=self._headers)
        res = self._conn.getresponse()
        raw_data = res.read()

        data = json.loads(raw_data.decode('utf-8'))
        response = data['response']
        return response

    def __exit__(self):
        self._conn = self._conn.close()


def get_team(name: str) -> dict:
    with LeagueAPI() as api:
        response = api.get(f'/teams?name={name}')
    
    assert type(response) is list
    assert len(response) == 1
    return response[0]


def get_teams_for_league(id: Any) -> list[dict]:
    with LeagueAPI() as api:
        response = api.get(f'/teams?league={id}&season={_SEASON}')
    
    assert type(response) is list
    return response


def get_players_for_team(id: Any) -> list[dict]:
    with LeagueAPI() as api:
        response = api.get(f'/players/squads?team={id}')
    
    assert type(response) is list
    assert len(response) == 1

    team = response[0]
    players = team['players']
    return players