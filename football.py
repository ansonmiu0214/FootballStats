import requests
url = "https://v3.football.api-sports.io/standings?league=39&season=2019"

payload = {}
headers = {
    'x-rapidapi-key': '46e3603952bbef534e2356d69f0a1ed6',
    'x-rapidapi-host': 'v3.football.api-sports.io'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
