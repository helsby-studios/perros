import json
import os

import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv

try:
    from pip import main as pipmain
except Exception:
    from pip._internal.main import main as pipmain

# load env
load_dotenv()
token = os.getenv("DISCORD_TOKEN")
dc_client_id = os.getenv("DISCORD_CLIENT_ID")
dc_client_secret = os.getenv("DISCORD_CLIENT_SECRET")
dc_callback_uri = os.getenv("DISCORD_CALLBACK_URI")
dev_mode = os.getenv("dev_mode")

client = commands.Bot(command_prefix=None)

if dev_mode == "true":
    guild_id = 888854978230374430


# add role
async def add_role(channel, user: discord.Member, role):
    role2 = channel.guild.get_role(role)
    await user.add_roles(role2)


@client.command(
    application_command_meta=commands.ApplicationCommandMeta(
        options=[
            discord.ApplicationCommandOption(
                name="one",
                type=discord.ApplicationCommandOptionType.integer,
                description="The first number that you want to add.",
            ),
            discord.ApplicationCommandOption(
                name="two",
                type=discord.ApplicationCommandOptionType.integer,
                description="The second number that you want to add.",
            ),
        ]
    )
)
async def add(ctx, one: int, two: int):
    await ctx.interaction.response.send_message(one + two)


@client.command(application_command_meta=commands.ApplicationCommandMeta())
async def ping(ctx):
    if round(client.latency * 1000) <= 50:
        embed = discord.Embed(
            title="PING",
            description=f":ping_pong:The ping is **{round(client.latency * 1000)}** milliseconds!",
            color=0x44FF44,
        )
    elif round(client.latency * 1000) <= 100:
        embed = discord.Embed(
            title="PING",
            description=f":ping_pong:The ping is **{round(client.latency * 1000)}** milliseconds!",
            color=0xFFD000,
        )
    elif round(client.latency * 1000) <= 200:
        embed = discord.Embed(
            title="PING",
            description=f":ping_pong:The ping is **{round(client.latency * 1000)}** milliseconds!",
            color=0xFF6600,
        )
    else:
        embed = discord.Embed(
            title="PING",
            description=f":ping_pong:The ping is **{round(client.latency * 1000)}** milliseconds!",
            color=0x990000,
        )
    await ctx.interaction.response.send_message(embed=embed)


@client.command(
    application_command_meta=commands.ApplicationCommandMeta(
        options=[
            discord.ApplicationCommandOption(
                name="cog",
                type=discord.ApplicationCommandOptionType.string,
                description="The name of the cog you want to load.",
            ),
        ]
    )
)
@commands.has_permissions(administrator=True)
async def load(ctx, cog: str):
    try:
        ctx.bot.load_extension(f"cogs.{cog}")
        await ctx.interaction.response.send_message(f"Loaded {cog}")
        if dev_mode == "true":
            await ctx.bot.register_application_commands(guild=discord.Object(guild_id))
        else:
            await ctx.bot.register_application_commands()
    except discord.ext.commands.errors.ExtensionAlreadyLoaded:
        await ctx.interaction.response.send_message(f"{cog} is already loaded.")
    except discord.ext.commands.errors.ExtensionNotFound:
        await ctx.interaction.response.send_message(f"{cog} is not found.")
    except discord.ext.commands.errors.ExtensionFailed:
        await ctx.interaction.response.send_message(f"{cog} failed to load.")
    except Exception as e:
        if dev_mode == "true":
            await ctx.interaction.response.send_message(f"{cog} failed to load.\n{e}")
        else:
            pass


@client.command(
    application_command_meta=commands.ApplicationCommandMeta(
        options=[
            discord.ApplicationCommandOption(
                name="cog",
                type=discord.ApplicationCommandOptionType.string,
                description="The name of the cog you want to unload.",
            ),
        ]
    )
)
@commands.has_permissions(administrator=True)
async def unload(ctx, cog: str):
    try:
        ctx.bot.unload_extension(f"cogs.{cog}")
        await ctx.interaction.response.send_message(f"Unloaded {cog}")
        if dev_mode == "true":
            await ctx.bot.register_application_commands(guild=discord.Object(guild_id))
        else:
            await ctx.bot.register_application_commands()
    except discord.ext.commands.errors.ExtensionNotLoaded:
        await ctx.interaction.response.send_message(f"{cog} is not loaded.")
    except Exception as e:
        if dev_mode == "true":
            await ctx.interaction.response.send_message(f"{cog} failed to unload.\n{e}")
        else:
            pass


