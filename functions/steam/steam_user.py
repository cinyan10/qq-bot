import discord
import requests
from discord import Embed

from config import STEAM_API_KEY


def get_steam_profile_info(steamid64):
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={STEAM_API_KEY}&steamids={steamid64}"

    try:
        response = requests.get(url)
        data = response.json()

        # Check if the response contains the player data
        if 'response' in data and 'players' in data['response']:
            player_data = data['response']['players'][0]

            name = player_data['personaname']
            avatar_url = player_data['avatarfull']
            profile_url = player_data['profileurl']

            return name, avatar_url, profile_url
        else:
            return None, None, None

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None, None, None


def embed_set_author_steam(embed: discord.Embed, steamid64):
    name, avatar_url, profile_url = get_steam_profile_info(steamid64)

    embed.set_author(name=name, url=profile_url, icon_url=avatar_url)

    return embed


def embed_user_steam(steamid64):
    name, avatar_url, profile_url = get_steam_profile_info(steamid64)

    embed = Embed()
    embed.set_author(name=name, url=profile_url, icon_url=avatar_url)

    return embed


def check_steam_bans(steamid64):
    """return {
        'vac_banned': True,
        'game_ban_count': 3,
        'community_banned': False,
        'economy_ban': 'none'
        }"""
    url = f'http://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key={STEAM_API_KEY}&steamids={steamid64}'
    response = requests.get(url)
    ban_data = response.json()

    # The response contains a list of players, but since we only requested one SteamID, we'll have only one entry.
    player_ban_info = ban_data['players'][0]

    # Check for VAC bans and game bans
    vac_banned = player_ban_info['VACBanned']
    game_ban_count = player_ban_info['NumberOfGameBans']

    # You can also check for community bans and economy bans (trade bans)
    community_banned = player_ban_info['CommunityBanned']
    economy_ban = player_ban_info['EconomyBan']

    return {
        'vac_banned': vac_banned,
        'game_ban_count': game_ban_count,
        'community_banned': community_banned,
        'economy_ban': economy_ban
    }


if __name__ == '__main__':
    user_steamid64 = "76561198083328612"
    rs = check_steam_bans(user_steamid64)
    print(rs)
    pass
