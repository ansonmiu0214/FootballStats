import pandas as pd
from statsbombpy import sb
from mplsoccer import Pitch
import matplotlib.pyplot as plt

print(sb.competitions())

data = (sb.matches(competition_id=2, season_id=27))
MATCH_ID = 3754008
match_event_df = sb.events(match_id=MATCH_ID)


df = pd.DataFrame(match_event_df)

# Export the DataFrame to CSV
csv_file_name = "output6.csv"
df.to_csv(csv_file_name)

print(f"Data exported to '{csv_file_name}' successfully.")
match_360_df = pd.read_json(
    r'C:\Users\amete\OneDrive\Documents\GitHub\open-data\data\three-sixty\{}.json'.format(MATCH_ID))
match_event_df['id']
