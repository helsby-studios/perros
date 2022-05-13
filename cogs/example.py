import discord
from discord.ext import commands


class Example(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(application_command_meta=commands.ApplicationCommandMeta())
    async def examplecog(self, ctx):
        await ctx.send("Examplecog!")


def setup(client):
    client.add_cog(Example(client))
