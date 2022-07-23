import discord
import requests
from discord.ext import commands


class updatemgr(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(application_command_meta=commands.ApplicationCommandMeta())
    @commands.has_permissions(administrator=True)
    async def update(self, ctx):
        response = requests.get(
            "https://raw.githubusercontent.com/helsby-studios/perros/main/bot.py"
        )
        with open("bot.py", "wb") as f:
            f.write(response.content)
        embed = discord.Embed(
            title="Bot Updated!", description="Bot has been updated!", color=0x00FF00
        )
        embed.add_field(
            name="Please restart the bot!", value="Bot Updated", inline=False
        )
        await ctx.interaction.response.send_message(embed=embed)


def setup(client):
    client.add_cog(updatemgr(client))
