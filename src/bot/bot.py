import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import Intents

# load values from .env file
load_dotenv()
token = os.getenv('TOKEN')

async def send_message(message, user_message, is_private):
    try:
        # Has to be implemented
    except:
        # Has to be implemented