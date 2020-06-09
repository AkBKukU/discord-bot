import discord
from discord.ext import commands


class Test:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def test1(self, ctx, user: discord.User):
        await ctx.send(f"{user.id} - {str(user)}")

    @commands.command(hidden=True)
    async def test2(self, ctx, user: discord.Member):
        await ctx.send(f"{user.id} - {str(user)}")


def setup(bot):
    bot.add_cog(Test(bot))
