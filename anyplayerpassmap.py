import pandas as pd
from statsbombpy import sb
from mplsoccer import Pitch
import matplotlib.pyplot as plt


def find_match_id(home_team, away_team):
    # Fetch the data using statsbombpy
    data = sb.matches(competition_id=43, season_id=106)

    # Filter the data to find the matching match
    match = data[(data['home_team'] == home_team) &
                 (data['away_team'] == away_team)]

    if len(match) == 0:
        print("No match found for the given home and away teams.")
        return None
    elif len(match) > 1:
        print("Multiple matches found for the given home and away teams.")
        return None
    else:
        match_id = match['match_id'].values[0]
        return match_id


sb.competitions()
home = "Portugal"  # Change later to input
away = "Ghana"  # Change later to input
match_id = find_match_id(home, away)
print(match_id)

match_event_df = sb.events(match_id=match_id)
match_360_df = pd.read_json(
    r'C:\Users\amete\OneDrive\Documents\GitHub\open-data\data\three-sixty\{}.json'.format(match_id))
match_event_df['id']
match_360_df['event_uuid']

df = pd.merge(left=match_event_df, right=match_360_df,
              left_on='id', right_on='event_uuid', how='left')

player_info_df = df[['player_id', 'player']
                    ].drop_duplicates().reset_index(drop=True)
player_name = "Cristiano Ronaldo dos Santos Aveiro"
player_df = match_event_df[match_event_df['player'] == player_name]
player_id = player_df['player_id'].values[0]
print(player_id)
