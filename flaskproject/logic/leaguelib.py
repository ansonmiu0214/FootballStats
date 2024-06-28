"""Dealing with getting league reference data."""

# built-ins
import http.client
import json
import urllib.parse
from typing import Any


_SEASON = 2023
_API_HOST = 'v3.football.api-sports.io'
_API_HEADERS = {
    'x-rapidapi-key': '46e3603952bbef534e2356d69f0a1ed6',   # TODO: remove!
    'x-rapidapi-host': _API_HOST,
    'season': _SEASON,
}


def _get_connection():
    return http.client.HTTPSConnection(_API_HOST)


def get_team(name: str) -> dict:
    url = urllib.parse.quote(f'/teams?name={name}', safe='/?=')
    
    conn = _get_connection()
    conn.request('GET', url, headers=_API_HEADERS)
    res = conn.getresponse()
    raw_data = res.read()

    data = json.loads(raw_data.decode('utf-8'))
    response = data['response']
    assert type(response) is list
    assert len(response) == 1
    return response[0]


def get_teams_for_league(id: Any) -> list[dict]:
    url = urllib.quote(f'/teams?league={id}&season={_SEASON}')
    
    conn = _get_connection()
    conn.request('GET', url, headers=_API_HEADERS)
    res = conn.getresponse()
    raw_data = res.read()

    data = json.loads(raw_data.decode('utf-8'))
    response = data['response']
    assert type(response) is list

    return response


def get_players_for_team(id: Any) -> list[dict]:
    url = urllib.quote(f'/players/squads?team={id}')
    
    conn = _get_connection()
    conn.request('GET', url, headers=_API_HEADERS)
    res = conn.getresponse()
    raw_data = res.read()

    data = json.loads(raw_data.decode('utf-8'))
    response = data['response']
    assert type(response) is list
    assert len(response) == 1

    team = response[0]
    players = team['players']
    return players