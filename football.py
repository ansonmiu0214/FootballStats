from statsbombpy import sb
import csv
import requests
import pandas as pd
url = "https://v3.football.api-sports.io/standings?league=39&season=2019"

payload = {}
headers = {
    'x-rapidapi-key': '46e3603952bbef534e2356d69f0a1ed6',
    'x-rapidapi-host': 'v3.football.api-sports.io'
}

# response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)
print(sb.competitions())
data = sb.competitions()
print(type(data))


df = pd.DataFrame(data)

# Export the DataFrame to CSV
csv_file_name = "output.csv"
df.to_csv(csv_file_name)

print(f"Data exported to '{csv_file_name}' successfully.")
