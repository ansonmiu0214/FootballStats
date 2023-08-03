import http.client
import json
import sqlite3
conn = http.client.HTTPSConnection("v3.football.api-sports.io")
def insert_league_data(league_id, league_name, league_logo):
    conn = sqlite3.connect("./instance/footballDB.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO competitions (compid, name, logo)
        VALUES (?, ?, ?)
    ''', (league_id, league_name, league_logo))
    
    conn.commit()
    conn.close()



payload = {}
headers = {
    'x-rapidapi-key': '46e3603952bbef534e2356d69f0a1ed6',
    'x-rapidapi-host': 'v3.football.api-sports.io',
    'season': 2023
}

#conn.request("GET", "/leagues?season=2023", headers=headers)
#res = conn.getresponse()
#data = res.read()

# Step 1: Open and read the JSON file
file_path = "football_leagues_data.json"

with open(file_path, "r") as file:
    data = json.load(file)
# Extract league information from the response
""" for x in range(len(data['response'])):
    league_id = data['response'][x]["league"]["id"]
    league_name = data["response"][x]["league"]["name"]
    league_logo = data["response"][x]["league"]["logo"]
    print(league_id,league_name,league_logo)
    insert_league_data(league_id, league_name, league_logo) """

