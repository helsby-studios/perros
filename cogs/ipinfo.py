import discord
from discord.ext import commands
from requests import get


class IPinfo(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.last_ip = get("https://api.ipify.org").text

    @commands.command(application_command_meta=commands.ApplicationCommandMeta())
    async def ipinfo(self, ctx):
        ip = get("https://api.ipify.org").text
        embed = discord.Embed(
            title="IP Info", description="Current IP:" + ip, color=0x00FF00
        )
        if self.last_ip != ip:
            embed.add_field(
                name="IP Changed",
                value="From " + self.last_ip + " to " + ip,
                inline=False,
            )
            self.last_ip = ip
        await ctx.interaction.response.send_message(embed=embed)


def setup(client):
    client.add_cog(IPinfo(client))
