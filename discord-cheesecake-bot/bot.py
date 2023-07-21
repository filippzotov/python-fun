import os
import discord
from token_file import TOKEN
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=".", intents=intents)


@bot.event
async def on_ready():
    print("The bot has logged in!")  # outputs to local command line
    server = bot.guilds[0]  # gets your server
    first_channel = server.text_channels[0]  # gets first text channel
    await first_channel.send("Hello, World!")  # outputs to Discord


@bot.event
async def on_guild_available(guild):
    await asyncio.sleep(
        2
    )  # Adjust the delay time if needed to ensure members are fetched properly
    member_list = []

    for member in guild.members:
        member_list.append(f"{member.name}#{member.discriminator} (ID: {member.id})")

    members_info = "\n".join(member_list)
    print(f'Members in the server "{guild.name}":\n{members_info}')
    print(guild.id)


bot.run(TOKEN)
