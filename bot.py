import discord
from discord.ext import tasks, commands
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

last_id = 0  # Initialize the last checked ID

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")
    check_new_entries.start()

@tasks.loop(seconds=30)
async def check_new_entries():
    global last_id  # Access the global variable to keep track of the last id

    try:
        db = mysql.connector.connect(
            host="127.0.0.1",
            user="u547027111_konsultacijas",
            password="K0nsult@@c1j@S",
            database="u547027111_kons"
        )
        cursor = db.cursor(dictionary=True)
        
        # Get the most recent entry
        cursor.execute("SELECT id FROM aparatura ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        
        if row:
            current_id = row['id']  # Get the latest entry ID

            if current_id > last_id:  # If there's a new entry
                last_id = current_id  # Update last_id to the new entry's ID
                channel = bot.get_channel(1363590543631716512)  # Replace with your channel ID
                await channel.send("🚨 Jauns pieteikums!! Apskati Administrācijas lapu!")
        
        cursor.close()
        db.close()
    except Exception as e:
        print("Error checking DB:", e)

bot.run(TOKEN)
