import mysql.connector

from config import db_config
from functions.globalapi.kz_mode import format_kzmode

db_config['database'] = 'discord'


def get_kzmode(qq_id) -> str:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT kz_mode FROM discord.qq WHERE id = %s", (qq_id,))
        result = cursor.fetchone()

        if result:
            return result[0]
        else:
            return 'kzt'

    except mysql.connector.Error as e:
        print(f"MySQL error: {e}")
        return 'kzt'

    finally:
        cursor.close()
        conn.close()


def reset_steamid_by_qq_id(qq_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    try:

        cursor.execute("SELECT steamid FROM discord.qq WHERE id = %s", (qq_id,))
        existing_steamid = cursor.fetchone()

        if existing_steamid:
            # If the QQ ID exists, reset the associated Steam ID to None (or an appropriate default value)
            cursor.execute("UPDATE discord.qq SET steamid = NULL WHERE id = %s", (qq_id,))
            conn.commit()
            return True  # Successfully reset Steam ID
        else:
            return False  # QQ ID not found in the database

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False  # Handle the error gracefully
    finally:
        # Close the cursor and the connection
        cursor.close()
        conn.close()


def qq_to_steamid(qq_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT steamid FROM discord.qq WHERE id = %s", (qq_id,))
        result = cursor.fetchone()
        print(result)
        if result:
            return result[0]  # Return the Steam ID
        else:
            return None  # QQ ID not found in the database

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None  # Handle the error gracefully
    finally:
        # Close the cursor and the connection
        cursor.close()
        conn.close()


def set_kzmode(qq_id, kzmode: str):
    kzmode = format_kzmode(kzmode)
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE discord.qq SET kz_mode = %s WHERE id = %s", (kzmode, qq_id))
        result = cursor.fetchone()
        print(result)
        if result:
            return result[0]  # Return the Steam ID
        else:
            return None  # QQ ID not found in the database

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None  # Handle the error gracefully
    finally:
        # Close the cursor and the connection
        cursor.close()
        conn.close()


def update_steamid(steamid, qq_id, qq_name):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM discord.qq WHERE id = %s", (qq_id,))
        existing_qq_id = cursor.fetchone()

        if existing_qq_id:
            cursor.execute("UPDATE discord.qq SET steamid = %s, username = %s WHERE id = %s", (steamid, qq_name, qq_id))
        else:
            cursor.execute("INSERT INTO discord.qq (steamid, id, username) VALUES (%s, %s, %s)",
                           (steamid, qq_id, qq_name))

        # Commit the changes
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    finally:
        cursor.close()
        conn.close()
