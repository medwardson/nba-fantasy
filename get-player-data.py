import json
import os
import psycopg2
import time
import requests
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('BITTOKEN')
pw = os.getenv('PASSWORD')

# Get all active NBA Players
player_dict = players.get_active_players()
time.sleep(.1000)

# Create a new array to store the new information
players_length = len(player_dict)
player_stat_dict = []

for i in range (0, players_length):
    player_stats = {}
    player_id = player_dict[i]['id']
    print("Now processing ", player_id)
    time.sleep(.1000)
    req = commonplayerinfo.CommonPlayerInfo(player_id)
    data = json.loads(req.get_json())
    player_personal_data = data["resultSets"][0]
    player_data = data["resultSets"][1]

    try:
        headers = player_data["headers"]
        values = player_data["rowSet"][0]
        personalHeaders = player_personal_data["headers"]
        personalValues = player_personal_data["rowSet"][0]      
        for j in range (0, 6):
            player_stats[headers[j]] = values[j]
        player_stats[personalHeaders[14]] = personalValues[14]
        player_stats[personalHeaders[19]] = personalValues[19]
        player_stat_dict.append(player_stats)
    except IndexError:
        continue


print(player_stat_dict)
f = open("playerdata.json", "w")
f.write(json.dumps(player_stat_dict))
f.close()

conn = psycopg2.connect(
   database="bitdotio", user='medwardson_demo_db_connection', password=pw, host='db.bit.io', port= '5432'
)


# Setting auto commit false
conn.autocommit = True

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Doping EMPLOYEE table if already exists
cursor.execute('DROP TABLE "medwardson/nba-data"."playerdata"')
print("Table dropped... ")

#Commit your changes in the database
conn.commit()

#Closing the connection
conn.close()


with open("playerdata.json", 'rb') as f:
    data = f.read()

url = 'https://import.bit.io/medwardson/nba-data/playerdata'

headers = {
    "Content-Disposition": "attachment;filename='test.csv'",
    "Authorization": "Bearer {}".format(token)
}

response = requests.request("POST", url, headers=headers, data=data)
print("Table added")