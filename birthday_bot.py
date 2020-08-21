import asyncio
import datetime
import json
import os
from discord.ext.commands import Bot
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

BOT_PREFIX = ("!")
bot = Bot(command_prefix=BOT_PREFIX)

@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")
    bot.loop.create_task(birthday_task())

async def birthday_task():
    next_check_date = datetime.datetime.today().strftime("%m/%d")  # Initialized to today's date so we can check for birthdays the same day we first run the bot
    while True:
        todays_date = datetime.datetime.today().strftime("%m/%d")
        if todays_date == next_check_date:
            next_check_date = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime("%m/%d")

            birthday_members = get_birthday_members(todays_date)
            if len(birthday_members) != 0:
                birthday_message = create_birthday_message(birthday_members)
                CHANNEL_ID = "XXXXXXX"
                await bot.get_channel(CHANNEL_ID).send(birthday_message)

        await asyncio.sleep(3600)

def get_birthday_members(todays_date):
    with open("birthdays.json") as f:
        birthday_data = json.load(f)

    birthday_members = []
    for birthday in birthday_data['birthdays']:
        if birthday['date'] == todays_date:
            birthday_members = birthday['people']

    return birthday_members

def create_birthday_message(birthday_members):
    member_ids = []
    for member in birthday_members:
        member_id = member['id']
        member_ids.append("<@" + str(member_id) + ">")

    happy_birthday_mention = "Happy birthday "
    if len(member_ids) == 1:
        happy_birthday_mention += member_ids[0]
    elif len(member_ids) == 2:
        happy_birthday_mention += " and ".join(member_ids)
    else:
        happy_birthday_mention += ", ".join(member_ids[:-1]) + ", and " + member_ids[-1]
    happy_birthday_mention += "!"
    return happy_birthday_mention

bot.run(TOKEN)