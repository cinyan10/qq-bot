import random
from datetime import datetime
import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Bot
from config import TEST_CHANNEL_ID, INFO_CHANNEL_ID, ANNOUNCEMENT_MESSAGE_ID
from dc_utils.announcement import AnnouncementView, ANNOUNCEMENTS

RESPONSES = ["meow~", "Itami~ >.<", "What's the matter, gosyujinnsama?", "pong~", "UwU", "don't poke me, plz T^T"]


class Basic(commands.Cog):

    def __init__(self, bot):
        self.bot: Bot = bot

    async def commands_sync(self):
        await self.bot.tree.sync()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user.name} (ID: {self.bot.user.id})')
        await self.commands_sync()

        title = "I'm successfully started!!"
        embed = Embed(title=title, colour=discord.Colour.green(), timestamp=datetime.now())
        await self.bot.get_channel(TEST_CHANNEL_ID).send(embed=embed)

        channel_id = INFO_CHANNEL_ID
        message_id = ANNOUNCEMENT_MESSAGE_ID
        channel = self.bot.get_channel(channel_id)

        if channel:
            try:
                message = await channel.fetch_message(message_id)
                await message.edit(embed=ANNOUNCEMENTS[0], view=AnnouncementView())
            except discord.NotFound:
                print(f'Message with ID {message_id} not found.')
        else:
            print(f'Channel with ID {channel_id} not found.')

    @commands.hybrid_command()
    async def ping(self, ctx):
        """Pings the bot"""
        result = random.choice(RESPONSES)
        await ctx.send(f'{result}')

    @commands.hybrid_command()
    @commands.has_permissions(administrator=True)
    async def sync(self, ctx):
        await self.commands_sync()
        await ctx.send("Sync completed!")


async def setup(bot):
    await bot.add_cog(Basic(bot))
