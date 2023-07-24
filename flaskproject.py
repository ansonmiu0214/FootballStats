import pandas as pd
from statsbombpy import sb
from mplsoccer import Pitch
import matplotlib.pyplot as plt
import io
import base64
from flask import Flask, render_template

app = Flask(__name__)


def generate_plot():
    sb.competitions()

    MATCH_ID = 3869685
    match_event_df = sb.events(match_id=MATCH_ID)
    match_360_df = pd.read_json(
        r'C:\Users\amete\OneDrive\Documents\GitHub\open-data\data\three-sixty\{}.json'.format(MATCH_ID))
    match_event_df['id']
    match_360_df['event_uuid']
    df = pd.merge(left=match_event_df, right=match_360_df,
                  left_on='id', right_on='event_uuid', how='left')
    df.head(25)
    MESSI = 5503
    df = df[(df['player_id'] == MESSI) & (
        df['type'] == 'Pass')].reset_index(drop=True)
    df[['x_start', 'y_start']] = pd.DataFrame(
        df.location.tolist(), index=df.index)
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

    # Save the plot to a BytesIO buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convert the plot to a base64 encoded string
    plot_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    return plot_base64


@app.route("/")
def index():
    plot_base64 = generate_plot()
    return render_template('base.html', plot_base64=plot_base64)


if __name__ == "__main__":
    app.run(debug=True)