@client.command(
    application_command_meta=commands.ApplicationCommandMeta(
        options=[
            discord.ApplicationCommandOption(
                name="cog",
                type=discord.ApplicationCommandOptionType.string,
                description="The name of the cog you want to reload.",
            ),
        ]
    )
)
@commands.has_permissions(administrator=True)
async def reload(ctx, cog: str):
    try:
        ctx.bot.unload_extension(f"cogs.{cog}")
        ctx.bot.load_extension(f"cogs.{cog}")
        await ctx.interaction.response.send_message(f"reloaded {cog}")
        if dev_mode == "true":
            await ctx.bot.register_application_commands(guild=discord.Object(guild_id))
        else:
            await ctx.bot.register_application_commands()
    except Exception as e:
        if dev_mode == "true":
            await ctx.interaction.response.send_message(f"{cog} failed to reload.\n{e}")
        else:
            ctx.interaction.response.send_message(f"{cog} failed to reload.")


@client.command(
    application_command_meta=commands.ApplicationCommandMeta(
        options=[
            discord.ApplicationCommandOption(
                name="link",
                type=discord.ApplicationCommandOptionType.string,
                description="The link of the cog you want to download. (raw)",
            ),
        ]
    )
)
@commands.has_permissions(administrator=True)
async def download(ctx, link: str):
    response = requests.get(link)
    with open(f"cogs/{response.url.split('/')[-1]}", "wb") as f:
        f.write(response.content)
    await ctx.interaction.response.send_message(
        f"Downloaded {response.url.split('/')[-1]} \n use load {response.url.split('/')[-1]}` to load it.",
    )


@client.command(
    application_command_meta=commands.ApplicationCommandMeta(
        options=[
            discord.ApplicationCommandOption(
                name="cog",
                type=discord.ApplicationCommandOptionType.string,
                description="The name of the cog you want to disable.",
            ),
        ]
    )
)
@commands.has_permissions(administrator=True)
async def disable(ctx, cog: str):
    try:
        ctx.bot.unload_extension(f"cogs.{cog}")
        if dev_mode == "true":
            await ctx.bot.register_application_commands(guild=discord.Object(guild_id))
        else:
            await ctx.bot.register_application_commands()
        try:
            os.rename(f"cogs/{cog}.py", f"cogs/{cog}.disabled")
            await ctx.interaction.response.send_message(f"Disabled {cog}")
        except FileNotFoundError:
            ctx.interaction.response.send_message(
                f"Failed to disable {cog}, it is probably not loaded."
            )
        except Exception as e:
            if dev_mode == "true":
                await ctx.interaction.response.send_message(
                    f"{cog} failed to disable.\n{e}"
                )
            else:
                pass
    except discord.ext.commands.errors.ExtensionNotLoaded:
        try:
            os.rename(f"cogs/{cog}.py", f"cogs/{cog}.disabled")
            await ctx.interaction.response.send_message(f"Disabled {cog}")
        except FileNotFoundError:
            ctx.interaction.response.send_message(
                f"Failed to disable {cog}, it is probably not loaded."
            )
        except Exception as e:
            if dev_mode == "true":
                await ctx.interaction.response.send_message(
                    f"{cog} failed to disable.\n{e}"
                )
            else:
                pass
    except Exception as e:
        if dev_mode == "true":
            await ctx.interaction.response.send_message(
                f"{cog} failed to disable.\n{e}"
            )
        else:
            pass


