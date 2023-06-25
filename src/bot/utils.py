#This file is to store the funtions I am creating to process the bot responses
import sqlite3
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import discord
import datetime

# Starting APSCHEDULER
scheduler = AsyncIOScheduler()
scheduler.start()

"""" Creating the SQLite Database"""
def create_database():
    #Installing SQLlite and connecting to the server. 
    conn = sqlite3.connect('announceac.db')
    #Conencting to a cursor to interact with the server.
    c = conn.cursor()

    #Here, I'm creating a SQLite table with the needed columns to manage the group info. 
    #If the table alreadly exists, then this query does nothing really.
    c.execute("""CREATE TABLE IF NOT EXISTS groupinfo (server_id TEXT PRIMARY KEY,  meeting_time TEXT, contact_info TEXT )""")
        # Explaination of some concepts:
            # 1. "Text" is simply a datatype that I am setting as a contraint for column values
            # 2. PRIMARY KEY is the identifier variable for the table. Each rows primary key must be unqiue.
            # 3. Primary keys create a searcg index for the column (which I'm going to use).
    # Saving the database by committing:
    conn.commit()
    conn.close()

""" Setting the group information."""
def set_group_info(server_id, meeting_time, contact_info):
    conn = sqlite3.connect('announceac.db')
    c = conn.cursor
    # Here, I'm adding or replacing Announce ase data based on the server information given.
        # The datatype constraints have already been set so I'm not explicitly stating them again.
    c.execute("INSERT OR REPLACE INTO groupinfo (server_id, meeting_time, contact_info) VALUES (?, ?, ?)",(server_id, meeting_time, contact_info) )
    # Saving changes:
    conn.commit()
    conn.close()

""" Retriving the group information """
# Bceause server_id is the Primary key, I'm using it as the index to search and retiereve group data.
def get_group_info(server_id):
    conn = sqlite3.connect('announceace.db')
    c = conn.cursor
    # Selecting the needed data from the groupinfo table. Im using the ? as a placeholder for the actual server_id.
    c.execute("SELECT meeting_time, contact_info FROM groupinfo WHERE server_id=?", (server_id,))
    # Geting the results of the groupinfo query
    info = c.fetchone()
    conn.close()
    conn.commit()

    # Returning the needed info.
    return info


""" Creaitng announcements table """
def create_message_table():
    # Connecting to SQlite database (if it doesn't exit then it's also creating one)
    conn = sqlite3.connect("announceace_messages.db")
    c = conn.cursor()

    # Here, I'm creating the announcments database.
    c.execute(""" CREATE TABLE IF NOT EXISTS announcements
             (annoucement_id INTEGER PRIMARY KEY , channel_id TEXT, announcement TEXT, scheduled_time DATETIME)""")
    conn.commit()
    conn.close()

#Send announcement has to be an async def so that the bot can do it simulatenously without waiting for the entire program.
# It also saves me time from constantly saying "await.channel.send(message) in the main bot code"
async def send_announcement(channel, announcement):
    # Personal explanaiton of this: Await is used before calling an asynchronous function to wait for it to complete. 
    # channel.send is an asynchronous function provided by the discord library that sends the announcement to a channel. 
    # Await ensures that the announcement is sent before the function continues.
    await channel.send(announcement)


""" Scheduling announcements """
def schedule_announcement(channel_id, announcement, scheduled_time):

    # I'm using the APScheduler module to send announcements here.
    # The "send" function will be called at whatever time is the scheduled datetime.
    job = scheduler.add_job(send_announcement, 'date', run_date = scheduled_time, args=(channel_id, announcement))

    #Saving the details of the message in the SQlite3 database.
    conn = sqlite3.connect("announceace_messages.db")
    c = conn.cursor()

    # Here, I'm creating the announcments database.
    c.execute("INSERT INTO announcements (channel_id, announcement, scheduled_time) VALUES (?, ?, ?)", (channel_id, announcement, scheduled_time))
    conn.commit()
    conn.close()

""" Getting upcoming announcements"""
def upcoming_announcements():
    # Connecting to the sql database
    conn = sqlite3.connect("announceace_messages.db")
    c = conn.cursor()

    # I'm selecting all of the data from announcements where the schdules time is greater than the current datetime.
    c.execute("SELECT * FROM announcements WHERE scheduled_time > ?", (datetime.now(),) )
    upcoming = c.fetchall()
    conn.commit()
    conn.close()
    return upcoming

""" Cancelling upcoming announcements"""
def cancel_announcements(announcement_id):
    # Remove the scheduled job with the given message_id from APScheduler.
    scheduler.remove_job(announcement_id)

    #Connecting to SQL
    conn = sqlite3.connect("announceace_messages.db")
    c = conn.cursor

    # Using the message id as the index to determine which message should be deleted
    c.execute("DELETE FROM announcements WHERE announcement_id=?", (announcement_id,))
    conn.commit()
    conn.close()

if __name__ == "___main__":
    create_database()
    scheduler.start()