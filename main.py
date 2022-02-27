import discord
import os

import random
from replit import db
from alive import keep_alive

os.environ['bot_pass']
client = discord.Client()

college_tips = ["college", "major", "rich", "wealth", "future"]

links = [
    'https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors',
    'https://www.businessinsider.com/personal-finance/interviewed-150-millionaires-isolated-common-patterns-habits',
    'https://www.forbes.com/sites/mattdurot/2021/10/08/want-to-be-a-billionaire-these-are-the-most-popular-majors-of-the-richest-americans/?sh=57bfc13526ef',
    'https://www.salary.com/articles/8-college-degrees-with-the-worst-return-on-investment/'
]

if "responding" not in db.keys():
    db["responding"] = True


def update_college_tips(college_tips_plus):
    if "college_tip" in db.keys():
        college_tip = db["college_tip"]
        college_tip.append(college_tips_plus)
        db["college_tip"] = college_tip
    else:
        db["college_tip"] = [college_tips_plus]


def delete_college_tips(index):
    college_tip = db['college_tip']
    if len(college_tip) > index:
        del college_tip[index]
        db["college_tip"] = college_tip


@client.event
async def on_ready():
    print('We have logged in as {0.user} '.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('$college'):
        await message.channel.send(
            'https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors'
        )

    if db["responding"]:
        options = links
        if "college_tip" in db.keys():
            options.extend(db["college_tip"])

        if any(word in msg for word in college_tips):
            await message.channel.send(random.choice(options))

    if msg.startswith("$new"):
        college_tip_plus = msg.split("$new ",1)[1]
        update_college_tips(college_tip_plus)
        await message.channel.send("New encouraging message added.")

    if msg.startswith("$del"):

        college_tip = []
        if "college_tip" in db.keys():
            index = int(msg.split("$del",1)[1])
            delete_college_tips(index)
            college_tip = db["college_tip"]
        await message.channel.send(college_tip)

    if msg.startswith("$list"):
        college_tip = []
        if "college_tip" in db.keys():
            college_tip = db["college_tip"]
        await message.channel.send(college_tip)

    if msg.startswith("$responding"):
        value = msg.split("$responding ",1)[1]

        if value.lower() == "true":
            db["responding"] = True
            await message.channel.send("Responding is on.")
        else:
            db["responding"] = False
            await message.channel.send("Responding is off.")

keep_alive()
client.run(os.environ['bot_pass'])
