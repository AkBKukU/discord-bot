from discord.ext import commands
from discord.ext.commands import Cog
import asyncio
import config


class Verification(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command()
    async def verify(self, ctx, *, verification_string: str):
        """Does verification.

        See text on top of #verification for more info."""

        await ctx.message.delete()

        veriflogs_channel = ctx.guild.get_channel(config.veriflogs_chanid)
        verification_role = ctx.guild.get_role(config.read_rules_roleid)
        verification_wanted = config.verification_code\
            .replace("[discrim]", ctx.author.discriminator)

        # Do checks on if the user can even attempt to verify
        if ctx.channel.id != config.verification_chanid:
            resp = await ctx.send("This command can only be used "
                                  f"on <#{config.verification_chanid}>.")
            await asyncio.sleep(config.sleep_secs)
            return await resp.delete()

        if verification_role in ctx.author.roles:
            resp = await ctx.send("This command can only by those without "
                                  f"<@&{config.read_rules_roleid}> role.")
            await asyncio.sleep(config.sleep_secs)
            return await resp.delete()

        # Log verification attempt
        await self.bot.update_logs("Verification Attempt",
                                   ctx.author.id,
                                   veriflogs_channel,
                                   log_text=verification_string,
                                   digdepth=50, result=-1)

        # Check verification code
        if verification_string.lower().strip() == verification_wanted:
            resp = await ctx.send("Success! Welcome to the "
                                  f"club, {str(ctx.author)}.")
            await self.bot.update_logs("Verification Attempt",
                                       ctx.author.id,
                                       veriflogs_channel,
                                       digdepth=50, result=0)
            await asyncio.sleep(config.sleep_secs)
            await ctx.author.add_roles(verification_role)
            await resp.delete()
        else:
            resp = await ctx.send(f"Incorrect password, {str(ctx.author)}.")
            await asyncio.sleep(config.sleep_secs)
            await resp.delete()


def setup(bot):
    bot.add_cog(Verification(bot))
