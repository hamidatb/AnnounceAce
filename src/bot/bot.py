import os
from dotenv import load_dotenv
import discord
import responses

# load values from .env file
load_dotenv()
token = os.getenv('TOKEN')

def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = Trueclient = discord.Client(intents)

    @client.event
    #This triggers everytime this code is ran, and lets you know that the bot is ready to be used on the server.
    async def on_ready():
        print("AnnounceAce has logged in as {0.user}".format(client))
    
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return



async def send_message(message, user_message, is_private):
    try:
        response = responses.get_responses(user_message)
        
        #Send the message directly to the author if it is a private message, otherwise send publically in the channel.
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as error:
        print(error)


