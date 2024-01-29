from discord.ext import commands
from config import *

from dc_utils.serverinfo import *
from config import SERVER_LIST
from functions.misc import get_or_create_message


class LoopUpdates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channels_info = [
            (SERVER_LIST_CHANNEL_ID, 'AXE SERVER LIST', server_list_embed_loop),
            (GUANGZHOU_CHANNEL_ID, '广州 SERVER LIST', lambda msg: gz_server_embeds_loop(msg, SERVER_LIST[:6], self.bot)),
            (BEIJING_CHANNEL_ID, '北京 SERVER LIST', lambda msg: bj_server_embeds_loop(msg, SERVER_LIST[6:], self.bot)),
            (JSTOP_CLIENT_ID, 'LocalStats Top', jstop_embeds_loop),
            (STATUS_CHANNEL_ID, 'SERVER STATUS', server_status_loop)
        ]

    async def setup_loop(self, channel_id, title, loop_func):
        channel = self.bot.get_channel(channel_id)
        existing_message = await get_or_create_message(channel, title, 'Loading...')
        loop_task = asyncio.create_task(loop_func(existing_message))
        await loop_task

    @commands.Cog.listener()
    async def on_ready(self):
        loop_tasks = [self.setup_loop(channel_id, title, func) for channel_id, title, func in self.channels_info]
        await asyncio.gather(*loop_tasks)


async def setup(bot):
    await bot.add_cog(LoopUpdates(bot))
