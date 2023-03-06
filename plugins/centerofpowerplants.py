import novus
from novus.ext import client
import db_driver as db
import random

class centerofpowerplants(client.Plugin):
    @client.command(
        name="play",
        description="Start a game",
        options=[
            novus.ApplicationCommandOption(
                name="difficulty",
                description="The difficulty of the game (easy, medium, hard, extreme, insane)",
                type=novus.ApplicationOptionType.string,
            ),
        ],
        dm_permission=False,
    )
    async def play(self, interaction: novus.Interaction, difficulty: str):
        if difficulty not in ["easy", "medium", "hard"]:
            await interaction.send("Invalid difficulty")
            return
        #if db.get_game(interaction.guild) is not None:
        #    await interaction.send("A game is already in progress")
        #    return
        # generate map randomly depending on difficulty
        mymap = []
        if difficulty == "easy":
            for i in range(0, 24):
                mymap.append(random.randint(0, 100))
        elif difficulty == "medium":
            for i in range(0, 24):
                mymap.append(random.randint(0, 200))
        elif difficulty == "hard":
            for i in range(0, 24):
                mymap.append(random.randint(0, 300))
        elif difficulty == "extreme":
            for i in range(0, 24):
                mymap.append(random.randint(0, 400))
        elif difficulty == "insane":
            for i in range(0, 24):
                mymap.append(random.randint(0, 500))

        # convert map into a string seperated by : to store in db
        mymap = ":".join(str(x) for x in mymap)
        print(interaction.guild)
        await db.add_game(1, difficulty, 0, mymap)
        game = await db.get_game(1)
        await interaction.send("Game started")

        # generate button menu in an embed
        embed = novus.Embed(
            title="Center of Power Plants",
            description="Day 1",
            color=0x00FF00,
        )
        embed.add_field(
            name="Difficulty",
            value=game.difficulty,
            inline=False,
        )

        components = [
            novus.ActionRow([
                novus.Button(
                    label="1",
                    custom_id="1",
                    style=novus.ButtonStyle.primary,
                ),
            ]),
        ]

        await interaction.send(embeds=[embed], components=components)
        await db.delete_game(1)

    @client.event.filtered_component("1")
    async def on_button_click(self, interaction: novus.Interaction):
        await interaction.update("Button 1 clicked")

