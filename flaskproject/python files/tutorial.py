import pandas as pd
from statsbombpy import sb
from mplsoccer import Pitch
import matplotlib.pyplot as plt

sb.competitions()

(sb.matches(competition_id=43, season_id=106))

MATCH_ID = 3869685
match_event_df = sb.events(match_id=MATCH_ID)
match_360_df = pd.read_json(
    r'C:\Users\amete\OneDrive\Documents\GitHub\open-data\data\three-sixty\{}.json'.format(MATCH_ID))
match_event_df['id']
print(match_event_df.columns)
match_360_df['event_uuid']
print(match_event_df.columns)
df = pd.merge(left=match_event_df, right=match_360_df,
              left_on='id', right_on='event_uuid', how='left')
print(df.head(25))
MESSI = 5503
df = df[(df['player_id'] == MESSI) & (
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

for x in df.iloc[0]['freeze_frame']:
    for index, row in df.iterrows():
        minute = row['minute']
        x_mid = (row['x_start'] + row['x_end']) / 2
        y_start = row['y_start']
        ax.text(x_mid, y_start - 1.5,
                f"{minute}'", ha='center', va='center', fontsize=10, color='black')


plt.show()