@client.command(
    application_command_meta=commands.ApplicationCommandMeta(
        options=[
            discord.ApplicationCommandOption(
                name="cog",
                type=discord.ApplicationCommandOptionType.string,
                description="The name of the cog you want to enable.",
            ),
        ]
    )
)
@commands.has_permissions(administrator=True)
async def enable(ctx, cog: str):
    try:
        os.rename(f"cogs/{cog}.disabled", f"cogs/{cog}.py")
        await ctx.interaction.response.send_message(
            f"enabled {cog}, load with load {cog}"
        )
    except FileNotFoundError:
        ctx.interaction.response.send_message(
            f"Failed to enable {cog}, it is probably not disabled."
        )
    except Exception as e:
        if dev_mode == "true":
            await ctx.interaction.response.send_message(f"{cog} failed to enable.\n{e}")
        else:
            pass


@client.command(application_command_meta=commands.ApplicationCommandMeta())
@commands.has_permissions(administrator=True)
async def repos(ctx):
    with open("sources.txt", "r") as f:
        reposit = f.read()
    embed = discord.Embed(
        title="Available Cogs:",
        description="Available cogs from the repository in sources.txt",
    )
    for repo in reposit.split("\n"):
        index = requests.get(repo).text
        index = json.loads(index)
        embed.add_field(
            name=index["name"] + ":",
            value=index["description"] + "\n id: " + index["id"],
            inline=False,
        )
        for cog in index["cogs"]:
            embed.add_field(
                name=index["cogs"][cog]["name"],
                value=index["cogs"][cog]["description"],
                inline=False,
            )
    await ctx.interaction.response.send_message(embed=embed)


@client.command(
    application_command_meta=commands.ApplicationCommandMeta(
        options=[
            discord.ApplicationCommandOption(
                name="cog",
                type=discord.ApplicationCommandOptionType.string,
                description="The name of the cog you want to download.",
            ),
        ]
    )
)
@commands.has_permissions(administrator=True)
async def repo_download(ctx, cog: str):
    with open("sources.txt", "r") as f:
        reposit = f.read()
    for repo in reposit.split("\n"):
        index = requests.get(repo).text
        index = json.loads(index)
        for cogs in index["cogs"]:
            if cog == index["cogs"][cogs]["name"]:
                file = index["cogs"][cogs]["filename"]
                requirements = index["cogs"][cogs]["requirements"]
                requirements = requirements.split(", ")
                for req in requirements:
                    if req == "discord.py":
                        pass
                    else:
                        print(req)
                        try:
                            pipmain(["install", req])
                        except Exception as e:
                            print(e)
                            pass
                link = repo.strip("index.json") + file
                response = requests.get(link)
                with open(f"cogs/{response.url.split('/')[-1]}", "wb") as f:
                    f.write(response.content)
                await ctx.interaction.response.send_message(
                    f"Downloaded {link.split('/')[-1]} \n use /load {link.split('/')[-1].strip('.py')} to load it.",
                )


@client.command(
    application_command_meta=commands.ApplicationCommandMeta(
        options=[
            discord.ApplicationCommandOption(
                name="url",
                type=discord.ApplicationCommandOptionType.string,
                description="The url to the repo you want to add. (needs to be raw)",
            ),
        ]
    )
)
@commands.has_permissions(administrator=True)
async def repo_add(ctx, url: str):
    with open("sources.txt", "a") as f:
        f.write("\n" + url)
    await ctx.interaction.response.send_message(
        f"Added {url} to sources.txt, use /repos to see the list of available cogs."
    )


# on_ready event
@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("------")
    if dev_mode == "true":
        print("Dev mode enabled")
        await client.change_presence(activity=discord.Game(name="Perros Development"))
    else:
        await client.change_presence(activity=discord.Game(name="gametec.org"))
        with open("profilepic.png", "rb") as image:
            await client.user.edit(avatar=image.read())

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                client.load_extension(f"cogs.{filename[:-3]}")
                print(f"Loaded {filename[:-3]}")
            except Exception as e:
                print(f"Failed to load {filename[:-3]}\n{e}")
    if dev_mode == "true":
        await client.register_application_commands(guild=discord.Object(guild_id))
    else:
        await client.register_application_commands()
    print("------")


def bot_main():
    client.run(token)


# run bot standalone
if __name__ == "__main__":
    bot_main()
