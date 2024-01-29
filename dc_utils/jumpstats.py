from discord import Embed
from config import *
from functions.db_operate.db_gokz import get_ljpb, get_jspb

from functions.steam.steam import convert_steamid
from functions.steam.steam_embed import steam_embed


def embed_ljpb(kz_mode, steamid, is_block_jump) -> Embed:
    steamid32 = convert_steamid(steamid, 'steamid32')
    ljpb_data: dict = get_ljpb(steamid32, kz_mode, is_block_jump, 0)

    if is_block_jump:
        title = f'LJPB: {ljpb_data['Block']} Block Jump'
    else:
        title = f'LJPB: {ljpb_data['Distance']}'
    ljpb_embed = steam_embed(steamid, title=title)

    for key in JUMPSTATS:
        ljpb_embed.add_field(name=key, value=ljpb_data[key], inline=True)

    return ljpb_embed


def embed_jspb(kz_mode: str, steamid) -> Embed:
    steamid32 = convert_steamid(steamid, 'steamid32')
    jspb_data: dict = get_jspb(steamid32, kz_mode)

    title = f'Jump Stats: {kz_mode.upper()}'
    jspb_embed = steam_embed(steamid, title=title)
    for jump_type, dist in jspb_data.items():
        jspb_embed.add_field(name=JUMP_TYPE[jump_type], value=dist / 10000.0, inline=True)

    return jspb_embed


if __name__ == '__main__':
    pass
