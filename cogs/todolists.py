import json
import os

import discord
from discord.ext import commands


class todolists(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(application_command_meta=commands.ApplicationCommandMeta())
    async def create_todo(self, ctx):
        await ctx.send("Check your Dms!")
        embed = discord.Embed(title="Todolist", color=0x68B38C)
        embed.add_field(
            name="Create todolist",
            value="Please enter the name of the todolist",
            inline=False,
        )
        await ctx.interaction.user.send(embed=embed)
        awnser_titel = await self.client.wait_for(
            "message",
            timeout=30,
            check=lambda message: message.author == ctx.interaction.user,
        )
        embed = discord.Embed(title="Todolist", color=0x68B38C)
        embed.add_field(
            name="Create todolist",
            value="Please enter the description of the todolist",
            inline=False,
        )
        await ctx.interaction.user.send(embed=embed)
        awnser_descript = await self.client.wait_for(
            "message",
            timeout=30,
            check=lambda message: message.author == ctx.interaction.user,
        )

        if os.path.exists("./todolists/" + awnser_titel.content + ".json"):
            embed = discord.Embed(title="Todolist", color=0xC92626)
            embed.add_field(name="Error", value="Todolist already exists", inline=False)
            await ctx.interaction.user.send(embed=embed)
            return
        else:
            embed = discord.Embed(title="Todolist", color=0x68B38C)
            embed.add_field(
                name=awnser_titel.content, value=awnser_descript.content, inline=False
            )
            embed.add_field(name="created...", value=".", inline=False)
            await ctx.interaction.user.send(embed=embed)
            with open("./todolists/" + awnser_titel.content + ".json", "w") as f:
                json.dump(
                    {
                        "title": awnser_titel.content,
                        "creator": str(ctx.interaction.user),
                        "description": awnser_descript.content,
                        "tasks": [],
                    },
                    f,
                )

    @commands.command(application_command_meta=commands.ApplicationCommandMeta())
    async def delete_todolist(self, ctx):
        await ctx.send("Check your Dms!")
        embed = discord.Embed(title="Todolist", color=0x68B38C)
        embed.add_field(
            name="Delete todolist",
            value="Please select the name of the todolist",
            inline=False,
        )
        options = []
        for list in os.listdir("./todolists/"):  # load json files
            options.append(
                discord.ui.SelectOption(label=list, value=list),
            )
        components = discord.ui.MessageComponents(
            discord.ui.ActionRow(
                discord.ui.SelectMenu(
                    custom_id="select",
                    options=options,
                ),
            ),
            discord.ui.ActionRow(
                discord.ui.Button(label="abort", custom_id="abort"),
            ),
        )
        await ctx.interaction.user.send(embed=embed, components=components)

        def check(interaction: discord.Interaction):
            return True

        interaction = await self.client.wait_for("component_interaction", check=check)
        components.disable_components()
        await interaction.response.edit_message(components=components)
        if interaction.component.custom_id == "abort":
            embed = discord.Embed(title="Todolist", color=0x68B38C)
            embed.add_field(name="Aborted", value="Deletion aborted", inline=False)
            await ctx.interaction.user.send(embed=embed)
            return

        if os.path.exists("./todolists/" + interaction.values[0]):
            with open("./todolists/" + interaction.values[0], "r") as f:
                data = json.load(f)

            if data["creator"] == str(ctx.interaction.user):
                os.remove("./todolists/" + interaction.values[0])
                embed = discord.Embed(title="Todolist", color=0x68B38C)
                embed.add_field(name="Deleted", value="Todolist deleted", inline=False)
                await ctx.interaction.user.send(embed=embed)
            else:
                embed = discord.Embed(title="Todolist", color=0xC92626)
                embed.add_field(
                    name="Error",
                    value="You do not have permission to delete this todolist",
                    inline=False,
                )
                await ctx.interaction.user.send(embed=embed)
        else:
            embed = discord.Embed(title="Todolist", color=0xC92626)
            embed.add_field(name="Error", value="Todolist does not exist", inline=False)
            await ctx.interaction.user.send(embed=embed)

    @commands.command(application_command_meta=commands.ApplicationCommandMeta())
    async def add_task(self, ctx):
        await ctx.send("Check your Dms!")
        embed = discord.Embed(title="Todolist", color=0x68B38C)
        embed.add_field(
            name="Add task",
            value="Please select the name of the todolist",
            inline=False,
        )
        options = []
        for list in os.listdir("./todolists/"):  # load json files
            options.append(
                discord.ui.SelectOption(label=list, value=list),
            )
        components = discord.ui.MessageComponents(
            discord.ui.ActionRow(
                discord.ui.SelectMenu(
                    custom_id="select",
                    options=options,
                ),
            ),
            discord.ui.ActionRow(
                discord.ui.Button(label="abort", custom_id="abort"),
            ),
        )
        await ctx.interaction.user.send(embed=embed, components=components)

        def check(interaction: discord.Interaction):
            return True

        interaction = await self.client.wait_for("component_interaction", check=check)
        components.disable_components()
        await interaction.response.edit_message(components=components)
        if interaction.component.custom_id == "abort":
            embed = discord.Embed(title="Todolist", color=0x68B38C)
            embed.add_field(name="Aborted", value="Edit aborted", inline=False)
            await ctx.interaction.user.send(embed=embed)
            return

        if os.path.exists("./todolists/" + interaction.values[0]):
            with open("./todolists/" + interaction.values[0], "r") as f:
                data = json.load(f)

            if data["creator"] == str(ctx.interaction.user):
                embed = discord.Embed(title="Todolist", color=0x68B38C)
                embed.add_field(
                    name="Add task",
                    value="Please enter the name of the task",
                    inline=False,
                )
                await ctx.interaction.user.send(embed=embed)
                name = await self.client.wait_for(
                    "message",
                    timeout=30,
                    check=lambda message: message.author == ctx.interaction.user,
                )
                embed = discord.Embed(title="Todolist", color=0x68B38C)
                embed.add_field(
                    name="Add task",
                    value="Please enter the description of the task",
                    inline=False,
                )
                await ctx.interaction.user.send(embed=embed)
                description = await self.client.wait_for(
                    "message",
                    timeout=30,
                    check=lambda message: message.author == ctx.interaction.user,
                )
                with open("./todolists/" + interaction.values[0], "r") as f:
                    data = json.load(f)
                data["tasks"].append(
                    {
                        "name": name.content,
                        "description": description.content,
                        "done": False,
                    }
                )
                with open("./todolists/" + interaction.values[0], "w") as f:
                    json.dump(data, f)
                embed = discord.Embed(title="Todolist", color=0x68B38C)
                embed.add_field(name="Added", value="Task added", inline=False)
                with open("./todolists/" + interaction.values[0], "r") as f:
                    data = json.load(f)
                embed = discord.Embed(title="Todolist", color=0x68B38C)
                for task in data["tasks"]:
                    embed.add_field(
                        name=task["name"], value=task["description"], inline=False
                    )
                await ctx.interaction.user.send(embed=embed)

            else:
                embed = discord.Embed(title="Todolist", color=0xC92626)
                embed.add_field(
                    name="Error",
                    value="You do not have permission to edit this todolist",
                    inline=False,
                )
                await ctx.interaction.user.send(embed=embed)
        else:
            embed = discord.Embed(title="Todolist", color=0xC92626)
            embed.add_field(name="Error", value="Todolist does not exist", inline=False)
            await ctx.interaction.user.send(embed=embed)

    @commands.command(application_command_meta=commands.ApplicationCommandMeta())
    async def delete_task(self, ctx):
        await ctx.send("Check your Dms!")
        embed = discord.Embed(title="Todolist", color=0x68B38C)
        embed.add_field(
            name="Delete task",
            value="Please select the name of the todolist",
            inline=False,
        )
        options = []
        for list in os.listdir("./todolists/"):  # load json files
            options.append(
                discord.ui.SelectOption(label=list, value=list),
            )
        components = discord.ui.MessageComponents(
            discord.ui.ActionRow(
                discord.ui.SelectMenu(
                    custom_id="select",
                    options=options,
                ),
            ),
            discord.ui.ActionRow(
                discord.ui.Button(label="abort", custom_id="abort"),
            ),
        )
        await ctx.interaction.user.send(embed=embed, components=components)

        def check(interaction: discord.Interaction):
            return True

        interaction = await self.client.wait_for("component_interaction", check=check)
        components.disable_components()
        await interaction.response.edit_message(components=components)
        if interaction.component.custom_id == "abort":
            embed = discord.Embed(title="Todolist", color=0x68B38C)
            embed.add_field(name="Aborted", value="Edit aborted", inline=False)
            await ctx.interaction.user.send(embed=embed)
            return

        if os.path.exists("./todolists/" + interaction.values[0]):
            file = interaction.values[0]
            with open("./todolists/" + file, "r") as f:
                data = json.load(f)

            if data["creator"] == str(ctx.interaction.user):
                embed = discord.Embed(title="Todolist", color=0x68B38C)
                embed.add_field(
                    name="Delete task",
                    value="Please select the task you want to delete",
                    inline=False,
                )
                options = []
                for task in data["tasks"]:
                    options.append(
                        discord.ui.SelectOption(label=task["name"], value=task["name"]),
                    )
                components = discord.ui.MessageComponents(
                    discord.ui.ActionRow(
                        discord.ui.SelectMenu(
                            custom_id="select",
                            options=options,
                        ),
                    ),
                    discord.ui.ActionRow(
                        discord.ui.Button(label="abort", custom_id="abort"),
                    ),
                )
                await ctx.interaction.user.send(embed=embed, components=components)
                interaction = await self.client.wait_for(
                    "component_interaction", check=check
                )
                components.disable_components()
                await interaction.response.edit_message(components=components)
                if interaction.component.custom_id == "abort":
                    embed = discord.Embed(title="Todolist", color=0x68B38C)
                    embed.add_field(name="Aborted", value="Edit aborted", inline=False)
                    await ctx.interaction.user.send(embed=embed)
                    return

                for task in data["tasks"]:
                    if task["name"] == interaction.values[0]:
                        data["tasks"].remove(task)
                        break
                with open("./todolists/" + file, "w") as f:
                    json.dump(data, f)
                embed = discord.Embed(title="Todolist", color=0x68B38C)
                embed.add_field(name="Task deleted", value="Task deleted", inline=False)
                await ctx.interaction.user.send(embed=embed)
                with open("./todolists/" + file, "r") as f:
                    data = json.load(f)
                embed = discord.Embed(title="Todolist", color=0x68B38C)
                for task in data["tasks"]:
                    embed.add_field(
                        name=task["name"], value=task["description"], inline=False
                    )
                await ctx.interaction.user.send(embed=embed)
            else:
                embed = discord.Embed(title="Todolist", color=0xC92626)
                embed.add_field(
                    name="Error",
                    value="You do not have permission to edit this todolist",
                    inline=False,
                )
                await ctx.interaction.user.send(embed=embed)
        else:
            embed = discord.Embed(title="Todolist", color=0xC92626)
            embed.add_field(name="Error", value="Todolist does not exist", inline=False)
            await ctx.interaction.user.send(embed=embed)

    @commands.command(application_command_meta=commands.ApplicationCommandMeta())
    async def list_task(self, ctx):
        await ctx.send("Check your Dms!")
        embed = discord.Embed(title="Todolist", color=0x68B38C)
        embed.add_field(
            name="List tasks",
            value="Please select the name of the todolist",
            inline=False,
        )
        options = []
        for list in os.listdir("./todolists/"):  # load json files
            options.append(
                discord.ui.SelectOption(label=list, value=list),
            )
        components = discord.ui.MessageComponents(
            discord.ui.ActionRow(
                discord.ui.SelectMenu(
                    custom_id="select",
                    options=options,
                ),
            ),
            discord.ui.ActionRow(
                discord.ui.Button(label="abort", custom_id="abort"),
            ),
        )
        await ctx.interaction.user.send(embed=embed, components=components)

        def check(interaction: discord.Interaction):
            return True

        interaction = await self.client.wait_for("component_interaction", check=check)
        components.disable_components()
        await interaction.response.edit_message(components=components)
        if interaction.component.custom_id == "abort":
            embed = discord.Embed(title="Todolist", color=0x68B38C)
            embed.add_field(name="Aborted", value="Listing aborted", inline=False)
            await ctx.interaction.user.send(embed=embed)
            return

        if os.path.exists("./todolists/" + interaction.values[0]):
            with open("./todolists/" + interaction.values[0], "r") as f:
                data = json.load(f)

            if data["creator"] == str(ctx.interaction.user):
                embed = discord.Embed(title="Todolist", color=0x68B38C)
                for task in data["tasks"]:
                    embed.add_field(
                        name=task["name"], value=task["description"], inline=False
                    )
                await ctx.interaction.user.send(embed=embed)

            else:
                embed = discord.Embed(title="Todolist", color=0xC92626)
                embed.add_field(
                    name="Error",
                    value="You do not have permission to view this todolist",
                    inline=False,
                )
                await ctx.interaction.user.send(embed=embed)
        else:
            embed = discord.Embed(title="Todolist", color=0xC92626)
            embed.add_field(name="Error", value="Todolist does not exist", inline=False)
            await ctx.interaction.user.send(embed=embed)


def setup(client):
    client.add_cog(todolists(client))
