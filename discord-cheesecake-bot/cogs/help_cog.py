import discord
from discord.ext import commands


# from youtube_dl import YoutubeDL


class help_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.help_text = """
        currency:
        help - you can see it now 👀
        slots - roll slot machine for 100 🍰
        balance - show your balance of 🍰 on this server
        steal - in development...
        \nrandom:
        choice - chose one of input arguments, example: c!choise one two three
        \nmusic:
        play - play audio from youtube
        skip - skip current audio
        leave - leave voice channel
        
        """

    @commands.command(name="help")
    async def help(self, ctx, *args):
        embed = discord.Embed(color=0xFFEE99)
        embed.set_author(name="Cheesecake command list")
        embed.set_thumbnail(url="https://i.imgur.com/ORADcoT.jpeg")
        embed.add_field(name="", value=self.help_text, inline=False)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(help_cog(bot))
