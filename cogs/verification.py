from discord.ext import commands
import asyncio


class Verification:
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command()
    async def verify(self, ctx, *, verification_string: str):
        """Does verification.

        See text on top of #verification for more info."""

        await ctx.message.delete()

        # TODO: pull from config
        sleep_secs = 3
        verification_channelid = 497446376234287114
        ver_logs_channelid = 498931990045655047
        verification_roleid = 497446531729850391

        ver_logs_channel = ctx.guild.get_channel(ver_logs_channelid)
        verification_role = ctx.guild.get_role(verification_roleid)
        verification_wanted = f"nice{ctx.author.discriminator}"

        if ctx.channel.id != verification_channelid:
            resp = await ctx.send("This command can only be used " +
                                  f"on <#{verification_channelid}>.")
            await asyncio.sleep(sleep_secs)
            await resp.delete()
            return

        if verification_role in ctx.author.roles:
            resp = await ctx.send("This command can only by those " +
                                  f"without <@&{verification_roleid}> role.")
            await asyncio.sleep(sleep_secs)
            await resp.delete()
            return

        if verification_string.lower().trim() == verification_wanted:
            resp = await ctx.send("Success! Welcome to the "
                                  f"club, {str(ctx.author)}.")
            await asyncio.sleep(sleep_secs)
            await ctx.author.add_roles(verification_role)
            await ver_logs_channel.send(f"{str(ctx.author)} ({ctx.author.id})"
                                        " successfully got verified.")
            await resp.delete()
        else:
            resp = await ctx.send(f"Incorrect password, {str(ctx.author)}.")
            await asyncio.sleep(sleep_secs)
            await resp.delete()


def setup(bot):
    bot.add_cog(Verification(bot))
