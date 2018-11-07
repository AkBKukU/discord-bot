from discord.ext import commands
import config


class Moderation:
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    def check_if_staff(ctx):
        return any(r.id in config.staff_role_ids for r in ctx.author.roles)

    @commands.check(check_if_staff)
    @commands.command()
    async def purge(self, ctx, *, count: int):
        """Purges a number of messages, staff only."""
        count = 100 if count > 100 else count
        ctx.channel.purge(limit=count)


def setup(bot):
    bot.add_cog(Moderation(bot))
