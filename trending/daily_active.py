import os

import pytz
from dotenv import load_dotenv
import mysql.connector
from datetime import datetime, timedelta, date
import requests
import json

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
TRENDING_WEBHOOK_URL = os.getenv('TRENDING_WEBHOOK_URL')

# Define your database configuration and webhook URL
db_config = {
            'user': DB_USER,
            'password': DB_PASSWORD,
            'host': DB_HOST,
            'port': int(DB_PORT),
            'database': 'firstjoin',
        }


def total_players_count() -> dict:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    try:
        # Query to count total players
        total_players_query = (
            "SELECT COUNT(*) AS total FROM firstjoin.firstjoin"
        )
        cursor.execute(total_players_query)
        total_players = cursor.fetchone()[0]

        # Query to count whitelisted players
        whitelisted_query = (
            "SELECT COUNT(*) AS total_whitelisted FROM firstjoin.firstjoin WHERE whitelist = 1"
        )
        cursor.execute(whitelisted_query)
        total_whitelisted = cursor.fetchone()[0]

        # Calculate un-whitelisted players
        total_un_whitelisted = total_players - total_whitelisted

        return {
            "total_players": total_players,
            "total_whitelisted": total_whitelisted,
            "total_un_whitelisted": total_un_whitelisted,
        }

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {
            "total_players": 0,
            "total_whitelisted": 0,
            "total_un_whitelisted": 0,
        }

    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()


def day_players_count() -> dict:
    # Establish a connection to the MySQL server
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    try:
        # Calculate the date one day ago
        one_day_ago_timestamp = int((datetime.now() - timedelta(days=1)).timestamp())
        # Query to get the total online players count
        total_online_query = (
            "SELECT COUNT(*) AS day_players FROM firstjoin WHERE timestamps >= %s"
        )
        cursor.execute(total_online_query, (one_day_ago_timestamp,))
        day_players = cursor.fetchone()[0]

        # Query to get whitelisted players count
        whitelisted_query = (
            "SELECT COUNT(*) AS whitelisted FROM firstjoin WHERE timestamps >= %s AND whitelist = 1"
        )
        cursor.execute(whitelisted_query, (one_day_ago_timestamp,))
        whitelisted = cursor.fetchone()[0]

        # Query to get un-whitelisted players count
        un_whitelisted = (
            "SELECT COUNT(*) AS un_whitelisted FROM firstjoin WHERE timestamps >= %s AND whitelist = 0"
        )
        cursor.execute(un_whitelisted, (one_day_ago_timestamp,))
        un_whitelisted_players = cursor.fetchone()[0]

        return {
            "day_players": day_players or 0,
            "whitelisted": whitelisted or 0,
            "un_whitelisted": un_whitelisted_players or 0,
        }
    finally:
        cursor.close()
        conn.close()


def insert_player_counts_to_table(day_players, total_players):
    # Establish a connection to the MySQL server
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    try:
        # Calculate the date for today
        yesterday = datetime.now() - timedelta(days=1)
        current_date = yesterday.strftime('%Y-%m-%d')

        # Insert the player counts into the 'online_day' table
        # `date`	day_players	day_whitelisted	day_un_whitelisted	total_players	total_whitelisted	total_un_whitelisted
        insert_query = (
            "INSERT INTO online_day (date, day_players, day_whitelisted, day_un_whitelisted, total_players, total_whitelisted, total_un_whitelisted) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        )
        cursor.execute(insert_query, (current_date, day_players['day_players'], day_players['whitelisted'], day_players['un_whitelisted'], total_players['total_players'], total_players['total_whitelisted'], total_players['total_un_whitelisted']))

        # Commit the changes to the database
        conn.commit()

    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()


def differ_yesterday(players_count, total_players):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    try:
        # Calculate the date for yesterday
        yesterday = datetime.now() - timedelta(days=2)
        yesterday_date = yesterday.strftime('%Y-%m-%d')

        # Query to get yesterday's data
        yesterday_data_query = (
            "SELECT day_players, day_whitelisted, total_players "
            "FROM online_day "
            "WHERE date = %s"
        )
        cursor.execute(yesterday_data_query, (yesterday_date,))
        yesterday_data = cursor.fetchone()

        if yesterday_data:
            day_players = yesterday_data[0]
            day_whitelisted = yesterday_data[1]
            total_whitelisted = yesterday_data[2]

            # Calculate the differences
            day_players_difference = players_count['day_players'] - day_players
            day_whitelisted_difference = players_count['whitelisted'] - day_whitelisted
            total_difference = total_players['total_players'] - total_whitelisted

            return [day_players_difference, day_whitelisted_difference, total_difference]

        else:
            print("No data found for yesterday.")
            return []

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

    finally:
        cursor.close()
        conn.close()


def send_discord_webhook(player_counts, total_count, differs) -> None:
    # Define the embed message payload
    yesterday = date.today() - timedelta(days=1)
    embed_payload = {
        "title": f"{yesterday} Player Count",
        "color": 0x60FFFF,  # Green color
        "timestamp": str(datetime.now(pytz.timezone("UTC"))),
        "fields": [
            {
                "name": "Active Player",
                "value": f"**{player_counts['day_players']}** ({'+' if differs[0] > 0 else ''}{differs[0]})",
                "inline": True
            },
            {
                "name": "WL Player",
                "value": f"**{player_counts['whitelisted']}** ({'+' if differs[1] > 0 else ''}{differs[1]})",
                "inline": True
            },
            {
                "name": "Total Player",
                "value": f"**{total_count['total_players']}** ({'+' if differs[2] > 0 else ''}{differs[2]})",
                "inline": True
            },
        ]
    }

    # Create the webhook message payload
    webhook_payload = {
        "embeds": [embed_payload]
    }

    # Send the webhook message to Discord
    response = requests.post(TRENDING_WEBHOOK_URL, data=json.dumps(webhook_payload), headers={"Content-Type": "application/json"})

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        print("Webhook message sent successfully.")
    elif response.status_code == 204:
        print("Webhook message sent successfully.")
    else:
        print(f"Failed to send webhook message. Status code: {response.status_code}")


if __name__ == "__main__":
    players_count = day_players_count()
    total_count = total_players_count()
    insert_player_counts_to_table(players_count, total_count)
    differs = differ_yesterday(players_count, total_count)
    send_discord_webhook(players_count, total_count, differs)
