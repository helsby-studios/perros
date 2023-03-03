import novus
from novus.ext import client

class test(client.Plugin):
    @client.command(name="test", description="me")
    async def hello(self, interaction: novus.Interaction):
        await interaction.send("This Command was loaded from a plugin file.")