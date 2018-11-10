from discord import NotFound
from datetime import datetime
import re


class Log:
    def __init__(self, bot):
        self.bot = bot
        self.bot.update_logs = self.update_logs
        self.re_lastentry_num = re.compile(r".*([0-9])\).*$")

    async def clean_log_text(self, log_text):
        log_text = log_text.strip().replace("\n", "").replace("\r", "")\
            .replace("`", "").replace("\\", "").replace(")", "")
        return log_text

    async def create_result_text(self, result):
        if result == -1:
            return "Ongoing"
        elif result == 0:
            return ":white_check_mark: Success"
        else:
            return f":x: {result}"

    async def create_log_message(self, log_name, userid,
                                 log_channel, log_text, result):
        status_text = await self.create_result_text(result)
        msg_text = (f"<@{userid}> ({userid}) - {log_name}\n```"
                    f"1) {str(datetime.utcnow())} {log_text}```\n"
                    f"{status_text}""")
        return await log_channel.send(msg_text)

    async def edit_log_message(self, last_message, log_text, result):
        split_msg = last_message.clean_content.split('```')

        lastentry_num = self.re_lastentry_num.findall(split_msg[1])[0]

        split_msg[1] = f"{split_msg[1]}\n{lastentry_num}) {log_text}"
        split_msg[2] = await self.create_result_text(result)

        msg_text = '```'.join(split_msg)

        return await last_message.edit(content=msg_text)

    async def get_message(self, userid, log_name,
                          log_channel, cache_list, digdepth):
        # Check if the message is present on the cache (if there is one)
        if cache_list and userid in cache_list:
            # Try to get the message and return it
            # If message does not exist, delete it from cache
            try:
                return await log_channel.get_message(cache_list[userid])
            except NotFound:
                del cache_list[userid]

        # Check if message is present in channel in last $digdepth messages
        async for potential_msg in log_channel.history(limit=digdepth):
            startwith_msg = f"<@{userid}> ({userid}) - {log_name}"
            if potential_msg.author == self.bot.user and\
                    potential_msg.startswith(startwith_msg):
                return potential_msg

        return None

    async def update_logs(self, log_name, userid,
                          log_channel, log_text=None,
                          cache_list=None, digdepth=25, result=-1):
        """ Updates logs for a user.

        - log_name: name for the log, duh

        - userid: self-explanatory
        It doesn't need to actually match user's ID
        You just need to use the same ID whenever you call this function

        - log_text: self-explanatory. Can be string, int, whatever.
        No log_text = just result update

        - log_channel: Which channel should we log to?
        Supply discord.channel, not int

        - cache_list: Supply a list if you want log message IDs to be cached
        No cache will be slower and use API more

        - digdepth: If no cached log message ID is found,
        how many messages should be checked in log_channel to find the prev ID?

        - result: What's the result of this log session?
        -1 = ongoing, 0 = success, anything else = failure with explanation
        """

        # Clean log text if it is set
        if log_text:
            log_text = await self.clean_log_text(log_text)

        # Attempt to get a log message
        log_msg = await self.get_message(userid, log_name, log_channel,
                                         cache_list, digdepth)

        # If message exists, edit it
        # If message does not exist*, create one and cache it
        # *: a new message will not be created if no log_text is given
        if log_msg:
            return await self.edit_log_message(log_msg, log_text, result)
        elif log_text:
            msg = await self.create_log_message(log_name, userid, log_channel,
                                                log_text, result)
            if cache_list:
                cache_list[userid] = msg.id

            return msg


def setup(bot):
    bot.add_cog(Log(bot))
