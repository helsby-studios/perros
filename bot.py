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
        await interaction.response.send_message("coming soon")


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
                embed = discord.Embed(title=command["embed"]["title"], description=command["embed"]["description"], color=0x00ff00)
                for field in command["embed"]["fields"]:
                    embed.add_field(name=field["name"], value=field["value"], inline=False)
                embed.set_footer(text=command["embed"]["footer"])
                embed.set_thumbnail(url=command["embed"]["thumbnail"])
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(command["response"])

        
client.run(token)