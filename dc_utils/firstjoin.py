from functions.db_operate.db_firstjoin import find_player_by_name_partial_match
from functions.embed_content import user_info


async def find_player(ctx, name):

    players = find_player_by_name_partial_match(name)
    if len(players) == 0:
        return await ctx.send("No players found or found more than 5 players")

    embeds = []
    for player in players:
        embed = user_info(steamid=player)
        embeds.append(embed)

    await ctx.send(embeds=embeds)
