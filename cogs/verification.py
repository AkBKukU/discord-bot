from discord.ext import commands
import asyncio


class Verification:
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.guild_only()
    @commands.command()
    async def verify(self, ctx, *, verification_string: str):
        """Does verification.

        See text on top of #verification for more info."""

        await ctx.message.delete()

        veriflogs_channel = ctx.guild.get_channel(self.config.veriflogs_chanid)
        verification_role = ctx.guild.get_role(self.config.read_rules_roleid)
        verification_wanted = self.config.verification_code\
            .replace("[discrim]", ctx.author.discriminator)

        if ctx.channel.id != self.config.verification_chanid:
            resp = await ctx.send("This command can only be used "
                                  f"on <#{self.config.verification_chanid}>.")
            await asyncio.sleep(self.config.sleep_secs)
            await resp.delete()
            return

        if verification_role in ctx.author.roles:
            resp = await ctx.send("This command can only by those without "
                                  f"<@&{self.config.read_rules_roleid}> role.")
            await asyncio.sleep(self.config.sleep_secs)
            await resp.delete()
            return

        if verification_string.lower().strip() == verification_wanted:
            resp = await ctx.send("Success! Welcome to the "
                                  f"club, {str(ctx.author)}.")
            await asyncio.sleep(self.config.sleep_secs)
            await veriflogs_channel.send(f"{str(ctx.author)} ({ctx.author.id})"
                                         " successfully got verified.")
            await ctx.author.add_roles(verification_role)
            await resp.delete()
        else:
            resp = await ctx.send(f"Incorrect password, {str(ctx.author)}.")
            await asyncio.sleep(self.config.sleep_secs)
            await resp.delete()


def setup(bot):
    bot.add_cog(Verification(bot))
