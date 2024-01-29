import discord
from discord import Embed

from functions.database import discord_id_to_steamid, get_steam_user_name, retrieve_join_date, retrieve_last_seen, \
    get_country_from_steamid32, query_jumpstats_top
from functions.db_operate.db_firstjoin import get_playtime
from functions.globalapi.kzgoeu import get_kzgoeu_profile_url
from functions.misc import format_string_to_datetime, get_country_code, seconds_to_hms
from functions.steam.steam import convert_steamid, get_steam_pfp, get_steam_profile_url


def user_info(discord_id=None, steamid=None) -> discord.Embed:

    if steamid is None:
        steamid = discord_id_to_steamid(discord_id)
    else:
        steamid = convert_steamid(str(steamid), 'steamid')
    steamid64 = convert_steamid(steamid, 'steamid64')
    steamid32 = convert_steamid(steamid, 'steamid32')

    name = get_steam_user_name(steamid)
    joindate = format_string_to_datetime(retrieve_join_date(steamid))
    lastseen = format_string_to_datetime(retrieve_last_seen(steamid))
    pfp_url = get_steam_pfp(steamid64)
    profile_url = get_steam_profile_url(steamid64)
    kzgoeu_url = get_kzgoeu_profile_url(steamid)
    country = get_country_code(get_country_from_steamid32(steamid32)).lower()
    playtime = get_playtime(steamid)
    hours, minutes, seconds = seconds_to_hms(playtime)

    content = (
        f":flag_{country}: **{name}**\n"
        f"**steamID**: `{steamid}`\n"
        f"**steamID64**: `{steamid64}`\n"
        f"**First Join**: {joindate}\n"
        f"**Last Seen**: {lastseen}\n"
        f"**Playtime**: {hours}h, {minutes}m, {seconds}s,\n"
    )

    embed = Embed(
        title=f"Info",
        description=content,
        colour=discord.Colour.blue(),
    )
    embed.set_author(name=f"{name}", icon_url=pfp_url, url=profile_url)
    embed.url = kzgoeu_url
    embed.set_image(url=pfp_url)

    return embed


def get_jstop(limit: int, mode: str) -> discord.Embed:
    content = query_jumpstats_top(limit, mode)
    embed = Embed(
        title="JUMPSTATS TOP " + mode.upper(),
        description=content,
        colour=discord.Colour.green()
    )

    return embed
