import discord
from discord.ext import commands
from games.roulette import Roulette


class roulette_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.game = Roulette()
        self.bet_names = {
            "single": self.single_check,
            "split": self.split_check,
            "corner": self.croner_check,
            "lowhigh": self.low_high_check,
            "redblack": self.red_black_check,
            "evenodd": self.even_odd_check,
            "dozens": self.dozens_check,
            "columns": self.columns_check,
        }

    def input_check(self, input_line):
        if len(input_line) != 3:
            return False
        bet_type, bet_arg, amount = input_line
        if bet_type not in self.bet_names:
            return False
        if not self.bet_names[bet_type](bet_arg):
            return False
        if amount.isnumeric():
            return True
        return False

    def single_check(self, bet_arg):
        if int(bet_arg) >= 0 and int(bet_arg) <= 36:
            return True
        return False

    def split_check(self, bet_arg):
        if int(bet_arg) >= 0 and int(bet_arg) <= 36:
            return True
        return False

    def croner_check(self, bet_arg):
        if int(bet_arg) >= 0 and int(bet_arg) <= 36:
            return True
        return False

    def low_high_check(self, bet_arg):
        if bet_arg in ("low", "high"):
            return True
        return False

    def red_black_check(self, bet_arg):
        if bet_arg in ("black", "red"):
            return True
        return False

    def even_odd_check(self, bet_arg):
        if bet_arg in ("odd", "even"):
            return True
        return False

    def dozens_check(self, bet_arg):
        if bet_arg in ("first", "second", "third"):
            return True
        return False

    def columns_check(self, bet_arg):
        if bet_arg in ("first", "second", "third"):
            return True
        return False

    @commands.command(name="roulette")
    async def roulette(self, ctx, *args):
        if not self.input_check(args):
            await ctx.send("Wrong command")
        else:
            bet_type, bet_arg, amount = args
            mult, win_position = self.game.roll_wheel(bet_type, bet_arg)
            await ctx.send(
                f"The win position is {win_position}, you've won {int(amount) * mult}!"
            )


async def setup(bot):
    await bot.add_cog(roulette_cog(bot))
