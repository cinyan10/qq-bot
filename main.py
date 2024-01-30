# -*- coding: utf-8 -*-
import os

import botpy
from botpy import logging

from botpy.message import Message
from botpy.ext.cog_yaml import read

from config import KZ_MODES
from functions.db_operate.db_discord import get_kzmode
from functions.db_operate.db_gokz import get_ljpb
from functions.db_operate.qq import reset_steamid_by_qq_id, qq_to_steamid, update_steamid, set_kzmode
from functions.db_operate.db_firstjoin import update_whitelist_status, get_playtime
from functions.globalapi.kz_global_stats import KzGlobalStats
from functions.gokzcn import fetch_playerdata
from functions.misc import seconds_to_hms
from functions.steam.a2s import query_all_servers_text
from functions.steam.steam import convert_steamid, is_in_group
from functions.steam.steam_user import check_steam_bans


test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging


async def whitelist(message: Message):
    steamid = qq_to_steamid(message.author.id)
    await message.reply(content=f"正在验证你的steam账号")
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


async def info(message: Message, steamid=None, mode='kzt'):
    await message.reply(content='加载中...')
    steamid = convert_steamid(steamid, 'steamid')
    steamid64 = convert_steamid(steamid, "steamid64")
    steamid32 = convert_steamid(steamid, "steamid32")
    stats = KzGlobalStats(steamid64=steamid64, kzmode=mode)
    content = stats.text_stats()

    # gokz.cn 排名
    try:
        cn_data = fetch_playerdata(steamid)
        content += f"cn排名：{cn_data['ranking']} 技术得分：{cn_data['point_skill']}\n"
    except Exception as e:  # NOQA
        content += f"获取cn数据失败\n"

    # 服务器内时间
    seconds = get_playtime(steamid)
    h, m, s = seconds_to_hms(seconds)
    content += f"服务器内游玩时间：{h} 时 {m}分 {s}秒\n"

    # LJPB
    try:
        ljpb = get_ljpb(steamid32, 'kzt', 0, 0)
        content += f"LJPB : {ljpb['Distance']}"
    except Exception as e:
        content += '获取LJPB数据失败'
    await message.reply(content=content)


async def bind_steam(message: Message, steamid=None):
    qq_id = message.author.id
    print('qq_id:', qq_id)
    qq_name = message.author.username
    print(qq_name)
    try:
        steamid = convert_steamid(steamid, "steamid")
    except ValueError:
        await message.reply(content="SteamID格式不正确")
        return
    if update_steamid(steamid, qq_id, qq_name):
        await message.reply(content='绑定成功')
    else:
        await message.reply(content='绑定失败')


class MyClient(botpy.Client):
    async def on_ready(self):
        print(f"robot 「{self.robot.name}」 on_ready!")

    async def on_message_create(self, message: Message, steamid=None, kzmode='kzt'): # NOQA
        commands = ['/wl', '/白名单']
        for command in commands:
            if command in message.content:
                # 分割指令后面的指令参数
                steamid = message.content.split(command)[1].strip()
                await whitelist(message)

        if "/kz" in message.content.lower():
            param = message.content.split('/kz')[1].strip()
            try:
                steamid = qq_to_steamid(message.author.id)
                if steamid is None:
                    await message.reply(content="请先 '/绑定' steamid")
                    return
            except ValueError:
                await message.reply(content="请先 '/绑定' steamid")

            if param is None:
                kzmode = get_kzmode(steamid=steamid)
            await info(message, steamid, mode=kzmode)

        elif '/绑定' in message.content:
            steamid = message.content.split('/绑定')[1].strip()
            await bind_steam(message, steamid)

        elif '/解绑' in message.content:
            qq_id = message.author.id
            print('qq_id:', qq_id)
            reset_steamid_by_qq_id(qq_id)
            await message.reply(content='解绑成功')

        elif '/服务器' in message.content:
            content = query_all_servers_text()
            await message.reply(content=content)

        elif '/setmode' in message.content:
            kzmode = message.content.split('/setmode')[1].strip()
            qq_id = message.author.id
            set_kzmode(qq_id, kzmode)
            pass


if __name__ == "__main__":

    intents = botpy.Intents(guild_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], secret=test_config["secret"])