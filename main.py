# -*- coding: utf-8 -*-
import os

import botpy
from botpy import logging

from botpy.message import Message
from botpy.ext.cog_yaml import read

from functions.db_operate.db_firstjoin import update_whitelist_status
from functions.globalapi.kz_global_stats import KzGlobalStats
from functions.steam.steam import convert_steamid, is_in_group
from functions.steam.steam_user import check_steam_bans


test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_at_message_create(self, message: Message, steamid=None):
        _log.info(message.author.avatar)
        commands = ['/wl', '/白名单']
        for command in commands:
            if command in message.content:
                # 分割指令后面的指令参数
                steamid = message.content.split(command)[1].strip()
        _log.info(message.author.username)

        await message.reply(content=f"{self.robot.name}正在验证你的steam账号")
        steamid = convert_steamid(steamid, 'steamid')
        steamid64 = convert_steamid(steamid, 'steamid64')

        # Check if the player has been banned by VAC or multiple games
        ban_status = check_steam_bans(steamid64)
        if ban_status['vac_banned']:
            await message.reply(content="❌️你已被VAC封禁!!!")
            return
        elif ban_status['game_ban_count'] > 1:
            await message.reply(content=F"❌️你已被 {ban_status['game_ban_count']} 个游戏封禁!!!")
            return
        else:
            await message.reply(content="✅你未被封禁")

        # Check if the player is in steam group
        if is_in_group(steamid64):
            await message.reply(content="✅你在Steam组中")
        else:
            await message.reply(content="❌️你还未加入Steam组！！！")
            return

            # Check if the player got enough pts
        for i in range(3):
            stats = KzGlobalStats(steamid64, i)
            print(i)
            if stats.is_reach_pts():
                await message.reply(content="✅你的分数高于5W分")
                print(update_whitelist_status(steamid))
                await message.reply(content="✅已成功将你添加到白名单")
                return True

        await message.reply(content="❌️你没有达到5万分!!!")
        return False


if __name__ == "__main__":

    intents = botpy.Intents(public_guild_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], secret=test_config["secret"])