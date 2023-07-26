import discord
from token_file import TOKEN
from discord.ext import commands
import asyncio
import db_logic as db
import random
import games.slots as slot_game

intents = discord.Intents.all()
intents.members = True
intents.messages = True
bot = commands.Bot(command_prefix="c!", intents=intents)
bot.remove_command("help")


@bot.event
async def on_ready():
    await bot.load_extension("cogs.music_cog")
    await bot.load_extension("cogs.help_cog")
    await bot.load_extension("cogs.roulette_cog")
    print("The bot has logged in!")  # outputs to local command line


@bot.event
async def on_guild_available(guild):
    await asyncio.sleep(
        2
    )  # Adjust the delay time if needed to ensure members are fetched properly
    # get all members from every server
    server_db = db.server_exists(session, guild.id)
    if not server_db:
        server_db = db.add_server(session, guild.id)
        print(server_db)
        for member in guild.members:
            print(member.name)

            db.add_user(session, member.id, member.name, server_db)


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
    res = db.update_daily_time(session, ctx.author.id, ctx.guild.id)
    if res[0]:
        new_balance = db.update_balance(session, ctx.author.id, ctx.guild.id, 1000)
        await ctx.send(
            f"{ctx.author.mention}\nDaily reward received! You've got {new_balance}🍰"
        )
    else:
        await ctx.send(f"{ctx.author.mention}\nYou need to wait {res[1]}")


# slot game
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
        if reward == 1:
            await ctx.send(
                f"{ctx.author.mention}\nYou've used 100 🍰 to spin the slots...\n"
                + slot_image
                + f"You've lost 100 🍰\n"
            )
            reward -= 101
        else:
            await ctx.send(
                f"{ctx.author.mention}\nYou've used 100 🍰 to spin the slots...\n"
                + slot_image
                + f"You've won {result[0]} 🍰\n"
            )
        db.update_balance(session, ctx.author.id, ctx.guild.id, reward)


# takes arguments in message and returns random element from arguments
@bot.command()
async def choice(ctx, *, message_text=""):
    input_words = message_text.split()
    if len(input_words) <= 1:
        await ctx.send("not enough arguments")
    else:
        answer = random.choice(input_words)
        await ctx.send(f"{ctx.author.mention}\nThe result is {answer}")


@bot.command()
async def steal(ctx, member: discord.Member = None):
    if not member:
        await ctx.send(f"You need to mention someone")
    else:
        balance = db.get_balance(session, member.id, ctx.guild.id)
        if random.random() > 0.5:
            if not balance:
                await ctx.send(f"This nigga is broke")
                return
            balance = random.randint(1, balance // 2)
            db.update_balance(session, member.id, ctx.guild.id, -balance)
            db.update_balance(session, ctx.author.id, ctx.guild.id, +balance)
            await ctx.send(
                f"{ctx.author.mention}\nYou seccessfully stole {balance} 🍰 from {member.mention}"
            )
        else:
            if not balance:
                await ctx.send(
                    f"This nigga is broke AND you've got caught, it's certified bruh moment"
                )
            else:
                await ctx.send(f"Nigga, you've got caught, you'll fined with 250 🍰")
            db.update_balance(session, ctx.author.id, ctx.guild.id, -250)


session = db.connect_db()
bot.run(TOKEN)
