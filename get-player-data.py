from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo

# Basic Request
# player_info = commonplayerinfo.CommonPlayerInfo(player_id=2544)
player_dict = players.get_active_players()

players_length = len(player_dict)

print(player_dict[0]['id'])