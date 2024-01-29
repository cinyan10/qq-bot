import mysql.connector
from config import *
from functions.steam.steam import convert_steamid


def get_kzmode(discord_id=None, steamid=None):

    cursor = None
    conn = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        if discord_id:
            cursor.execute("SELECT kz_mode FROM discord.users WHERE discord_id = %s", (discord_id,))
        else:
            steamid = convert_steamid(steamid, "steamid64")
            cursor.execute("SELECT kz_mode FROM discord.users WHERE steamid = %s", (steamid,))
        result = cursor.fetchone()

        if result:
            return result[0]
        else:
            return None

    except mysql.connector.Error as e:
        print(f"MySQL error: {e}")
        return None

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    pass
