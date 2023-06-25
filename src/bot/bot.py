import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import utils

load_dotenv()
token = os.getenv('TOKEN')
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)  # Using "!" as the command prefix.

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")

@bot.command(name='hello')
async def hello(ctx):
    await ctx.send("Hello!")

@bot.command(name='private')
async def private_message(ctx, *, message):
    await ctx.author.send(message)

@bot.command(name='public')
async def public_message(ctx, *, message):
    await ctx.send(message)


@bot.command(name='features')
async def explain_features(ctx):
    await ctx.send(" Hi! Thanks for installing Announce Ace! \n Here are my features: ")
    #Fill this in more later.

bot.run(token)