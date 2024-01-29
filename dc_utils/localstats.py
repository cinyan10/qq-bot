from datetime import datetime

import discord
from discord import Embed

from functions.db_operate.db_firstjoin import get_whitelisted_players, get_playtime
from functions.misc import seconds_to_hms
from functions.steam.steam import convert_steamid, get_steam_username, get_steam_profile_url


def get_playtime_rank() -> list[Embed]:
    embeds = []
    steamids = get_whitelisted_players()

    datas = []
    count = 0
    for steamid in steamids:
        count = count + 1
        print(f"{count}/{len(steamids)} {steamid}")
        steamid64 = convert_steamid(steamid, 'steamid64')
        playtime = get_playtime(steamid)
        name = get_steam_username(steamid64)
        url = get_steam_profile_url(steamid64)
        datas.append([name, steamid64, playtime, url])

    datas = sorted(datas, key=lambda x: x[2], reverse=True)
    chunk_size = 20
    sublists = [datas[i:i + chunk_size] for i in range(0, len(datas), chunk_size)]
    count = 0

    for sublist in sublists:
        content = ''
        for player in sublist:
            hours, minutes, seconds = seconds_to_hms(player[2])
            count += 1
            content += f'[**{count}. {player[0]}**]({player[3]}) - Play Time: **{hours}h, {minutes}m, {seconds}s**\n'
        embeds.append(Embed(description=content, colour=discord.Colour.blue()))

    embeds[0].title = 'Playtime Ranking'
    embeds[-1].timestamp = datetime.now()

    return embeds


if __name__ == '__main__':
    rs = get_playtime_rank()
    print(rs)
