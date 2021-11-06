import json
import time
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo

# Basic Request
# player_info = commonplayerinfo.CommonPlayerInfo(player_id=1630247)
# print(player_info.get_json())
player_dict = players.get_active_players()
time.sleep(.1000)
# print(player_dict)

players_length = len(player_dict)
player_stat_dict = []

# test = player_dict[0]['id']
for i in range (0, players_length):
    player_stats = {}
    player_id = player_dict[i]['id']
    print(player_id)
    time.sleep(.1000)
    print("sleep done")
    req = commonplayerinfo.CommonPlayerInfo(player_id)
    print("req processed")
    player_data = json.loads(req.get_json())["resultSets"][1]
    print(player_data)
    try:
        headers = player_data["headers"]
        values = player_data["rowSet"][0]
        print(headers, values)
        for j in range (0, 6):
            player_stats[headers[j]] = values[j]
        player_stat_dict.append(player_stats)
    except IndexError:
        continue


print(player_stat_dict)

