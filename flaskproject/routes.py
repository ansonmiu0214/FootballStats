from positiondict import my_dictionary as dct
from mplsoccer import Pitch, VerticalPitch
from flask import render_template, url_for, flash, redirect, request, jsonify, send_file
from flaskproject import app, db, bcrypt
from flaskproject.forms import RegistrationForm, LoginForm
from flaskproject.models import User, Countries, Competitions, Teams, Comps, TeamsLogo
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import text
import http.client
import json
from statsbombpy import sb
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import seaborn as sns
from scipy.ndimage import gaussian_filter
import matplotlib
connt = http.client.HTTPSConnection("v3.football.api-sports.io")


def heatMapmodel(id,player):
    
    match_event_df = sb.events(match_id=id)
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
    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png', transparent=True)
    img_stream.seek(0)
    return img_stream

def logoChecker(teamName):
    if teamName == 'Leicester City':
        teamName = 'Leicester'
    team = Teams.query.filter_by(team_name=teamName).first()
    team_backup = TeamsLogo.query.filter_by(team_name=teamName).first()
    if team:
        return team.team_logo_url
    if team_backup:
        return team_backup.team_logo_url
    else:
        payload = {}
        headers = {
            'x-rapidapi-key': '46e3603952bbef534e2356d69f0a1ed6',
            'x-rapidapi-host': 'v3.football.api-sports.io',
            'season': 2023
        }
        connt.request("GET", f"/teams?name={teamName.replace(' ', '%20')}", headers=headers)
        res = connt.getresponse()
        data = res.read()
        data = json.loads(data.decode('utf-8'))
        teamid = data['response'][0]["team"]["id"]
        team_name = data["response"][0]["team"]["name"]
        country = data["response"][0]["team"]["country"]
        team_logo_url = data['response'][0]['team']['logo']
        team = TeamsLogo(teamid=teamid, team_name=team_name,
                         country=country, team_logo_url=team_logo_url)
        db.session.add(team)
        db.session.commit()
        team = TeamsLogo.query.filter_by(team_name=teamName).first()
        return team.team_logo_url


def formationplot(id,df):
    df = sb.events(match_id=id)
    home_position_id = []
    away_position_id = []

    # Add jersey numbers to lineup df
    home_jersey_number = []
    away_jersey_number = []

    # Add player names to lineup df
    home_player_name = []
    away_player_name = []

    for i in range(len(df['tactics'][0]['lineup'])):
        home_position_id.append(df['tactics'][0]['lineup'][i]['position']['id'])
        away_position_id.append(df['tactics'][1]['lineup'][i]['position']['id'])

        home_jersey_number.append(
            df['tactics'][0]['lineup'][i]['jersey_number'])
        away_jersey_number.append(
            df['tactics'][1]['lineup'][i]['jersey_number'])

        home_player_name.append(df.tactics[0]['lineup'][i]['player']['name'])
        away_player_name.append(df.tactics[1]['lineup'][i]['player']['name'])

    # Add position's x and y values
    home_position_x = []
    home_position_y = []
    away_position_x = []
    away_position_y = []
    for i in range(11):
        home_position_x.append(dct.get(home_position_id[i]).get('x') / 2)
        home_position_y.append(dct.get(home_position_id[i]).get('y'))
        away_position_x.append(
            120 - (dct.get(away_position_id[i]).get('x') / 2))
        away_position_y.append(dct.get(away_position_id[i]).get('y'))

    # Merges all lineup infos into home/away_lineup
    home_lineup = pd.DataFrame(list(zip(home_position_id, home_player_name, home_position_x, home_position_y, home_jersey_number)),
                               columns=['position_id', 'player_name', 'position_x', 'position_y', 'jersey_number'])
    away_lineup = pd.DataFrame(list(zip(away_position_id, away_player_name, away_position_x, away_position_y, away_jersey_number)),
                               columns=['position_id', 'player_name', 'position_x', 'position_y', 'jersey_number'])

    pitch = Pitch(pitch_type='statsbomb',
                  pitch_color='#22312b', line_color='white')
    fig, ax = pitch.draw(
        figsize=(12, 8), constrained_layout=True, tight_layout=False)

    # Plotting dots
    plt.scatter(home_lineup['position_x'],
                home_lineup['position_y'], color='blue', s=700)
    plt.scatter(away_lineup['position_x'],
                away_lineup['position_y'], color='red', s=700)

    # Plotting player names and jersey numbers
    for index, row in home_lineup.iterrows():
        pitch.annotate(int(row.jersey_number), xy=(row.position_x, row.position_y), c='white', va='center',
                       ha='center', size=15, ax=ax)
        pitch.annotate(row.player_name, xy=(row.position_x, row.position_y-3), c='white', va='center',
                       ha='center', size=8, ax=ax)
    for index, row in away_lineup.iterrows():
        pitch.annotate(int(row.jersey_number), xy=(row.position_x, row.position_y), c='white', va='center',
                       ha='center', size=15, ax=ax)
        pitch.annotate(row.player_name, xy=(row.position_x, row.position_y-3), c='white', va='center',
                       ha='center', size=8, ax=ax)

    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png', transparent=True)
    img_stream.seek(0)
    return img_stream

