import os
import discord
from token_file import TOKEN
from discord.ext import commands
import asyncio
import db_logic as db


import games.slots as slot_game

intents = discord.Intents.all()
intents.members = True
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print("The bot has logged in!")  # outputs to local command line
    server = bot.guilds[0]  # gets your server
    first_channel = server.text_channels[0]  # gets first text channel
    await first_channel.send("!ping")  # outputs to Discord


@bot.event
async def on_guild_available(guild):
    await asyncio.sleep(
        2
    )  # Adjust the delay time if needed to ensure members are fetched properly

    server_db = db.server_exists(session, guild.id)
    if not server_db:
        server_db = db.add_server(session, guild.id)
        print(server_db)
        for member in guild.members:
            print(member.name)

            db.add_user(session, member.id, member.name, server_db)


# @bot.event
# async def on_message(message):
#     print(message.content)
#     print(message.author)
#     server = bot.guilds[0]  # gets your server

#     first_channel = server.text_channels[0]  # gets first text channel


@bot.command()
async def ping(ctx):
    print("ping")
    await ctx.send("Pong!")  # Responds with "Pong!" when the command !ping is used


@bot.command()
async def hello(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    await ctx.send(f"Hello, {member.mention}!")


@bot.command()
async def balance(ctx):
    balance = db.get_balance(session, ctx.author.id, ctx.guild.id)
    embed = discord.Embed(colour=discord.Colour.green())
    embed.set_author(name=f"{ctx.author.name} balance: {balance} 🍰")
    await ctx.send(embed=embed)


@bot.command()
async def daily(ctx):
    new_balance = db.update_balance(session, ctx.author.id, ctx.guild.id, 1000)
    await ctx.send(
        f"{ctx.author.mention}\nDaily reward received! You've got {new_balance}🍰"
    )


@bot.command()
async def slots(ctx):
    balance = db.get_balance(session, ctx.author.id, ctx.guild.id)
    if balance - 100 < 0:
        await ctx.send(f"{ctx.author.mention}\nYou are broke🍰")
    else:
        game = slot_game.SlotMachine()
        result = game.roll_machine()
        slot_image = ""
        reward = result[0]
        for line in result[1]:
            slot_image += f"|{line[0]}|{line[1]}|{line[2]}|\n"
        if not reward:
            await ctx.send(
                f"{ctx.author.mention}\nYou spining slots for 100🍰...\nYou lost 100🍰\n"
                + slot_image
            )
            reward -= 100
        else:
            await ctx.send(
                f"{ctx.author.mention}\nYou spining slots for 100🍰...\nYou win {result[0]}🍰\n"
                + slot_image
            )
        db.update_balance(session, ctx.author.id, ctx.guild.id, reward)


session = db.connect_db()
bot.run(TOKEN)
