import os
from dotenv import load_dotenv
import pytz
import mysql.connector
from datetime import datetime, timedelta
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


def create_online_month_table():
    # Establish a connection to the MySQL server
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        # SQL query to create the 'online_month' table
        create_table_query = (
            "CREATE TABLE IF NOT EXISTS online_month ("
            "map_id INT AUTO_INCREMENT PRIMARY KEY,"
            "month_date DATE NOT NULL,"
            "players_online INT NOT NULL,"
            "whitelisted INT NOT NULL,"
            "un_whitelisted INT NOT NULL"
            ")"
        )

        cursor.execute(create_table_query)

        # Commit the changes to the database
        connection.commit()

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()


def players_played_last_month_count():
    # Establish a connection to the MySQL server
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        # Calculate the timestamp for one month ago
        one_month_ago = datetime.now() - timedelta(days=30)
        one_month_ago_timestamp = int(one_month_ago.timestamp())

        # Query to get the count of players who played last month
        last_month_query = (
            "SELECT COUNT(DISTINCT auth) AS total_count "
            "FROM firstjoin "
            "WHERE timestamps >= %s"
        )

        cursor.execute(last_month_query, (one_month_ago_timestamp,))
        total_count = cursor.fetchone()[0] if cursor else 0

        # Query to get the count of whitelisted players who played last month
        whitelisted_query = (
            "SELECT COUNT(DISTINCT auth) AS whitelisted_count "
            "FROM firstjoin "
            "WHERE timestamps >= %s AND whitelist = 1"
        )

        cursor.execute(whitelisted_query, (one_month_ago_timestamp,))
        whitelisted_count = cursor.fetchone()[0] if cursor else 0

        # Calculate un-whitelisted count
        un_whitelisted_count = total_count - whitelisted_count

        return {
            "total": total_count,
            "whitelisted": whitelisted_count,
            "un_whitelisted": un_whitelisted_count
        }

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()


def insert_player_counts_to_table(player_counts):
    # Establish a connection to the MySQL server
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        # Calculate the date for one month ago
        one_month_ago = datetime.now() - timedelta(days=30)
        one_month_ago_str = one_month_ago.strftime('%Y-%m-%d')

        # Insert the player counts into the 'online_month' table
        insert_query = (
            "INSERT INTO firstjoin.online_month (month_date, players_online, whitelisted, un_whitelisted) "
            "VALUES (%s, %s, %s, %s)"
        )

        cursor.execute(insert_query, (
            one_month_ago_str, player_counts['total'], player_counts['whitelisted'], player_counts['un_whitelisted']))

        # Commit the changes to the database
        connection.commit()

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()


def send_discord_webhook(player_counts):
    # Define the embed message payload
    embed_payload = {
        "title": "Last Month's player count",
        "color": 0x00ff00,  # Green color
        "timestamp": str(datetime.now(pytz.timezone("UTC"))),
        "fields": [
            {
                "name": "Total",
                "value": str(player_counts['total']),
                "inline": True
            },
            {
                "name": "Whitelisted",
                "value": str(player_counts['whitelisted']),
                "inline": True
            },
            {
                "name": "Un-whitelisted",
                "value": str(player_counts['un_whitelisted']),
                "inline": True
            }
        ]
    }

    # Create the webhook message payload
    webhook_payload = {
        "embeds": [embed_payload]
    }

    # Send the webhook message to Discord
    response = requests.post(TRENDING_WEBHOOK_URL, data=json.dumps(webhook_payload),
                             headers={"Content-Type": "application/json"})

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        print("Webhook message sent successfully.")
    elif response.status_code == 204:
        print("Webhook message sent successfully.")
    else:
        print(f"Failed to send webhook message. Status code: {response.status_code}")


if __name__ == "__main__":
    create_online_month_table()
    last_month_player_counts = players_played_last_month_count()

    insert_player_counts_to_table(last_month_player_counts)
    # Send a webhook message with player counts
    send_discord_webhook(last_month_player_counts)
