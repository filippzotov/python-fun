import discord
from discord.ext import commands
from games.blackjack import Blackjack
import db_logic as db


class blackjack_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.games = {}

    @commands.command(name="blackjack")
    async def blackjack(self, ctx):
        if ctx.guild.id not in self.games:
            self.games[ctx.guild.id] = Blackjack(4)
        if ctx.author.id in self.games[ctx.guild.id].players:
            await ctx.send(f"You are already playing")
        else:
            result = self.games[ctx.guild.id].start_game(ctx.author.id)
            player_hand = self.games[ctx.guild.id].players[ctx.author.id][0]
            dealer_card = self.games[ctx.guild.id].players[ctx.author.id][1]
            print(result)
            if result is not None:
                await ctx.send(f"{result}")
            elif result == 1:
                await ctx.send(f"You won, {player_hand}, {dealer_card}")
                del self.games[ctx.guild.id].players[ctx.author.id]
            else:
                await ctx.send(f"Your hand: {player_hand}\n Dealer: {dealer_card[0]}")

    @commands.command(name="take")
    async def take(self, ctx):
        result = self.games[ctx.guild.id].take_card(ctx.author.id)
        player_hand = self.games[ctx.guild.id].players[ctx.author.id][0]
        dealer_card = self.games[ctx.guild.id].players[ctx.author.id][1]
        if result is False:
            await ctx.send(f"You lost, {player_hand}, {dealer_card}")
            del self.games[ctx.guild.id].players[ctx.author.id]
        else:
            await ctx.send(f"{player_hand}, {dealer_card[0]}")

    @commands.command(name="end")
    async def end(self, ctx):
        result = self.games[ctx.guild.id].end_game(ctx.author.id)
        player_hand = self.games[ctx.guild.id].players[ctx.author.id][0]
        dealer_card = self.games[ctx.guild.id].players[ctx.author.id][1]
        if not result:
            await ctx.send(f"You lost, {player_hand}, {dealer_card}")
        else:
            await ctx.send(f"You won, {player_hand}, {dealer_card}")
        del self.games[ctx.guild.id].players[ctx.author.id]


async def setup(bot):
    await bot.add_cog(blackjack_cog(bot))
