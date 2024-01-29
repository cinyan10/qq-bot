from discord import Embed
from valve.source import a2s
from config import SERVER_LIST, MAP_TIERS
from functions.misc import format_seconds
from functions.server import Server


def fetch_online_player(ip: str, port: int) -> tuple:
    try:
        with a2s.ServerQuerier((ip, port)) as server:
            info = server.info()
            return info['player_count'], info['max_players']
    except Exception as e:
        print("Error fetching online player: ", e)


if __name__ == "__main__":
    s = SERVER_LIST[0]
    print(type(s.ip), type(s.port))
    rs = fetch_online_player(s.ip, s.port)
    print(rs)
    pass


def query_all_servers() -> str:
    info_data = ''
    for s in SERVER_LIST:
        info_data += query_server_simple(s)

    return info_data


def query_server_simple(server):  # NOQA
    try:
        with a2s.ServerQuerier((server.ip, server.port)) as s:
            info = s.info()
            players = s.players()
            try:
                tier = MAP_TIERS[info['map']]
            except Exception:
                tier = 'T0'
        content = (f"[**AXE GOKZ {server.name_short[:2]}#{server.name_short[2]}**](http://redirect.axekz.com/{server.id}):  "
                   f"*{info['map']}* "
                   f'**T{tier}**  '
                   f"{info['player_count']}/{info['max_players']}\n")

        if players:
            players_str = ''
            for player in players['players']:
                content += f"`{player['name'].replace('`', '')}`  "
                players_str += f"`{player['name']}`"
            if players_str != '':
                content += "\n"
        return content
    except Exception as e:
        print(f"Error: {e}")
        return ""


def query_server_details(server: Server) -> str:  # NOQA
    try:
        with a2s.ServerQuerier((server.ip, server.port)) as s:
            info = s.info()
            players = s.players()
            try:
                tier = MAP_TIERS[info['map']]
            except Exception:
                tier = 'T0'

        content = (f"Server: {info['server_name']}"
                   f"\nMap: {info['map']} T{tier}"
                   f"\nPlayers: {info['player_count']}/{info['max_players']}")
        if players:
            content += "\nPlayer List:"
            for player in players['players']:
                content += f"\n{player['name']}\t - Time: {format_seconds(player['duration'])}"

        return content
    except Exception as e:
        print(f"Error: {e}")


async def query_server_embed(server: Server, bot=None) -> Embed:
    try:
        with a2s.ServerQuerier((server.ip, server.port)) as s:
            info = s.info()
            players = s.players()
            try:
                tier = MAP_TIERS[info['map']]
            except Exception:
                tier = 'T0'

            players_str = ''
            for player in players['players']:
                players_str += f"\n{player['name']} - {format_seconds(player['duration'])}"

            embed = Embed(
                title=f'{info['map']} - T{tier}',
                description=players_str,
                color=0x58b9ff,
            )

            embed.set_author(name=f"{info['server_name']}    {info['player_count']}/{info['max_players']}")
            embed.url = f'http://redirect.axekz.com/{server.id}'
            embed.set_image(url=f"https://raw.githubusercontent.com/KZGlobalTeam/map-images/master/images/{info['map']}.jpg")

            # edit channel name
            if bot:
                channel = bot.get_channel(server.channel_id)
                await channel.edit(name=f"{server.name_short}│{info['player_count']}／{info['max_players']}│{info['map'][3:]}")

            return embed
    except Exception as e:
        print(f"Error: {e}")
        return Embed(title="Error")
