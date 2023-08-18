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
teamid = 33
players = []
payload = {}
headers = {
    'x-rapidapi-key': '46e3603952bbef534e2356d69f0a1ed6',
    'x-rapidapi-host': 'v3.football.api-sports.io',
    'season': 2023
}
connt.request(
    "GET", f"/players/squads?team={teamid}", headers=headers)
res = connt.getresponse()
data = res.read()
data = json.loads(data.decode('utf-8'))
for i in range(len(data['response'][0]['players'])):
    playerid = data['response'][0]['players'][i]['id']
    player_name = data['response'][0]['players'][i]['name']
    player_number = data['response'][0]['players'][i]['number']
    player_position = data['response'][0]['players'][i]['position']
    player_photo = data['response'][0]['players'][i]['photo']
    print(playerid,player_name,player_number,player_position,player_photo)