import asyncio
from datetime import datetime, timezone

import discord

from dc_utils.server_status import embeds_server_status
from functions.embed_content import get_jstop
from functions.steam.a2s import query_all_servers, query_server_embed


async def server_list_embed_loop(message):
    while True:
        # Function that updates the content of the embedded message
        current_datetime = datetime.now(timezone.utc)
        new_content = query_all_servers()
        embed = discord.Embed(
            title='AXE SERVER LIST',
            description=new_content,
            colour=0x60FFFF,
            timestamp=current_datetime
        )

        # Edit the embedded message with the new content
        await message.edit(embed=embed)

        # Wait for one minute before the next update
        await asyncio.sleep(58)


async def gz_server_embeds_loop(message: discord.Message, servers, bot):
    while True:
        embeds = [await query_server_embed(s, bot) for s in servers]
        await message.edit(embeds=embeds)
        await asyncio.sleep(59)


async def bj_server_embeds_loop(message: discord.Message, servers, bot):
    while True:
        embeds = [await query_server_embed(s, bot) for s in servers]
        await message.edit(embeds=embeds)
        await asyncio.sleep(60)


async def server_status_loop(message: discord.Message):
    while True:
        embeds = embeds_server_status()
        await message.edit(embeds=embeds)
        await asyncio.sleep(61)


async def jstop_embeds_loop(message: discord.Message):
    while True:
        embeds = []
        embed1 = get_jstop(20, 'kzt')
        embed2 = get_jstop(10, 'skz')
        embed3 = get_jstop(10, 'vnl')
        embeds.append(embed1)
        embeds.append(embed2)
        embeds.append(embed3)
        await message.edit(embeds=embeds)
        await asyncio.sleep(10800)
