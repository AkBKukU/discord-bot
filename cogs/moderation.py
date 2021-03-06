from discord.ext import commands
from discord.ext.commands import Cog
import config


class Moderation(Cog):
    def __init__(self, bot):
        self.bot = bot

    def check_if_staff(ctx):
        return any(r.id in config.staff_role_ids for r in ctx.author.roles)

    @commands.check(check_if_staff)
    @commands.command()
    async def purge(self, ctx, *, count: int):
        """Purges a number of messages, staff only."""
        count = 100 if count > 100 else count
        await ctx.channel.purge(limit=count)


def setup(bot):
    bot.add_cog(Moderation(bot))
