import asyncio
import logging
import os
from dotenv import load_dotenv

import novus
from novus.ext import client

load_dotenv()
dev_mode = os.getenv("DEV_MODE", "false").lower() == "true"
logging.basicConfig(
    level=logging.DEBUG if dev_mode else logging.INFO,
)

log = logging.getLogger("PerrOS")

intents = novus.Intents.all()
intents.privileged = False
intents.typing = False
config = client.Config(
    token=os.getenv("DISCORD_TOKEN"),
    intents=intents,
)
bot = client.Client(config)

class main(client.Plugin):
    @client.event("READY")
    async def on_ready(self):
        log.info("Perros Ready.")

    @client.command(name="Hello", description="World")
    async def hello(self, interaction: novus.Interaction):
        await interaction.send("Hello World")

bot.add_plugin(main)

if __name__ == "__main__":
    asyncio.run(bot.run(sync=True))
