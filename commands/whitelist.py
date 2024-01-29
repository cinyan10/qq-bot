from discord.ext import commands
from discord.ext.commands import Bot

from dc_utils.whitelist import get_whitelisted


class Whitelist(commands.Cog):

    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.hybrid_command(name="whitelist")
    async def whitelist(self, ctx):
        """Get Whitelisted!!"""
        await get_whitelisted(ctx)


async def setup(bot):
    await bot.add_cog(Whitelist(bot))
