import discord
from discord.ext import commands
from games.blackjack import Blackjack
import db_logic as db


class blackjack_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.games = {}
        self.number = {
            "1": ":regional_indicator_a:",
            "2": ":two:",
            "3": ":three:",
            "4": ":four:",
            "5": ":six:",
            "6": ":six:",
            "7": ":seven:",
            "8": ":eight:",
            "9": ":nine:",
            "10": ":keycap_ten:",
            "j": ":regional_indicator_j:",
            "q": ":regional_indicator_q:",
            "k": ":regional_indicator_k:",
        }
        self.suit = {
            "h": ":hearts:",
            "c": ":clubs:",
            "d": ":diamonds:",
            "s": ":spades:",
        }

        #

    def get_emoji_result(self, player, dealer):
        player_emoji = []
        dealer_emoji = []
        for card in player:
            player_emoji.append(self.number[card[:-1]] + self.suit[card[-1]])
        for card in dealer:
            dealer_emoji.append(self.number[card[:-1]] + self.suit[card[-1]])
        return (player_emoji, dealer_emoji)

    def get_player_game(self, ctx):
        player_hand = self.games[ctx.guild.id].players[ctx.author.id][0]
        dealer_hand = self.games[ctx.guild.id].players[ctx.author.id][1]
        return self.get_emoji_result(player_hand, dealer_hand)

    async def print_take(self, ctx):
        player_hand, dealer_hand = self.get_player_game(ctx)
        await ctx.send(f"Your hand: {' '.join(player_hand)}\n Dealer: {dealer_hand[0]}")

    async def print_win(self, ctx):
        player_hand, dealer_hand = self.get_player_game(ctx)
        await ctx.send(
            f"You won,\nYour hand{' '.join(player_hand)}\nDealer hand{' '.join(dealer_hand)}"
        )
        self.change_balance(ctx, 1)
        del self.games[ctx.guild.id].players[ctx.author.id]

    async def print_lost(self, ctx):
        player_hand, dealer_hand = self.get_player_game(ctx)
        await ctx.send(
            f"You lost\nYour hand: {' '.join(player_hand)}\nDealer hand: {' '.join(dealer_hand)}"
        )
        self.change_balance(ctx, -1)
        del self.games[ctx.guild.id].players[ctx.author.id]

    def change_balance(self, ctx, win_lost):
        print(self.games[ctx.guild.id].players[ctx.author.id])
        money = self.games[ctx.guild.id].players[ctx.author.id][2]
        db.update_balance(
            db.connect_db(), ctx.author.id, ctx.guild.id, int(money) * win_lost
        )

    @commands.command(name="blackjack")
    async def blackjack(self, ctx, *args):
        if len(args) != 1 or not args[0].isnumeric():
            await ctx.send(f"Wrong command")
            return
        if ctx.guild.id not in self.games:
            self.games[ctx.guild.id] = Blackjack(4)
        if ctx.author.id in self.games[ctx.guild.id].players:
            await ctx.send(f"You are already playing")
        else:
            result = self.games[ctx.guild.id].start_game(ctx.author.id, args[0])
            if result is not None:
                await ctx.send(f"{result}")
            elif result == 1:
                await self.print_win(ctx)
            else:
                await self.print_take(ctx)

    @commands.command(name="take")
    async def take(self, ctx):
        result = self.games[ctx.guild.id].take_card(ctx.author.id)
        if result is False:
            await self.print_lost(ctx)
        else:
            await self.print_take(ctx)

    @commands.command(name="end")
    async def end(self, ctx):
        result = self.games[ctx.guild.id].end_game(ctx.author.id)
        if not result:
            await self.print_lost(ctx)
        else:
            await self.print_win(ctx)


async def setup(bot):
    await bot.add_cog(blackjack_cog(bot))
