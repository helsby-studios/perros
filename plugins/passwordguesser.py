import novus
from novus.ext import client

import aiohttp
import asyncio
import hashlib


class passwordguesser(client.Plugin):
    @client.command(name="passwordguesser", description="play a game of passwordguesser")
    async def play(self, interaction: novus.Interaction):
        global running
        global score
        global already_guessed
        running = True
        score = 0
        already_guessed = []
        # create a embed with a timer and buttons to stop
        embed = novus.Embed(
            title="Password Guesser",
            description="Time left: 60",
            color=0x00FF00,
        )
        embed.add_field(name="Score", value="0")
        embed.add_field(name="Instructions", value="Send a message to guess the password")

        # create the buttons
        components = [
            novus.ActionRow([
                novus.Button(
                    label="Stop",
                    style=novus.ButtonStyle.danger,
                    custom_id="stop",
                ),
            ]),
        ]

        # send the embed
        await interaction.send(embeds=[embed], components=components)

        # start a one minute timer and edit the message to update the timer
        for i in range(60):
            if running == False:
                break
            embed = novus.Embed(
                title="Password Guesser",
                description=f"Time left: {60 - i}",
                color=0x00FF00,
            )
            embed.add_field(name="Score", value=str(score))
            embed.add_field(name="Instructions", value="Send a message to guess the password")
            await interaction.edit_original(embeds=[embed], components=components)
            await asyncio.sleep(1)

        # set running to false and send a message with the score
        running = False
        embed = novus.Embed(
            title="Password Guesser",
            description="Time's up!",
            color=0xFF0000,
        )
        embed.add_field(name="Score", value=str(score))
        await interaction.edit_original(embeds=[embed], components=[])
        await interaction.send(embeds=[embed])
        score = 0

    @client.event.message
    async def gamehandler(self, message: novus.Message):
        global running
        global score
        global already_guessed
        if running and message.author.bot == False:
            guess = message.content

            # hash the message content with sha1
            hashed = hashlib.sha1(guess.encode()).hexdigest()
            # send the hash to the api
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://api.pwnedpasswords.com/range/{hashed[:5]}") as response:
                    r = await response.text()
            # check if the hash is in the api
            if hashed[5:].upper() in r and guess not in already_guessed:
                # if it is, add one to the score and react with a checkmark
                await message.add_reaction("✅")
                already_guessed.append(guess)
                score += 1
            else:
                # if it isn't, react with a cross
                await message.add_reaction("❌")

    @client.event.filtered_component("stop")
    async def stop(self, interaction: novus.Interaction):
        global running
        global score
        if running:
            running = False
        await interaction.send("Game stopped", ephemeral=True)
