import pandas as pd
from statsbombpy import sb
from mplsoccer import Pitch, VerticalPitch
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
from scipy.ndimage import gaussian_filter


match_event_df = sb.events(match_id=3857256)
data1 = (match_event_df)
data1 = data1[(data1['player'] == player) & (
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
df = passing
customcmap = matplotlib.colors.LinearSegmentedColormap.from_list('custom cmap', [
    'black', 'red'])
""" p = Pitch(pitch_type='statsbomb', pitch_color='black',
          line_color='white', line_zorder=2)
fig, ax = p.draw(figsize=(12, 8))
p.kdeplot(df['x_start'], df['y_start'], ax=ax,
          cmap=customcmap, shade=True, n_levels=100, zorder=1)
"""
pitch = Pitch(pitch_type='statsbomb', line_zorder=2,
              pitch_color='#22312b', line_color='white') 

fig, ax = pitch.draw(figsize=(16, 9))
bin_statistic = pitch.bin_statistic(
    passing.x_start, passing.y_start, statistic='count', bins=(25, 25))
bin_statistic['statistic'] = gaussian_filter(bin_statistic['statistic'], 1)
pcm = pitch.heatmap(bin_statistic, ax=ax, cmap='hot', edgecolors='#22312b')
cbar = fig.colorbar(pcm, ax=ax)

plt.show()
