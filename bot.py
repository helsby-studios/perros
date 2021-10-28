import discord
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

client = discord.Client()

#set commands
commands = [discord.ApplicationCommand(name="ping", description="Shows the roundtrip time"), discord.ApplicationCommand(name="apply", description="Start a application"),]
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


#application
async def apply(ctx, user: discord.User):
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
        print(interaction.values[0])
        for application in app:#load json files
            if interaction.values[0] == application:
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
                        final.add_field(name=field["question"], value=awnser.content, inline=False)
                    channel = client.get_channel(int(app[application]["channel"]))
                    await channel.send(embed=final)
                    return
                return
    else:
        await user.send("There are no applications available")



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
        await apply(interaction.response, interaction.user)
        print("applied")



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

        
client.run(token)