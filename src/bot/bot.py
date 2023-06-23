import os
from dotenv import load_dotenv
import discord
import responses


def run_discord_bot():
    load_dotenv()
    token = os.getenv('TOKEN')
    intents = discord.Intents.default()
    intents.messages = True  # Enable messages
    intents.message_content = True  # Enable message content
    client = discord.Client(intents=intents)  # Pass intents as a keyword argument

    @client.event
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
        
        # If the message starts with a ?, respond to the user in private
        if user_message.startswith("?"):
            user_message = user_message[1:]
            await send_response(message, user_message, is_private=True)

        # If the message starts with a &, respond to the user in the public channel in which the message was sent.
        elif user_message.startswith("&"):
            user_message = user_message[1:]
            await send_response(message, user_message, is_private=False)

        #If the message does not start with either & or ?, AnnounceAce will ignore it.
    client.run(token)


async def send_response(message, user_message, is_private):
    try:
        response = responses.get_responses(user_message)
        # Send the message directly to the author if it is a private message, otherwise send publicly in the channel.
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as error:
        print(error)


if __name__ == '__main__':
    run_discord_bot()