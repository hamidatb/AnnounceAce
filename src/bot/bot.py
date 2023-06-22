import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import Intents

# load values from .env file
load_dotenv()
token = os.getenv('TOKEN')

intents = Intents.default()
intents.messages = True
intents.guilds = True
intents.guild_messages = True
intents.typing = False
intents.presences = False

# Change client to use bot with command_prefix
bot = commands.Bot(command_prefix="$Ace ", intents=intents)

@bot.event
# Events that occur must be initialized
async def on_ready():
    print(f"AnnounceAce has logged in as {bot.user}")

@bot.event
# This event is to find out why an error happened if one occurred.
async def on_error(event, *args, **kwargs):
    import traceback
    print("An error has occurred: ", traceback.format_exc())

# Using commands instead of on_message
@bot.command(name='shutdown')
async def shutdown(ctx):
    await ctx.send("Shutting down...")
    await bot.close()

@bot.command(name='hello')
async def hello(ctx):
    await ctx.send("Hello!")

# Use bot.run instead of client.run
bot.run(token)
