from flask import render_template, url_for, flash, redirect, request, jsonify
from flaskproject import app, db, bcrypt
from flaskproject.forms import RegistrationForm, LoginForm
from flaskproject.models import User, Countries, Competitions, Teams
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import text
import http.client
import json
import sqlite3

conn = http.client.HTTPSConnection("v3.football.api-sports.io")

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
        return redirect(url_for('login'))
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
def favteam():
    sql_query = text("SELECT * FROM countries;")
    data = db.session.execute(sql_query)
    return render_template('favteam.html',data=data)

@app.route('/query_country', methods=['POST'])
def query_country():
    try:
        data = request.get_json()
        country_name = data['countryName']

        # Query the country from the database using SQLAlchemy
        comps = Competitions.query.filter_by(country=country_name).all()
        if comps:
            # You can access the country's flag_url using country.flag_url

            results = [{'comp_name': c.name, 'logo_url': c.logo, 'comp_id': c.compid} for c in comps]

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
    comp = Competitions.query.filter_by(name=league_name,country = country_name).first()
    leagueid = comp.compid
    team = Teams.query.filter_by(compid=leagueid).all()
    if team:

        results = [{'teamid': t.teamid, 'team_badge': t.team_logo_url, 'comp_id': t.compid, 'team_name': t.team_name} for t in team]
        return jsonify(results)
    else:
        #Inserting into the database
        #Function that inserts the data
        def insert_league_data(teamid,team_name,country,team_logo_url,stadium_id,stadium_name,stadium_capacity,stadium_image,leagueid):
            conn = sqlite3.connect("./instance/footballDB.db")
            cursor = conn.cursor()
    
            cursor.execute('''
                INSERT INTO teams(teamid, team_name,country,team_logo_url,stadium_id,stadium_name,stadium_capacity,stadium_image,compid)
                    VALUES (?,?,?,?,?,?,?,?,?)
                ''', (teamid,team_name,country,team_logo_url,stadium_id,stadium_name,stadium_capacity,stadium_image,leagueid))
    
            conn.commit()
            conn.close()

        payload = {}
        headers = {
        'x-rapidapi-key': '46e3603952bbef534e2356d69f0a1ed6',
        'x-rapidapi-host': 'v3.football.api-sports.io',
        'season': 2023
        }
        conn.request("GET", f"/teams?league={leagueid}&season=2023", headers=headers)
        res = conn.getresponse()
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
            stadium_image = data['response'][x]['venue']['image']
            insert_league_data(teamid,team_name,country,team_logo_url,stadium_id,stadium_name,stadium_capacity,stadium_image,leagueid)
        team = Teams.query.filter_by(compid=leagueid).all()
        results = [{'teamid': t.teamid, 'team_badge': t.team_logo_url, 'comp_id': t.compid, 'team_name': t.team_name} for t in team]
        return jsonify(results)

