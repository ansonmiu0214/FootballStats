import pandas as pd
from statsbombpy import sb
from mplsoccer import Pitch
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
match_360_df = pd.read_json(
    r'C:\Users\amete\OneDrive\Documents\GitHub\open-data\data\three-sixty\{}.json'.format(MATCH_ID))
data1 = (match_event_df)
data1 = data1[(data1['team'] == 'France') & (
    data1['type'] == 'Pass')].reset_index(drop=True)
data1[['x_start', 'y_start']] = pd.DataFrame(
    data1.location.tolist(), index=data1.index)
data1[['x_end', 'y_end']] = pd.DataFrame(
    data1.pass_end_location.tolist(), index=data1.index)
passing = data1[['x_start', 'y_start', 'x_end', 'y_end', 'pass_outcome']]

# Populates all the blank field which are supposed "Pass"
for i in range(len(passing)):
    if pd.isnull(passing.loc[i, 'pass_outcome']) and passing.loc[max(0, i - 1), 'pass_outcome'] != '':
        passing.loc[i, 'pass_outcome'] = 'Pass'


# Changing to df just for now
df = passing


p = Pitch(pitch_type='statsbomb')
fig, ax = p.draw(figsize=(12, 8))

pass_outcomes = df['pass_outcome'].unique()

# Define colors for each pass outcome
pass_colors = {'Pass': 'green', 'Incomplete': 'red', 'Pass Offside': 'orange','Out': 'red','Unknown':'red'}

for outcome in pass_outcomes:
    df_subset = df[df['pass_outcome'] == outcome]
    p.scatter(x=df_subset['x_start'], y=df_subset['y_start'],
              color=pass_colors[outcome], ax=ax)
    p.lines(xstart=df_subset['x_start'], ystart=df_subset['y_start'],
            xend=df_subset['x_end'], yend=df_subset['y_end'], color=pass_colors[outcome], ax=ax, comet=True)

plt.show()
