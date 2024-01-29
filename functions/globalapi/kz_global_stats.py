import discord
import requests
from discord import Embed
from config import *
from functions.database import get_steam_user_name
from functions.globalapi.kz_maps import get_map_tier
from functions.globalapi.kz_mode import format_kzmode
from functions.globalapi.maps import Maps
from functions.misc import add_commas, percentage_bar
from functions.steam.steam import convert_steamid, get_steam_pfp, get_steam_profile_url


class KzGlobalStats:
    def __init__(self, steamid64, kzmode="kz_timer"):
        if kzmode:
            kzmode = format_kzmode(kzmode.lower())
        self.maps = Maps(kzmode)

        tp_data = cal_stats(fetch_global_stats(steamid64, kzmode, True))
        pro_data = cal_stats(fetch_global_stats(steamid64, kzmode, False))

        # Steam info
        self.name = get_steam_user_name(convert_steamid(steamid64, "steamid"))
        self.pfp = get_steam_pfp(steamid64)
        self.profile_url = get_steam_profile_url(steamid64)

        # TP Stats
        self.tp_avg_pts = tp_data['avg_pts']
        self.tp_avg_tier_pts = tp_data['avg_tier_pts']
        self.tp_wr = tp_data['wr']
        self.tp_silver = tp_data['silver']
        self.tp_copper = tp_data['copper']
        self.tp_total_pts = tp_data['total_pts']
        self.tp_total_maps = tp_data['total_maps']
        self.tp_tier_maps = tp_data['tier_maps']

        # Pro Stats
        self.pro_avg_pts = pro_data['avg_pts']
        self.pro_avg_tier_pts = pro_data['avg_tier_pts']
        self.pro_wr = pro_data['wr']
        self.pro_silver = pro_data['silver']
        self.pro_copper = pro_data['copper']
        self.pro_total_pts = pro_data['total_pts']
        self.pro_total_maps = pro_data['total_maps']
        self.pro_tier_maps = pro_data['tier_maps']

        # Total Stats
        self.total_pts = self.tp_total_pts + self.pro_total_pts
        try:
            self.total_avg_pts = self.total_pts / (self.tp_total_maps + self.pro_total_maps)
        except ZeroDivisionError:
            self.total_avg_pts = 0

    def __str__(self):
        return self.name

    def embed_stats(self) -> Embed:
        embed = Embed(title=f"{self.name}", url=self.profile_url, colour=discord.Colour.blue())
        embed.set_thumbnail(url=self.pfp)
        embed.description = f"Total: **{add_commas(self.total_pts)}** Avg: **{int(self.total_avg_pts)}**"

        emojis = ["⬛", '🟦', '🟩', '🟨', '🟧', '🟥', '🟪', '⬜']
        # ⬛ ⬜

        tp_content = (f"🥇 {self.tp_wr} 🥈 {self.tp_silver} 🥉 {self.tp_copper} "
                      f"Total:**{add_commas(self.tp_total_pts)}** Avg:**{int(self.tp_avg_pts)}**\n")
        for i in range(1, 8):
            tp_content += f"{percentage_bar(self.tp_tier_maps[i] / self.maps.tier[i], 15, emojis[i], '⬛',
                                            show_percentage=False, show_brackets=False)} "
            tp_content += f"T{i} `{self.tp_tier_maps[i]}/{self.maps.tier[i]}` | `{int(self.tp_avg_tier_pts[i])}`\n"

        embed.add_field(inline=False, name=f"TP Stats", value=tp_content)

        pro_content = (f"🥇 {self.pro_wr} 🥈 {self.pro_silver} 🥉 {self.pro_copper} "
                       f"Total:**{add_commas(self.pro_total_pts)}** Avg:**{int(self.pro_avg_pts)}**\n")
        for i in range(1, 8):
            pro_content += f"{percentage_bar(self.pro_tier_maps[i] / self.maps.tier[i], 15, emojis[i], '⬛',
                                             show_percentage=False, show_brackets=False)} "
            pro_content += f"T{i} `{self.pro_tier_maps[i]}/{self.maps.tier[i]}` | `{int(self.pro_avg_tier_pts[i])}`\n"

        embed.add_field(inline=False, name=f"Pro Stats", value=pro_content)

        return embed

    def is_reach_pts(self) -> bool:
        if self.total_pts > 50000:
            return True
        else:
            return False


def get_stats_embed(steamid64, kzmode):
    return KzGlobalStats(steamid64, kzmode=kzmode).embed_stats()


def fetch_global_stats(steamid64, mode_str, has_tp: bool):
    api_url = (f"{GLOBAL_API_URL}api/v2.0/records/top?&steamid64={steamid64}&tickrate=128&"
               f"stage=0&modes_list_string={mode_str}&limit=10000&has_teleports={has_tp}")
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()

    return data


def cal_stats(data):
    total_points = 0
    total_records = len(data)
    tier_points = {i: 0 for i in range(1, 8)}
    points_count = {
        "total": 0,
        "1000+": 0,
        "900+": 0,
        "800+": 0,
    }
    tier_counts = {i: 0 for i in range(1, 8)}

    for record in data:
        points = record["points"]
        map_id = record["map_id"]
        tier = get_map_tier(map_id=map_id)

        if tier is not None:
            total_points += points
            tier_points[tier] += points

            if points >= 1000:
                points_count["1000+"] += 1
            if 900 <= points < 1000:
                points_count["900+"] += 1
            if 800 <= points < 900:
                points_count["800+"] += 1

            tier_counts[tier] += 1
    try:
        avg_total_points = total_points / total_records
    except ZeroDivisionError:
        avg_total_points = 0
    avg_tier_points = {tier: points / tier_counts[tier] if tier_counts[tier] > 0 else 0 for tier, points in tier_points.items()}  # NOQA

    return {
        "avg_pts": avg_total_points,
        "avg_tier_pts": avg_tier_points,
        "wr": points_count["1000+"],
        "silver": points_count["900+"],
        "copper": points_count["800+"],
        "total_pts": total_points,
        "total_maps": total_records,
        "tier_maps": tier_counts,
    }


def fetch_personal_recent(steamid64, mode, limit):
    mode = format_kzmode(mode)

    if limit > 5:
        limit = 5

    api_url = (f"{GLOBAL_API_URL}api/v2.0/records/top/recent?steamid64={steamid64}"
               f"&modes_list_string={mode}&stage=0&limit={limit}")

    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()
    return data


def fetch_personal_best(steamid64, map_name, mode):
    mode = format_kzmode(mode)

    api_url = (f"{GLOBAL_API_URL}api/v2.0/records/top?steamid64={steamid64}&map_name={map_name}"
               f"&stage=0&modes_list_string={mode}")

    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()

    return data[0]


if __name__ == "__main__":
    rs = fetch_personal_best(STEAMID64, 'kz_lionheart', 'kzt')
    print(rs)
    print(type(rs))
    pass
