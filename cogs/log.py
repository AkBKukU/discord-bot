import os
from discord import NotFound
from datetime import datetime
import re
import json


class Log:
    def __init__(self, bot):
        self.bot = bot
        self.bot.update_logs = self.update_logs
        self.re_lastentry_num = re.compile(r".*([0-9])\).*$")
        self.cache_filename = "log_cache.json"
        self.log_caches = self.load_cache()

    async def clean_log_text(self, log_text):
        log_text = log_text.strip().replace("\n", "").replace("\r", "")\
            .replace("`", "").replace("\\", "").replace(")", "")
        return log_text

    async def create_result_text(self, result):
        if result == -1:
            return "**Status:** :arrow_right: Ongoing"
        elif result == 0:
            return "**Status:** :white_check_mark: Success"
        else:
            return f"**Status:** :x: {result}"

    async def create_log_message(self, log_name, userid,
                                 log_channel, log_text, result):
        status_text = await self.create_result_text(result)
        msg_text = (f"<@{userid}> ({userid}) - {log_name}\n```"
                    f"1) <{str(datetime.utcnow())}> {log_text}```"
                    f"{status_text}""")
        return await log_channel.send(msg_text)

    async def edit_log_message(self, last_message, log_text, result):
        split_msg = last_message.content.split('```')

        lastentry_num = self.re_lastentry_num.findall(split_msg[1])[0]
        current_num = int(lastentry_num) + 1

        if not log_text:
            log_text = ""

        result_candidate = await self.create_result_text(result)
        if split_msg[2] != result_candidate:
            split_msg[2] = result_candidate
            log_text += f" [result changed to {result}]"

        split_msg[1] = (f"{split_msg[1]}\n{current_num}) "
                        f"<{str(datetime.utcnow())}> {log_text.strip()}")

        msg_text = '```'.join(split_msg)

        return await last_message.edit(content=msg_text)

    async def get_message(self, userid, log_name,
                          log_channel, digdepth):
        # Check if the message is present on the cache (if there is one)
        msg_cache = await self.get_cache_entry(log_name, userid)
        if msg_cache:
            self.bot.log.info(f"{userid} found in cache"
                              f" as {msg_cache}")
            # Try to get the message and return it
            # If message does not exist, delete it from cache
            try:
                return await log_channel.get_message(msg_cache)
            except NotFound:
                self.bot.log.info(f"{userid} cache invalid, removing")
                await self.del_cache_entry(log_name, userid)

        # Check if message is present in channel in last $digdepth messages
        async for potential_msg in log_channel.history(limit=digdepth):
            startwith_msg = f"<@{userid}> ({userid}) - {log_name}"
            if potential_msg.author == self.bot.user and\
                    potential_msg.content.startswith(startwith_msg):
                self.bot.log.info(f"Found log for {userid}: {potential_msg.id}")
                await self.set_cache_entry(log_name, userid, potential_msg.id)
                return potential_msg

        return None

    async def save_cache(self):
        with open(self.cache_filename, 'w') as json_file:
            json.dump(self.log_caches, json_file)
        self.bot.log.info(f"Saved cache to {self.cache_filename}.")

    def load_cache(self):
        # If file is empty, don't attempt to load it
        if not os.path.isfile(self.cache_filename)\
                or os.path.getsize(self.cache_filename):
            self.bot.log.info(f"{self.cache_filename} not found or empty.")
            return {}

        with open(self.cache_filename) as json_data:
            self.bot.log.info(f"Loaded cache from {self.cache_filename}.")
            return json.load(json_data)

    async def get_cache_entry(self, log_name, entry_name):
        # Check if cache contains the entry, if not, return None
        if log_name not in self.log_caches or entry_name not in\
                self.log_caches[log_name]:
            return None

        # Get the cached value, log it and return it
        cache_res = self.log_caches[log_name][entry_name]
        self.bot.log.info(f"Get cache: {log_name}-{entry_name}-{cache_res}")
        return cache_res

    async def set_cache_entry(self, log_name, entry_name, entry_value):
        if log_name not in self.log_caches:
            self.log_caches[log_name] = {}
            self.bot.log.info(f"Created {log_name} in cache")

        self.log_caches[log_name][entry_name] = entry_value
        self.bot.log.info(f"Set cache: {log_name}-{entry_name}-{entry_value}")
        await self.save_cache()
        return True

    async def del_cache_entry(self, log_name, entry_name):
        # Check if cache contains the entry, if not, return None
        if log_name not in self.log_caches and entry_name not in\
                self.log_caches[log_name]:
            return False

        del self.log_caches[log_name][entry_name]

        self.bot.log.info(f"Del cache: {log_name}-{entry_name}")
        await self.save_cache()
        return True

    async def update_logs(self, log_name, userid,
                          log_channel, log_text=None,
                          digdepth=25, result=-1):
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
            self.bot.log.info("Cleaned log text")

        # Attempt to get a log message
        log_msg = await self.get_message(userid, log_name,
                                         log_channel, digdepth)

        # If message exists, edit it
        # If message does not exist*, create one and cache it
        # *: a new message will not be created if no log_text is given
        if log_msg:
            self.bot.log.info("Log msg found, editing")
            return await self.edit_log_message(log_msg, log_text, result)
        elif log_text:
            self.bot.log.info("Log msg not found, creating")
            msg = await self.create_log_message(log_name, userid, log_channel,
                                                log_text, result)
            await self.set_cache_entry(log_name, userid, msg.id)

            return msg


def setup(bot):
    bot.add_cog(Log(bot))
