import discord
from discord.ext import commands
from requests import get


class IPinfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(application_command_meta=commands.ApplicationCommandMeta())
    async def ipinfo(self, ctx):
        ip = get("https://api.ipify.org").text
        embed = discord.Embed(
            title="IP Info", description="Current IP: " + str(ip), color=0x00FF00
        )
        await ctx.interaction.response.send_message(embed=embed)


def setup(client):
    client.add_cog(IPinfo(client))
