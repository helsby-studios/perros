# pylint: skip-file
import datetime
import json

import discord
from discord.ext import commands

import mc_rcon


class applications(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def add_role(channel, user: discord.Member, role):
        role2 = channel.guild.get_role(role)
        await user.add_roles(role2)

    @commands.command(application_command_meta=commands.ApplicationCommandMeta())
    async def apply(self, ctx):
        await ctx.send("Check your Dms!")
        try:
            app = json.load(open(f"./applications.json"))
        except FileNotFoundError:
            app = {}

        if app != {}:
            options = []
            for application in app:  # load json files
                options.append(
                    discord.ui.SelectOption(
                        label=app[application]["name"], value=application
                    ),
                )
            components = discord.ui.MessageComponents(
                discord.ui.ActionRow(
                    discord.ui.SelectMenu(
                        custom_id="select menu",
                        options=options,
                    )
                )
            )
            await ctx.interaction.user.send(components=components)
            interaction = await self.client.wait_for("component_interaction")
            components.disable_components()
            await interaction.response.edit_message(components=components)

            for application in app:  # load json files
                if interaction.values[0] == application:
                    vals = []
                    embed = discord.Embed(title="Application", color=0x68B38C)
                    embed.add_field(
                        name="Applying for " + app[application]["name"],
                        value=app[application]["description"],
                        inline=False,
                    )
                    components = discord.ui.MessageComponents(
                        discord.ui.ActionRow(
                            discord.ui.Button(label="abort", custom_id="abort"),
                            discord.ui.Button(label="continue", custom_id="continue"),
                        ),
                    )
                    await ctx.interaction.user.send(embed=embed, components=components)
                    interaction = await self.client.wait_for("component_interaction")
                    components.disable_components()
                    await interaction.response.edit_message(components=components)
                    if interaction.component.custom_id == "abort":
                        embed = discord.Embed(title="Application", color=0x68B38C)
                        embed.add_field(
                            name="Aborted", value="Application aborted", inline=False
                        )
                        await ctx.interaction.user.send(embed=embed)
                        return
                    if interaction.component.custom_id == "continue":
                        embed = discord.Embed(title="Application", color=0x68B38C)
                        embed.add_field(
                            name="Applying for " + app[application]["name"],
                            value=app[application]["description"],
                            inline=False,
                        )
                        embed.add_field(
                            name="Please enter your application",
                            value="app",
                            inline=False,
                        )
                        await ctx.interaction.user.send(embed=embed)
                        final = discord.Embed(
                            title="Application - " + str(interaction.user),
                            color=0x68B38C,
                        )
                        for field in app[application]["questions"]:
                            embed = discord.Embed(title="Application", color=0x68B38C)
                            embed.add_field(
                                name=field["question"],
                                value="awnser below",
                                inline=False,
                            )
                            await ctx.interaction.user.send(embed=embed)
                            awnser = await self.client.wait_for(
                                "message",
                                timeout=30,
                                check=lambda message: message.author
                                == ctx.interaction.user,
                            )
                            vals.append(awnser)
                            final.add_field(
                                name=field["question"],
                                value=awnser.content,
                                inline=False,
                            )
                        finish = discord.Embed(title="Application", color=0x68B38C)
                        finish.add_field(
                            name="Application finished",
                            value="Thank you for your application",
                            inline=False,
                        )
                        await ctx.interaction.user.send(embed=finish)
                        channel = self.client.get_channel(
                            int(app[application]["channel"])
                        )
                        components = discord.ui.MessageComponents(
                            discord.ui.ActionRow(
                                discord.ui.Button(label="Accept", custom_id="accept"),
                                discord.ui.Button(label="Deny", custom_id="deny"),
                            )
                        )
                        await channel.send(embed=final, components=components)
                        interaction = await self.client.wait_for(
                            "component_interaction"
                        )
                        components.disable_components()
                        await interaction.response.edit_message(components=components)
                        if interaction.component.custom_id == "accept":
                            embed = discord.Embed(title="Application", color=0x68B38C)
                            embed.add_field(
                                name="Accepted",
                                value="Application accepted",
                                inline=False,
                            )
                            await ctx.interaction.user.send(embed=embed)
                            await channel.send(embed=embed)
                            role = int(app[application]["role"])
                            await ctx.interaction.user.add_roles(
                                channel.guild.get_role(role)
                            )
                            if app[application]["whitelist"] == "True":
                                index = 0
                                for field in app[application]["questions"]:
                                    index += 1
                                    if field["question"] == app[application]["ign_var"]:
                                        ign = vals[index - 1].content
                                        mc_rcon.whitelist_player(ign)
                                        break

                            question = []
                            index = 0
                            for field in app[application]["questions"]:
                                question.append(
                                    {field["question"]: vals[index - 1].content}
                                )
                            with open(
                                "./app_logs/"
                                + str(interaction.user)
                                + "_"
                                + application
                                + "_"
                                + str(
                                    datetime.datetime.now().strftime(
                                        "%d-%m-%Y-%H-%M-%S"
                                    )
                                )
                                + ".json",
                                "w",
                            ) as f:
                                json.dump(
                                    {
                                        str(interaction.user): {
                                            "user": str(interaction.user.id),
                                            "application": application,
                                            "date": datetime.datetime.now().strftime(
                                                "%d/%m/%Y %H:%M:%S"
                                            ),
                                            "questions": question,
                                        }
                                    },
                                    f,
                                    indent=4,
                                    sort_keys=True,
                                )
                        if interaction.component.custom_id == "deny":
                            embed = discord.Embed(title="Application", color=0xC92626)
                            embed.add_field(
                                name="Denied", value="Application denied", inline=False
                            )
                            await ctx.interaction.user.send(embed=embed)
                            final.add_field(
                                name="Denied", value="Application denied", inline=False
                            )
                            await channel.send(embed=embed)
                            print("denied")

                        return
                    return

        else:
            await ctx.send("No applications found!")


def setup(client):
    client.add_cog(applications(client))
