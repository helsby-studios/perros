import os
import sys
import time
import random
import json
import discord
import asyncio
import requests
import datetime
import subprocess
import mariadb
from dotenv import load_dotenv
from discord.ext import commands
import mc_rcon
import database

#invite link https://discord.com/api/oauth2/authorize?client_id=894582921946599474&permissions=8&redirect_uri=http%3A%2F%2Flocalhost%2Fcallback%2F&scope=bot%20applications.commands

#load envs
load_dotenv()
db_user = os.getenv("DB_USER")
db_passwd = os.getenv("DB_PASSWD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_db = os.getenv("DB_DB")
token = os.getenv("DISCORD_TOKEN")
dc_client_id = os.getenv("DISCORD_CLIENT_ID")
dc_client_secret = os.getenv("DISCORD_CLIENT_SECRET")
dc_callback_uri = os.getenv("DISCORD_CALLBACK_URI")
dev_mode = os.getenv("dev_mode")

client = discord.Client()

#set commands
commands = [
    discord.ApplicationCommand(name="ping", description="Shows the roundtrip time"),
    discord.ApplicationCommand(name="apply", description="Start a application"),
    discord.ApplicationCommand(name="create-todo", description="Create a Todolist"),
    discord.ApplicationCommand(name="delete-todo", description="Delete a Todolist"),
    discord.ApplicationCommand(name="add-todo", description="Add a task to a Todolist"),
]

av_commands = os.listdir("./commands")
for command in av_commands:
    command = json.load(open(f"./commands/{command}"))
    commands.append(discord.ApplicationCommand(name=command["name"], description=command["description"]))


#async executor
async def aexec(code):
    exec(
        f'async def __ex(): ' +
        ''.join(f'\n {l}' for l in code.split('\n'))
    )
    return await locals()['__ex']()



#onready event
@client.event
async def on_ready():
    await client.register_application_commands(commands)
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')
    if dev_mode == "true":
        print("Dev mode enabled")
        await client.change_presence(activity=discord.Game(name="Perros Development"))
    else:
        await client.change_presence(activity=discord.Game(name="cloudcorp.uk"))
        with open('profilepic.png', 'rb') as image:
            await client.user.edit(avatar=image.read())


#add role
async def add_role(channel, user: discord.Member, role):
    role2 = channel.guild.get_role(role)
    await user.add_roles(role2)

#application
async def apply(user: discord.User):
    try:
        app = json.load(open(f"./applications.json"))
    except:
        app = {}
    if app != "" and app != None:
        embed=discord.Embed(title="Application", color=0x68b38c)
        embed.add_field(name="What do you want to apply for?", value="please select", inline=False)
        options = []
        for application in app:#load json files
            options.append(discord.ui.SelectOption(label=app[application]["name"], value=application),)
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


        await user.send(embed=embed,components=components)

        def check(interaction: discord.Interaction):
            return True
        interaction = await client.wait_for("component_interaction", check=check)
        components.disable_components()
        await interaction.response.edit_message(components=components)
        if interaction.component.custom_id == "abort":
            embed=discord.Embed(title="Application", color=0x68b38c)
            embed.add_field(name="Aborted", value="Application aborted", inline=False)
            await user.send(embed=embed)
            return
        app_id = interaction.values[0]
        for application in app:#load json files
            if interaction.values[0] == application:
                vals = []
                embed=discord.Embed(title="Application", color=0x68b38c)
                embed.add_field(name="Applying for " + app[application]["name"], value=app[application]["description"], inline=False)
                components = discord.ui.MessageComponents(discord.ui.ActionRow(discord.ui.Button(label="abort", custom_id="abort"),discord.ui.Button(label="continue", custom_id="continue"),),)
                await user.send(embed=embed, components=components)
                interaction = await client.wait_for("component_interaction", check=check)
                components.disable_components()
                await interaction.response.edit_message(components=components)
                if interaction.component.custom_id == "abort":
                    embed=discord.Embed(title="Application", color=0x68b38c)
                    embed.add_field(name="Aborted", value="Application aborted", inline=False)
                    await user.send(embed=embed)
                    return
                if interaction.component.custom_id == "continue":
                    embed=discord.Embed(title="Application", color=0x68b38c)
                    embed.add_field(name="Applying for " + app[application]["name"], value=app[application]["description"], inline=False)
                    embed.add_field(name="Please enter your application", value="app", inline=False)
                    await user.send(embed=embed)
                    final=discord.Embed(title="Application - " + str(interaction.user), color=0x68b38c)
                    for field in app[application]["questions"]:
                        embed=discord.Embed(title="Application", color=0x68b38c)
                        embed.add_field(name=field["question"], value="awnser below", inline=False)
                        await user.send(embed=embed)
                        awnser = await client.wait_for("message", timeout = 30, check=lambda message: message.author == user)
                        vals.append(awnser)
                        final.add_field(name=field["question"], value=awnser.content, inline=False)
                    finish = discord.Embed(title="Application", color=0x68b38c)
                    finish.add_field(name="Application finished", value="Thank you for your application", inline=False)
                    await user.send(embed=finish)
                    channel = client.get_channel(int(app[application]["channel"]))
                    components = discord.ui.MessageComponents(discord.ui.ActionRow(discord.ui.Button(label="Accept", custom_id="accept"), discord.ui.Button(label="Deny", custom_id="deny")))
                    await channel.send(embed=final, components=components)
                    interaction = await client.wait_for("component_interaction", check=check)
                    components.disable_components()
                    await interaction.response.edit_message(components=components)
                    if interaction.component.custom_id == "accept":
                        embed=discord.Embed(title="Application", color=0x68b38c)
                        embed.add_field(name="Accepted", value="Application accepted", inline=False)
                        await user.send(embed=embed)
                        await channel.send(embed=embed)
                        role = int(app[application]["role"])
                        await user.add_roles(channel.guild.get_role(role))
                        if bool(app[application]["whitelist"]) == True:
                            index = 0
                            for field in app[application]["questions"]:
                                index += 1
                                if field["question"] == app[application]["ign_var"]:
                                    ign = vals[index - 1].content
                                    mc_rcon.whitelist_player(ign)
                                    break
                        index = 0
                        data = ""
                        for field in app[application]["questions"]:
                            index += 1
                            vals[index -1].content
                            data = data + str(field["question"]) + ": " + str(vals[index -1].content) + " \n  "
                        database.insert("users", user, str(app_id + " \n  " + data))




                        print("accepted")

                    if interaction.component.custom_id == "deny":
                        embed=discord.Embed(title="Application", color=0xc92626)
                        embed.add_field(name="Denied", value="Application denied", inline=False)
                        await user.send(embed=embed)
                        final.add_field(name="Denied", value="Application denied", inline=False)
                        await channel.send(embed=embed)
                        print("denied")

                    return
                return
    else:
        await user.send("There are no applications available")

class todolist:
    async def create(user):
        embed=discord.Embed(title="Todolist", color=0x68b38c)
        embed.add_field(name="Create todolist", value="Please enter the name of the todolist", inline=False)
        await user.send(embed=embed)
        awnser_titel = await client.wait_for("message", timeout=30, check=lambda message: message.author == user)
        embed=discord.Embed(title="Todolist", color=0x68b38c)
        embed.add_field(name="Create todolist", value="Please enter the description of the todolist", inline=False)
        await user.send(embed=embed)
        awnser_descript = await client.wait_for("message", timeout=30, check=lambda message: message.author == user)

        if os.path.exists("./todolists/" + awnser_titel.content + ".json"):
            embed=discord.Embed(title="Todolist", color=0xc92626)
            embed.add_field(name="Error", value="Todolist already exists", inline=False)
            await user.send(embed=embed)
            return
        else:
            embed = discord.Embed(title="Todolist", color=0x68b38c)
            embed.add_field(name=awnser_titel.content, value=awnser_descript.content, inline=False)
            embed.add_field(name="created...", value=".", inline=False)
            await user.send(embed=embed)
            with open("./todolists/" + awnser_titel.content + ".json", "w") as f:
                json.dump({"title": awnser_titel.content, "creator": str(user), "description": awnser_descript.content, "tasks": []}, f)

    async def delete(user):
        embed=discord.Embed(title="Todolist", color=0x68b38c)
        embed.add_field(name="Delete todolist", value="Please select the name of the todolist", inline=False)
        options = []
        for list in os.listdir('./todolists/'):  # load json files
            options.append(discord.ui.SelectOption(label=list, value=list), )
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
        await user.send(embed=embed, components=components)

        def check(interaction: discord.Interaction):
            return True
        interaction = await client.wait_for("component_interaction", check=check)
        components.disable_components()
        await interaction.response.edit_message(components=components)
        if interaction.component.custom_id == "abort":
            embed=discord.Embed(title="Todolist", color=0x68b38c)
            embed.add_field(name="Aborted", value="Deletion aborted", inline=False)
            await user.send(embed=embed)
            return

        if os.path.exists("./todolists/" + interaction.values[0]):
            with open("./todolists/" + interaction.values[0], "r") as f:
                data = json.load(f)

            if data["creator"] == str(user):
                os.remove("./todolists/" + interaction.values[0])
                embed=discord.Embed(title="Todolist", color=0x68b38c)
                embed.add_field(name="Deleted", value="Todolist deleted", inline=False)
                await user.send(embed=embed)
            else:
                embed=discord.Embed(title="Todolist", color=0xc92626)
                embed.add_field(name="Error", value="You do not have permission to delete this todolist", inline=False)
                await user.send(embed=embed)
        else:
            embed=discord.Embed(title="Todolist", color=0xc92626)
            embed.add_field(name="Error", value="Todolist does not exist", inline=False)
            await user.send(embed=embed)

    async def add_task(user):
        embed=discord.Embed(title="Todolist", color=0x68b38c)
        embed.add_field(name="Add task", value="Please select the name of the todolist", inline=False)
        options = []
        for list in os.listdir('./todolists/'):  # load json files
            options.append(discord.ui.SelectOption(label=list, value=list), )
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
        await user.send(embed=embed, components=components)

        def check(interaction: discord.Interaction):
            return True

        interaction = await client.wait_for("component_interaction", check=check)
        components.disable_components()
        await interaction.response.edit_message(components=components)
        if interaction.component.custom_id == "abort":
            embed = discord.Embed(title="Todolist", color=0x68b38c)
            embed.add_field(name="Aborted", value="Edit aborted", inline=False)
            await user.send(embed=embed)
            return

        if os.path.exists("./todolists/" + interaction.values[0]):
            with open("./todolists/" + interaction.values[0], "r") as f:
                data = json.load(f)

            if data["creator"] == str(user):
                embed=discord.Embed(title="Todolist", color=0x68b38c)
                embed.add_field(name="Add task", value="Please enter the name of the task", inline=False)
                await user.send(embed=embed)
                name = await client.wait_for("message", timeout=30, check=lambda message: message.author == user)
                embed=discord.Embed(title="Todolist", color=0x68b38c)
                embed.add_field(name="Add task", value="Please enter the description of the task", inline=False)
                await user.send(embed=embed)
                description = await client.wait_for("message", timeout=30, check=lambda message: message.author == user)
                with open("./todolists/" + interaction.values[0], "r") as f:
                    data = json.load(f)
                data["tasks"].append({"name": name.content, "description": description.content, "done": False})
                with open("./todolists/" + interaction.values[0], "w") as f:
                    json.dump(data, f)
                embed=discord.Embed(title="Todolist", color=0x68b38c)
                embed.add_field(name="Added", value="Task added", inline=False)
                with open("./todolists/" + interaction.values[0], "r") as f:
                    data = json.load(f)
                embed = discord.Embed(title="Todolist", color=0x68b38c)
                for task in data["tasks"]:
                    embed.add_field(name=task["name"], value=task["description"], inline=False)
                await user.send(embed=embed)

            else:
                embed = discord.Embed(title="Todolist", color=0xc92626)
                embed.add_field(name="Error", value="You do not have permission to edit this todolist", inline=False)
                await user.send(embed=embed)
        else:
            embed = discord.Embed(title="Todolist", color=0xc92626)
            embed.add_field(name="Error", value="Todolist does not exist", inline=False)
            await user.send(embed=embed)




#handle slash commands
@client.event
async def on_slash_command(interaction: discord.Interaction):
    command_name = interaction.command_name
    if command_name == "ping":
        if round(client.latency * 1000) <= 50:
            embed=discord.Embed(title="PING", description=f":ping_pong:The ping is **{round(client.latency *1000)}** milliseconds!", color=0x44ff44)
        elif round(client.latency * 1000) <= 100:
            embed=discord.Embed(title="PING", description=f":ping_pong:The ping is **{round(client.latency *1000)}** milliseconds!", color=0xffd000)
        elif round(client.latency * 1000) <= 200:
            embed=discord.Embed(title="PING", description=f":ping_pong:The ping is **{round(client.latency *1000)}** milliseconds!", color=0xff6600)
        else:
            embed=discord.Embed(title="PING", description=f":ping_pong:The ping is **{round(client.latency *1000)}** milliseconds!", color=0x990000)
        await interaction.response.send_message(embed=embed)

    if command_name == "apply":
        embed=discord.Embed(title="Application", color=0x68b38c)
        embed.add_field(name="Application started", value=interaction.user, inline=False)
        await interaction.response.send_message(embed=embed)
        await apply(interaction.user)

    if command_name == "create-todo":
        embed = discord.Embed(title="Todolist", color=0x68b38c)
        embed.add_field(name="Please check your DMs", value="Creation started", inline=False)
        await interaction.response.send_message(embed=embed)
        await todolist.create(user = interaction.user)

    if command_name == "delete-todo":
        embed = discord.Embed(title="Todolist", color=0x68b38c)
        embed.add_field(name="Please check your DMs", value="Deletion started", inline=False)
        await interaction.response.send_message(embed=embed)
        await todolist.delete(user = interaction.user)

    if command_name == "add-todo":
        embed = discord.Embed(title="Todolist", color=0x68b38c)
        embed.add_field(name="Please check your DMs", value="Adding task started", inline=False)
        await interaction.response.send_message(embed=embed)
        await todolist.add_task(user = interaction.user)


    #custom commands
    av_commands = os.listdir("./commands")
    for command in av_commands:
        command = json.load(open(f"./commands/{command}"))
        if command["name"] == command_name:
            if command["code"] != "":
                try:
                    commandresult = None
                    await aexec(command["code"])
                except:
                    pass
            if command["embed"] != "":
                embed = discord.Embed(title=command["embed"]["title"], description=command["embed"]["description"], color=0x68b38c)
                for field in command["embed"]["fields"]:
                    embed.add_field(name=field["name"], value=field["value"], inline=False)
                embed.set_footer(text=command["embed"]["footer"])
                embed.set_thumbnail(url=command["embed"]["thumbnail"])
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(command["response"])


def bot_main():
    client.run(token)

#run bot standalone
if __name__ == "__main__":
    bot_main()