def passingNetworkmodel(id,team):
    df = sb.events(match_id=id)
    match_event_df = sb.events(match_id=id)
    df = df[(df['type'] == 'Pass')].reset_index(drop=True)
    starter_id = []
    for x in range(2):
        for y in range(11):
            player_id = match_event_df['tactics'][x]['lineup'][y]['player']['id']
            starter_id.append(player_id)

    # Seperates locations[x,y] and pass_end_location[x,y] into x_start,y_start,x_end,y_end
    df[['x_start', 'y_start']] = pd.DataFrame(
        df.location.tolist(), index=df.index)
    df[['x_end', 'y_end']] = pd.DataFrame(
        df.pass_end_location.tolist(), index=df.index)
    passing = df[df['player_id'].isin(starter_id)][['player', 'player_id', 'team', 'pass_recipient',
                                                        'x_start', 'y_start', 'x_end', 'y_end', 'pass_outcome']]
    # Variable will be used
    passing = passing[passing['team'] == team]
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


    p = Pitch(line_color='white', pitch_type='statsbomb',pitch_color='#22312b')
    fig, ax = p.draw(figsize=(12, 8))
    arrows = p.arrows(pass_between.x_start_x, pass_between.y_start_x,
                    pass_between.x_start_y, pass_between.y_start_y, ax=ax, width=3, headwidth=3, color='red')
    nodes = p.scatter(average_location.x_start, average_location.y_start, s=300,
                    color='#d3d3d3', edgecolors='black', linewidth=2.5, alpha=1, zorder=1, ax=ax)
    text_offset = 3  # You can increase or decrease this value to adjust the vertical offset
    for i, player_name in enumerate(average_location.index):
        ax.annotate(player_name, (average_location.x_start[i], average_location.y_start[i] - text_offset),
                    ha='center', va='top', fontsize=9, color='white', weight='bold')
    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png', transparent=True)
    img_stream.seek(0)
    return img_stream

def passmapmodelteam(id,team):
    data1 = sb.events(match_id=id)
    data1 = data1[(data1['team'] == team) & (
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
    pass_colors = {'Pass': 'green', 'Incomplete': 'red', 'Pass Offside': 'orange','Out': 'red','Unknown':'red','Injury Clearance':'orange'}
    for outcome in pass_outcomes:
        df_subset = df[df['pass_outcome'] == outcome]
        p.scatter(x=df_subset['x_start'], y=df_subset['y_start'],
                color=pass_colors[outcome], ax=ax)
        p.lines(xstart=df_subset['x_start'], ystart=df_subset['y_start'],
                xend=df_subset['x_end'], yend=df_subset['y_end'], color=pass_colors[outcome], ax=ax, comet=True)
    legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=pass_colors[outcome], markersize=10, label=outcome) for outcome in pass_outcomes]
    ax.legend(handles=legend_handles, loc='upper right')
    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png', transparent=True)
    img_stream.seek(0)
    return img_stream

def get_scorers(id,home_team,away_team):
    df = sb.events(match_id=id)
    HomeGoals = []
    AwayGoals = []
    HomeScorer = df[(df['shot_outcome'] == 'Goal') & (df['type'] == 'Shot') & (df['team']== home_team)].reset_index(drop=True)
    AwayScorers = df[(df['shot_outcome'] == 'Goal') & (df['type'] == 'Shot') & (df['team']== away_team)].reset_index(drop=True)
    OwnGoalsForHomeTeam = df[(df['type']=='Own Goal Against') & (df['team']== home_team)].reset_index(drop=True)
    OwnGoalsForAwayTeam = df[(df['type']=='Own Goal Against') & (df['team']== away_team)].reset_index(drop=True)
    print(OwnGoalsForAwayTeam)
    try:
        for i in range(0,len(HomeScorer)):
            player = HomeScorer['player'].values[i]
            minute = HomeScorer['minute'].values[i]+1
            HomeGoals.append(f"{player} ({minute}')")     
    except:
        pass
    try:
        for i in range(0,len(AwayScorers)):
            player = AwayScorers['player'].values[i]
            minute = AwayScorers['minute'].values[i]+1
            AwayGoals.append(f"{player} ({minute}')")
            
    except:
        pass
    try:
        for i in range(0,len(OwnGoalsForHomeTeam)+1):
            player = OwnGoalsForHomeTeam['player'].values[i]
            minute = OwnGoalsForHomeTeam['minutes'].values[i]+1
            print(player)
            AwayGoals.append(f"OG {player} {minute}")
    except:
        pass
    try:
        for i in range(0,len(OwnGoalsForAwayTeam)+1):
            player = OwnGoalsForAwayTeam['player'].values[i]
            minute = OwnGoalsForAwayTeam['minute'].values[i]+1
            print(player)
            HomeGoals.append(f" {player} ({minute}' OG)")
    except:
        pass
    return HomeGoals, AwayGoals
    
