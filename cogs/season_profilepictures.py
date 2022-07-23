import os
from datetime import date, datetime

import discord
from discord.ext import commands, tasks


class season_profilepictures(commands.Cog):
    def __init__(self, client):
        self.client = client
        if (
            os.path.exists("winter.png")
            and os.path.exists("summer.png")
            and os.path.exists("spring.png")
            and os.path.exists("fall.png")
        ):
            self.picture_update_service.start()

    @tasks.loop(hours=5)
    async def picture_update_service(self):
        Y = 2000
        seasons = [
            ("winter", (date(Y, 1, 1), date(Y, 3, 20))),
            ("spring", (date(Y, 3, 21), date(Y, 6, 20))),
            ("summer", (date(Y, 6, 21), date(Y, 9, 22))),
            ("autumn", (date(Y, 9, 23), date(Y, 12, 20))),
            ("winter", (date(Y, 12, 21), date(Y, 12, 31))),
        ]
        now = date.today()
        if isinstance(now, datetime):
            now = now.date()
        now = now.replace(year=Y)
        season = next(season for season, (start, end) in seasons if start <= now <= end)
        if season == "winter":
            with open("winter.png", "rb") as image:
                await self.client.user.edit(avatar=image.read())
        elif season == "spring":
            with open("spring.png", "rb") as image:
                await self.client.user.edit(avatar=image.read())
        elif season == "summer":
            with open("summer.png", "rb") as image:
                await self.client.user.edit(avatar=image.read())
        elif season == "autumn":
            with open("fall.png", "rb") as image:
                await self.client.user.edit(avatar=image.read())

    @commands.command(application_command_meta=commands.ApplicationCommandMeta())
    @commands.has_permissions(administrator=True)
    async def pp_status(self, ctx):
        embed = discord.Embed(
            title="Status",
            description="Status of the Profile Picture Service",
            color=0x00FF00,
        )
        if os.path.exists("winter.png"):
            embed.add_field(name="Winter", value="Found", inline=False)
        else:
            embed.add_field(name="Winter", value="Not Found", inline=False)
        if os.path.exists("summer.png"):
            embed.add_field(name="Summer", value="Found", inline=False)
        else:
            embed.add_field(name="Summer", value="Not Found", inline=False)
        if os.path.exists("spring.png"):
            embed.add_field(name="Spring", value="Found", inline=False)
        else:
            embed.add_field(name="Spring", value="Not Found", inline=False)
        if os.path.exists("fall.png"):
            embed.add_field(name="Fall", value="Found", inline=False)
        else:
            embed.add_field(name="Fall", value="Not Found", inline=False)
        await ctx.interaction.response.send_message(embed=embed)
        if (
            os.path.exists("winter.png")
            and os.path.exists("summer.png")
            and os.path.exists("spring.png")
            and os.path.exists("fall.png")
        ):
            try:
                self.picture_update_service.start()
            except RuntimeError:
                pass


def setup(client):
    client.add_cog(season_profilepictures(client))
