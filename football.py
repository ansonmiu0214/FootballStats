import http.client
import json
import sqlite3
conn = http.client.HTTPSConnection("v3.football.api-sports.io")
def insert_league_data(teamid,team_name,country,team_logo_url,stadium_id,stadium_name,stadium_capacity,stadium_image,league_id):
    conn = sqlite3.connect("./instance/footballDB.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO teams(teamid, team_name,country,team_logo_url,stadium_id,stadium_name,stadium_capacity,stadium_image,compid)
        VALUES (?,?,?,?,?,?,?,?,?)
    ''', (teamid,team_name,country,team_logo_url,stadium_id,stadium_name,stadium_capacity,stadium_image,league_id))
    
    conn.commit()
    conn.close()



payload = {}
headers = {
    'x-rapidapi-key': '46e3603952bbef534e2356d69f0a1ed6',
    'x-rapidapi-host': 'v3.football.api-sports.io',
    'season': 2023
}
league_id = 78
conn.request("GET", f"/teams?league={league_id}&season=2023", headers=headers)
res = conn.getresponse()
data = res.read()
data = json.loads(data.decode('utf-8'))
# Step 1: Open and read the JSON file

# Extract league information from the response
for x in range(len(data['response'])):
    teamid = data['response'][x]["team"]["id"]
    team_name = data["response"][x]["team"]["name"]
    country = data["response"][x]["team"]["country"]
    team_logo_url = data['response'][x]['team']['logo']
    stadium_id = data['response'][x]['venue']['id']
    stadium_name = data['response'][x]['venue']['name']
    stadium_capacity = data['response'][x]['venue']['capacity']
    stadium_image = data['response'][x]['venue']['image']
    insert_league_data(teamid,team_name,country,team_logo_url,stadium_id,stadium_name,stadium_capacity,stadium_image,league_id)