def passmapmodelplayer(id,player):
    data1 = sb.events(match_id=id)
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
    legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=pass_colors[outcome], markersize=10, label=outcome) for outcome in pass_outcomes]
    ax.legend(handles=legend_handles, loc='upper right')
    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png', transparent=True)
    img_stream.seek(0)
    return img_stream

def getPlayerNames(id,team):
    df = sb.events(match_id=id)
    player_info_df = df.loc[df['team'] == team, ['player_id', 'player', 'team']]
    player_info_df = player_info_df.drop_duplicates().reset_index(drop=True)
    player_info_df = player_info_df.dropna(subset=['player'])
    players = player_info_df['player'].tolist()
    return players

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your Account has been created! You are now able to log in', 'success')
        return redirect(url_for('favteam'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')


@app.route("/favteam")
@login_required
def favteam():
    data = Countries.query.all()
    return render_template('favteam.html', data=data)


@app.route('/query_country', methods=['POST'])
def query_country():
    try:
        data = request.get_json()
        country_name = data['countryName']

        # Query the country from the database using SQLAlchemy
        comps = Competitions.query.filter_by(country=country_name).all()
        if comps:
            # You can access the country's flag_url using country.flag_url

            results = [{'comp_name': c.name, 'logo_url': c.logo,
                        'comp_id': c.compid} for c in comps]

            return jsonify(results)
        else:
            return jsonify({'message': 'comps not found'})

    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/query_teams', methods=['POST'])
def query_teams():
    data = request.get_json()
    league_name = data['leagueName']
    country_name = data['lastClickedButtonCountry']
    comp = Competitions.query.filter_by(
        name=league_name, country=country_name).first()
    leagueid = comp.compid
    team = Teams.query.filter_by(compid=leagueid).all()
    if team:

        results = [{'teamid': t.teamid, 'team_badge': t.team_logo_url,
                    'comp_id': t.compid, 'team_name': t.team_name} for t in team]
        return jsonify(results)
    else:
        payload = {}
        headers = {
            'x-rapidapi-key': '46e3603952bbef534e2356d69f0a1ed6',
            'x-rapidapi-host': 'v3.football.api-sports.io',
            'season': 2023
        }
        connt.request(
            "GET", f"/teams?league={leagueid}&season=2023", headers=headers)
        res = connt.getresponse()
        data = res.read()
        data = json.loads(data.decode('utf-8'))
        for x in range(len(data['response'])):
            teamid = data['response'][x]["team"]["id"]
            team_name = data["response"][x]["team"]["name"]
            country = data["response"][x]["team"]["country"]
            team_logo_url = data['response'][x]['team']['logo']
            stadium_id = data['response'][x]['venue']['id']
            stadium_name = data['response'][x]['venue']['name']
            stadium_capacity = data['response'][x]['venue']['capacity']
            stadium_address = data['response'][x]['venue']['address']
            stadium_image = data['response'][x]['venue']['image']
            team = Teams(teamid=teamid, team_name=team_name, country=country, team_logo_url=team_logo_url, stadium_id=stadium_id,
                         stadium_name=stadium_name, stadium_capacity=stadium_capacity, stadium_image=stadium_image,stadium_address=stadium_address,compid=leagueid)
            db.session.add(team)
            db.session.commit()
        team = Teams.query.filter_by(compid=leagueid).all()
        results = [{'teamid': t.teamid, 'team_badge': t.team_logo_url,
                    'comp_id': t.compid, 'team_name': t.team_name} for t in team]
        return jsonify(results)


@app.route('/store_favteam', methods=['POST'])
def store_favteam():
    data = request.get_json()
    team_name = data['teamName']
    print(team_name)
    current_user.favourite_team = team_name
    db.session.commit()
    flash(f'{team_name} was selected as your Favourite Team!', 'success')
    return jsonify({})

# Fetches the competitions that I can use to show the data models



@app.route('/stats')
def stats():
    comps = sb.competitions()
    comp_season_data = []
    for index, row in comps.iterrows():
        comp_season_data.append((row['competition_name'], row['season_name']))

    return render_template('stats.html', data=comp_season_data)


@app.route('/get_comp_id&seasonid', methods=['POST'])
def get_comp_id_seasonid():
    data = request.get_json()
    compName = data['compName']
    compYear = data['compYear']
    match = Comps.query.filter_by(
        competition_name=compName, season_name=compYear).first()
    results = [{'compId': match.competition_id, 'seasonId': match.season_id}]
    return jsonify(results)


@app.route('/get_selected_comp', methods=['POST'])
def get_selected_comp():
    conn = db.engine.connect()
    print('starting')
    data = request.get_json()
    compId = data['compId']
    seasonId = data['seasonId']
    # matches = Comps.query.filter_by(competition_id=compId,season_id=seasonId)
    query = f'SELECT * FROM matches WHERE compId={compId} AND seasonId ={seasonId}'
    df = pd.read_sql_query(query, conn)
    if df.empty:
        print("Starting")
        matches = (sb.matches(competition_id=compId, season_id=seasonId))
        matches = matches.assign(compId=compId, seasonId=seasonId)
        matches.to_sql('matches', conn, if_exists='append', index=False)
        query = f'SELECT * FROM matches WHERE compId={compId} AND seasonId ={seasonId}'
        df = pd.read_sql_query(query, conn)

    else:
        pass
    conn.commit()
    conn.close()
    matches_json = df.to_json(orient='records')
    matches_json = json.loads(matches_json)
    return jsonify(matches_json)


@app.route('/get_match_stats', methods=['POST'])
def get_match_stats():
    conn = db.engine.connect()
    data = request.get_json()
    global gMATCH_ID
    global gHome_Score
    global gAway_Score
    global gHome_Team
    global gAway_Team
    gMATCH_ID = data['match_id']
    gHome_Score = data['match_home_score']
    gAway_Score = data['match_away_score']
    gHome_Team = data['match_home_team']
    gAway_Team = data['match_away_team']
    query = f'SELECT * FROM gamestats WHERE match_id={gMATCH_ID}'
    df = pd.read_sql_query(query, conn)
    if df.empty:
        matches = (sb.events(match_id=gMATCH_ID))
        matches = matches.assign(match_id=gMATCH_ID)
        matches = matches[['player_id', 'player', 'type', 'location', 'pass_outcome',
                           'pass_recipient', 'team', 'tactics', 'pass_type', 'match_id', 'shot_outcome']]
        matches = matches.astype(str)
        matches.to_sql('gamestats', conn, if_exists='append', index=False)
        query = f'SELECT * FROM gamestats WHERE match_id={gMATCH_ID}'
        df = pd.read_sql_query(query, conn)

    else:
        df = df.astype(str)
    conn.commit()
    conn.close()
    global Gmatches_dataframe
    Gmatches_dataframe = df
    return jsonify({})


@app.route('/matchstats')
def matchstats():
    team1_logo = logoChecker(gHome_Team)
    team2_logo = logoChecker(gAway_Team)
    home_players = getPlayerNames(gMATCH_ID,gHome_Team)
    away_players = getPlayerNames(gMATCH_ID,gAway_Team)
    print(home_players)
    homegoals,awaygoals = get_scorers(gMATCH_ID,gHome_Team,gAway_Team)
    score = str(gHome_Score) + " - " + str(gAway_Score)
    img_stream = formationplot(gMATCH_ID,Gmatches_dataframe)
    img_data = base64.b64encode(img_stream.read()).decode('utf-8')
    return render_template('matchstats.html', img_data=img_data,score=score, gHome_Team=gHome_Team, gAway_Team=gAway_Team, gMATCH_ID=gMATCH_ID,team1_logo=team1_logo,team2_logo=team2_logo,homegoals=homegoals,awaygoals=awaygoals,home_players=home_players,away_players=away_players)


@app.route('/get_passmapteam', methods=['POST'])
def get_passmap():
    data = request.get_json()
    team = data['team'] 
    passmap = passmapmodelteam(gMATCH_ID,team)
    passmap = base64.b64encode(passmap.read()).decode('utf-8')
    return jsonify({"image_data": passmap})

@app.route('/get_passmapplayer', methods=['POST'])
def get_passmapplayer():
    data = request.get_json()
    player = data['player'] 
    passmap = passmapmodelplayer(gMATCH_ID,player)
    passmap = base64.b64encode(passmap.read()).decode('utf-8')
    return jsonify({"image_data": passmap})

@app.route('/get_passnetwork', methods=['POST'])
def get_passnetwork():
    data = request.get_json()
    team = data['team'] 
    passnetwork = passingNetworkmodel(gMATCH_ID,team)
    passnetwork = base64.b64encode(passnetwork.read()).decode('utf-8')
    return jsonify({"image_data": passnetwork})

@app.route('/get_heatmap', methods=['POST'])
def get_heatmap():
    data = request.get_json()
    player = data['player'] 
    heatmap = heatMapmodel(gMATCH_ID,player)
    heatmap = base64.b64encode(heatmap.read()).decode('utf-8')
    return jsonify({"image_data": heatmap})

