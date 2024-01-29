import asyncio

import discord.ext.commands
from discord import Embed

from dc_utils.info import set_wl_role
from functions.database import discord_id_to_steamid
from functions.db_operate.db_firstjoin import update_whitelist_status
from functions.globalapi.kz_global_stats import KzGlobalStats
from functions.steam.steam import convert_steamid, is_in_group
from functions.steam.steam_user import check_steam_bans


async def get_whitelisted(ctx):
    ms = await ctx.send("loading...")
    user_id = ctx.author.id
    steamid = discord_id_to_steamid(user_id)
    steamid64 = convert_steamid(steamid, 'steamid64')
    embeds = []
    # Check if the player has been banned by VAC or multiple games
    ban_status = check_steam_bans(steamid64)
    if ban_status['vac_banned']:
        embeds.append(Embed(title="You have been banned by VAC!!!", colour=discord.Colour.red()))
        await ms.edit(embeds=embeds)
        return
    elif ban_status['game_ban_count'] > 1:
        embeds.append(Embed(title=f"You have been banned by {ban_status['game_ban_count']} games!!!", colour=discord.Colour.red()))
        await ms.edit(embeds=embeds)
        return
    else:
        embeds.append(Embed(title=f"You haven't been banned", colour=discord.Colour.green()))
        await ms.edit(embeds=embeds)

    # Check if the player is in steam group
    if is_in_group(steamid64):
        embeds.append(Embed(title=f"You're In the Steam Group", colour=discord.Colour.green()))
        await ms.edit(embeds=embeds)
    else:
        embeds.append(Embed(title=f"You haven't join in Steam Group yet!", colour=discord.Colour.red()))
        await ms.edit(embeds=embeds)
        return

        # Check if the player got enough pts
    for i in range(3):
        stats = KzGlobalStats(steamid64, i)
        print(i)
        if stats.is_reach_pts():
            embeds.append(Embed(title=f"You reached 50k pts!!", colour=discord.Colour.green()))
            await ms.edit(embeds=embeds)
            update_whitelist_status(steamid)
            embeds.append(Embed(title=f"Added you to the whitelist", colour=discord.Colour.green()))
            await ms.edit(embeds=embeds)
            await set_wl_role(ctx, steamid)
            break

    await ms.edit(embeds=Embed(title=f"You Didn't reach 50k pts!!", colour=discord.Colour.red()))
