import os
from dotenv import load_dotenv
import discord
import responses


def run_discord_bot():
    load_dotenv()
    token = os.getenv('TOKEN')
    
    intents = discord.Intents.default()
    intents.messages = True  # Enable messages
    
    client = discord.Client(intents=intents)  # Pass intents as a keyword argument

    @client.event
    #This triggers everytime this code is ran, and lets you know that the bot is ready to be used on the server.
    async def on_ready():
        print("AnnounceAce has logged in as {0.user}".format(client))
    
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} said: '{user_message}' ({channel})")
        
        #This means it removes the question mark at the start of the message sent in private so that it processes the string normally.
        if user_message [0] == "?":
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    client.run(token)

async def send_message(message, user_message, is_private):
    try:
        response = responses.get_responses(user_message)
        
        #Send the message directly to the author if it is a private message, otherwise send publically in the channel.
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as error:
        print(error)

# This is important to make sure that you're running the code in the correct file.
if __name__ == '__main__':
    run_discord_bot()
