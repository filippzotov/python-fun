import discord
from discord.ext import commands
from games.roulette import Roulette
import db_logic as db


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
        self.help_text = """
        Example of command c!roulette single 6 100 - single bet on number 6 with 100 money bet
        single - pcick single number form 0 to 36
        lowhigh - 0-18 low, 19-36 high
        redblack - pick color, red or black
        evenodd - pick even or odd
        dozens - pick dozen, first 0-12, second 13-24, third 25-36
        columns - pick column, first, second or third
        """

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
            if mult < 0:
                await ctx.send(
                    f"The win position is {win_position}, you've lost {-(int(amount) * mult)}"
                )
            else:
                await ctx.send(
                    f"The win position is {win_position}, you've won {int(amount) * mult}!"
                )
            db.update_balance(
                db.connect_db(), ctx.author.id, ctx.guild.id, int(amount) * mult
            )

    @commands.command(name="roulette_help")
    async def roulette_help(self, ctx):
        embed = discord.Embed(color=0xFFEE99)
        embed.set_image(
            url="https://upload.wikimedia.org/wikipedia/commons/4/43/Roulette_frz_2.png"
        )
        embed.set_author(name="Roulette rules and commands")
        embed.add_field(name="", value=self.help_text, inline=False)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(roulette_cog(bot))
