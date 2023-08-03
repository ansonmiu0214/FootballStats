import pandas as pd
from statsbombpy import sb
from mplsoccer import Pitch, VerticalPitch
import matplotlib.pyplot as plt


def tocsv(name, df):
    csv_file_name = f"{name}.csv"
    df.to_csv(csv_file_name)

    print(f"Data exported to '{csv_file_name}' successfully.")


sb.competitions()

(sb.matches(competition_id=43, season_id=106))

MATCH_ID = 3869685
PLAYER_ID = 5503
match_event_df = sb.events(match_id=MATCH_ID)

data1 = (match_event_df)

data1 = data1[(data1['type'] == 'Pass')].reset_index(drop=True)

starter_id = []

for x in range(2):
    for y in range(11):
        player_id = match_event_df['tactics'][x]['lineup'][y]['player']['id']
        starter_id.append(player_id)

# Seperates locations[x,y] and pass_end_location[x,y] into x_start,y_start,x_end,y_end
data1[['x_start', 'y_start']] = pd.DataFrame(
    data1.location.tolist(), index=data1.index)
data1[['x_end', 'y_end']] = pd.DataFrame(
    data1.pass_end_location.tolist(), index=data1.index)
passing = data1[data1['player_id'].isin(starter_id)][['player', 'player_id', 'team', 'pass_recipient',
                                                      'x_start', 'y_start', 'x_end', 'y_end', 'pass_outcome']]
# Variable will be used
passing = passing[passing['team'] == "France"]
passing['pass_outcome'].fillna("Complete", inplace=True)
passing = passing[passing['pass_outcome'] == 'Complete']
average_location = passing.groupby('player').agg(
    {'x_start': ['mean'], 'y_start': ['mean', 'count']})
average_location.columns = ['x_start', 'y_start', 'count']

pass_between = passing.groupby(
    ['player', 'pass_recipient']).player_id.count().reset_index()
pass_between.rename({'player_id': 'pass_count'}, axis='columns', inplace=True)
pass_between = pass_between.merge(
    average_location, left_on='player', right_index=True)
pass_between = pass_between.merge(
    average_location, left_on='pass_recipient', right_index=True)
pass_between = pass_between[pass_between['pass_count'] > 3]


p = VerticalPitch(pitch_color='grass', line_color='white', pitch_type='statsbomb',
                  stripe=True)
fig, ax = p.draw(figsize=(12, 8))
arrows = p.arrows(pass_between.x_start_x, pass_between.y_start_x,
                  pass_between.x_start_y, pass_between.y_start_y, ax=ax, width=3, headwidth=3, color='red')
nodes = p.scatter(average_location.x_start, average_location.y_start, s=300,
                  color='#d3d3d3', edgecolors='black', linewidth=2.5, alpha=1, zorder=1, ax=ax)
text_offset = 3  # You can increase or decrease this value to adjust the vertical offset
for i, player_name in enumerate(average_location.index):
    ax.annotate(player_name, (average_location.y_start[i], average_location.x_start[i] - text_offset),
                ha='center', va='top', fontsize=5, color='black', weight='bold')
plt.show()
