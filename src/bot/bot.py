import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import utils 
from datetime import datetime

load_dotenv()
token = os.getenv('TOKEN')
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)  # Using "!" as the command prefix.

# Call the functions from utils to create the database and message table
utils.create_database()
utils.create_message_table()


""" Making sure the bot is running as expected. """
@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")

""" AnnounceAce will say hello if it's said to it first """
@bot.command(name='Hello' or 'hello')
async def hello(ctx):
    await ctx.send("Hello!")

""" Reply to the message in private if wanted """
@bot.command(name='private')
async def private_message(ctx, *, message):
    await ctx.author.send(message)

""" Reply to the message publically in the current channel if wanted"""
@bot.command(name='public')
async def public_message(ctx, *, message):
    await ctx.send(message)


""" Scheduling a message """
@bot.command(name='schedule')
# I want the user to be able to schdule an announcement like:
# "!schedule 06-30-2023 12:00 This is a scheduled announcement!"
async def schedule_announcement(ctx, date: str, time: str, *, announcement: str):
    try:
    # Combining the date and time into one string, and converting it into a date-time format that Python can understand.
        scheduled_time_str = f"{date} {time}:00"
        # Converting the string to a Python datetime object
        scheduled_time = datetime.strptime(scheduled_time_str, "%m-%d-%Y %H:%M:%S")
        # Grabbing the ID of the channel where the command was used, so we know where to send the announcement.
        channel_id = ctx.channel.id

        # This is where I'm calling the 'schedule_announcement' function from the utils module to actually schedule the announcement.
        # We pass it the channel ID, the announcement text, and the time we want it to go out.
        utils.schedule_announcement(channel_id, announcement, scheduled_time)
        
        # Telling the user that their announcement was scheduled successfully
        await ctx.send("Announcement scheduled successfully for {} at {}!".format(date, time))
    # 'except' means: if there was any error in the 'try' part, do this instead
    except Exception as e:
        # Telling the user that something went wrong, and giving them some information on what might have caused the error.
        await ctx.send(f"Error scheduling announcement. Make sure the date is in MM-DD-YYYY format and time in 24-hour format HH:MM. Error details: {str(e)}")

bot.run(token)

