import pandas as pd
from statsbombpy import sb
from mplsoccer import Pitch
import matplotlib.pyplot as plt

sb.competitions()
sb.matches(competition_id=43, season_id=106)

MATCH_ID = 3857298
RONALDO = 5207
match_event_df = sb.events(match_id=MATCH_ID)
print(match_event_df['id'])
df = match_event_df
print(df[[]])
