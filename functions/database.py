import mysql.connector
from datetime import timedelta

from config import *
from functions.globalapi.kzgoeu import get_kzgoeu_profile_url
from functions.steam.steam import convert_steamid

# Global constants
db_config = {
    'user': DB_USER,
    'password': DB_PASSWORD,
    'host': DB_HOST,
    'database': 'gokz',
    'raise_on_warnings': True,
    'port': DB_PORT,
}

KZ_MODES = {'kzt': 2, 'skz': 1, 'vnl': 0}


# Database utility function
def execute_query(query, params=(), fetch_one=False, commit=False):
    with mysql.connector.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            if commit:
                conn.commit()
                return
            return cursor.fetchone() if fetch_one else cursor.fetchall()


# Function definitions
def get_country_from_steamid32(steamid32):
    query = "SELECT country FROM gokz.Players WHERE steamid32 = %s"
    result = execute_query(query, (steamid32,), fetch_one=True)
    return result[0] if result else None


def discord_id_to_steamid(discord_id):
    query = 'SELECT steamid FROM discord.users WHERE discord_id = %s'
    result = execute_query(query, (discord_id,), fetch_one=True)
    return result[0] if result else None


def retrieve_join_date(steam_id):
    query = 'SELECT joindate FROM firstjoin.firstjoin WHERE auth = %s'
    result = execute_query(query, (steam_id,), fetch_one=True)
    return result[0] if result else None


def retrieve_last_seen(steam_id):
    query = 'SELECT lastseen FROM firstjoin.firstjoin WHERE auth = %s'
    result = execute_query(query, (steam_id,), fetch_one=True)
    return result[0] if result else None


def reset_user_steam(discord_id):
    update_query = 'UPDATE discord.users SET steamid = NULL, steamid32 = NULL, steamid = NULL WHERE discord_id = %s'
    execute_query(update_query, (discord_id,), commit=True)


def get_steam_user_name(steamid):
    query = 'SELECT name FROM firstjoin.firstjoin WHERE auth = %s'
    result = execute_query(query, (steamid,), fetch_one=True)
    return result[0] if result else None


def query_jumpstats_top(limit: int = 10, mode: str = 'kzt') -> str:
    # Establish a database connection
    conn = mysql.connector.connect(**db_config)

    # Prepare the SQL query
    query = f'''
    SELECT j.SteamID32, MAX(j.Distance) as MaxDistance
    FROM Jumpstats j
    JOIN Players p ON j.SteamID32 = p.SteamID32
    WHERE j.JumpType = 0 AND j.Mode = {KZ_MODES[mode]} AND p.Cheater != 1
    GROUP BY j.SteamID32
    ORDER BY MaxDistance DESC
    LIMIT {limit}
    '''

    # Execute the query
    cursor = conn.cursor()
    cursor.execute(query)

    # Fetch the results
    rows = cursor.fetchall()

    # Process the results
    result = ''
    rank = 1
    for steamid32, distance in rows:
        steamid = convert_steamid(steamid32, 'steamid')
        kzgoeu_url = get_kzgoeu_profile_url(steamid, mode)
        name = get_steam_user_name(steamid)
        formatted_distance = distance / 10000  # Convert distance to float with four decimal places
        result += f'[{rank}. {name}]({kzgoeu_url}) - {formatted_distance:.4f}\n'
        rank += 1

    # Close the cursor and connection
    cursor.close()
    conn.close()
    return result


def cal_playtime(steamid32):
    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Prepare the SQL query to sum all runtimes for a given SteamID32
    query = '''
    SELECT SUM(Runtime)
    FROM Times
    WHERE SteamID32 = %s
    '''

    # Execute the query
    cursor.execute(query, (steamid32,))

    # Fetch the result
    result = cursor.fetchone()
    total_runtime_milliseconds = int(result[0]) if result[0] is not None else 0

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Convert the total runtime from milliseconds to a timedelta object
    total_runtime = timedelta(milliseconds=total_runtime_milliseconds)

    # Format the timedelta to a string in the format of hours:minutes:seconds
    # Note: This will only show the hours contained in one day if you have more than 24 hours of playtime
    total_hours = total_runtime.days * 24 + total_runtime.seconds // 3600
    total_minutes = (total_runtime.seconds // 60) % 60
    total_seconds = total_runtime.seconds % 60

    return total_hours, total_minutes, total_seconds


if __name__ == "__main__":
    rs = cal_playtime(STEAMID32)
    print(rs[0], rs[1], rs[2])
