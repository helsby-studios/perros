import discord
from discord.ext import commands, tasks


class tmp_voicechannels(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.vc_manager.start()

    @tasks.loop(seconds=5)
    async def vc_manager(self):
        for server in self.client.guilds:
            voice_channel_list = []
            for channel in server.channels:
                if str(channel.type) == "voice":
                    voice_channel_list.append(channel)
            exists = False
            for channel in voice_channel_list:
                if channel.name == "Create a Voice Channel":
                    exists = True
                    for member in channel.members:
                        print(member)
                        print(member.voice.channel)
                        print(channel)
                        print(channel.id)
                        await server.create_voice_channel("tmp-" + member.name)
                        channel = discord.utils.get(
                            server.channels, name="tmp-" + member.name
                        )
                        await member.move_to(channel)

                if len(channel.members) == 0 and "tmp-" in channel.name:
                    await channel.delete()
            if not exists:
                for guild in self.client.guilds:
                    await guild.create_voice_channel("Create a Voice Channel")

    @commands.command(
        application_command_meta=commands.ApplicationCommandMeta(
            options=[
                discord.ApplicationCommandOption(
                    name="name",
                    type=discord.ApplicationCommandOptionType.string,
                    description="The new name of the channel",
                ),
            ]
        )
    )
    async def vc_rename(self, ctx, name: str):
        channel = ctx.interaction.user.voice.channel
        name = "tmp-" + name
        await channel.edit(name=name)
        await ctx.interaction.response.send_message(f"Renamed channel to {name}")

    @commands.command(
        application_command_meta=commands.ApplicationCommandMeta(
            options=[
                discord.ApplicationCommandOption(
                    name="limit",
                    type=discord.ApplicationCommandOptionType.string,
                    description="The new limit of the channel",
                ),
            ]
        )
    )
    async def vc_limit(self, ctx, limit: str):
        channel = ctx.interaction.user.voice.channel
        await channel.edit(user_limit=limit)
        await ctx.interaction.response.send_message(f"Set channel limit to {limit}")


def setup(client):
    client.add_cog(tmp_voicechannels(client))
