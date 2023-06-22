import os
from dotenv import load_dotenv
import discord
from discord import Intents

# load values from .env file
load_dotenv()
token = os.getenv('TOKEN')

intents = Intents.default()
intents.messages = True
intents.typing = False
intents.presences = False

client = discord.Client(intents=intents)

@client.event
# Events that occur must be initialized
async def on_ready():
    print("AnnounceAce has logged in as {0.user}".format(client))

@client.event
# This event is to find out why an error happened if one occurred.
async def on_error(event, *args, **kwargs):
    import traceback
    print("An error has occurred: ", traceback.format_exc())

@client.event
async def on_message(message):
    if message.author == client.user:
        # If the message author is AnnounceAce itself, ignore the message.
        return

    msg_content = message.content.strip()
    print(f"Message received from {message.author}: {msg_content}")

    if msg_content == "$Ace shutdown":
        await message.channel.send("Shutting down...")
        await client.close()
    elif msg_content.startswith("$Ace"):
        await message.channel.send("Hello!")

client.run(os.getenv("TOKEN"))