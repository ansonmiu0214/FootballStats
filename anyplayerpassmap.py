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


def find_player_id(df, player_name):
    player_info_df = df[['player_id', 'player']
                        ].drop_duplicates().reset_index(drop=True)
    # print(player_info_df)  # Used to see all the players
    player_df = match_event_df[match_event_df['player'] == player_name]
    player_id = player_df['player_id'].values[0]
    print(player_id)
    player_id = int(player_id)
    return player_id


sb.competitions()
(sb.matches(competition_id=11, season_id=4))

home = input("Home Team:")
away = input("Away Team:")
# home = "Portugal"  # Change later to input
# away = "Ghana"  # Change later to input
MATCH_ID = find_match_id(home, away)
print(MATCH_ID)

match_event_df = sb.events(match_id=MATCH_ID)
match_360_df = pd.read_json(
    r'C:\Users\amete\OneDrive\Documents\GitHub\open-data\data\three-sixty\{}.json'.format(MATCH_ID))
match_event_df['id']
match_360_df['event_uuid']

df = pd.merge(left=match_event_df, right=match_360_df,
              left_on='id', right_on='event_uuid', how='left')


# Showing the name temp
player_info_df = df[['player_id', 'player']
                    ].drop_duplicates().reset_index(drop=True)
print(player_info_df)


player_name = input("Enter a player name:")
PLAYER_ID = find_player_id(df, player_name)
print(PLAYER_ID)
(df.head(25))

df = df[(df['player_id'] == PLAYER_ID) & (
    df['type'] == 'Pass')].reset_index(drop=True)
df[['x_start', 'y_start']] = pd.DataFrame(df.location.tolist(), index=df.index)
df[['x_end', 'y_end']] = pd.DataFrame(
    df.pass_end_location.tolist(), index=df.index)

p = Pitch(pitch_type='statsbomb')
fig, ax = p.draw(figsize=(12, 8))
df = df[:]
p.scatter(x=df['x_start'], y=df['y_start'], ax=ax)
p.lines(xstart=df['x_start'], ystart=df['y_start'],
        xend=df['x_end'], yend=df['y_end'], ax=ax, comet=True)
plt.show()
