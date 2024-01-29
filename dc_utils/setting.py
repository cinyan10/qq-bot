import mysql.connector
from config import db_config


async def set_language(ctx, lang):
    discord_id = ctx.author.id  # Get the Discord ID of the user
    query = "UPDATE discord.users SET language = %s WHERE discord_id = %s"

    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (lang, discord_id))
                conn.commit()
                await ctx.send(f"Language set to {lang} for user {ctx.author.name}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        await ctx.send("Failed to update language.")


async def set_kz_mode(ctx, kz_mode):
    discord_id = ctx.author.id  # Get the Discord ID of the user
    query = "UPDATE discord.users SET kz_mode = %s WHERE discord_id = %s"

    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (kz_mode, discord_id))
                conn.commit()
                await ctx.send(f"KZ mode set to {kz_mode} for user {ctx.author.name}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        await ctx.send("Failed to update KZ mode.")
