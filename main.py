import os
import threading

import bot
from dotenv import load_dotenv
from quart import Quart, redirect, render_template, url_for
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

# start bot
thread = threading.Thread(target=bot.bot_main)

# load envs
load_dotenv()
token = os.getenv("DISCORD_TOKEN")
dc_client_id = os.getenv("DISCORD_CLIENT_ID")
dc_client_secret = os.getenv("DISCORD_CLIENT_SECRET")
dc_callback_uri = os.getenv("DISCORD_CALLBACK_URI")

# initiailize app
app = Quart(__name__)
app.secret_key = b"TiV7TDXK39uNgaLtwB7EXkfoZfQpJ615vDKqgPHaMXoFsJUBWMebg4pAQhj9cyWc8AAKVXQ3ha1jh12DsCoW58KQL3T4KcaPHQmM" # key used to sign session cookies
app.config["DISCORD_CLIENT_ID"] = dc_client_id
app.config["DISCORD_CLIENT_SECRET"] = dc_client_secret
app.config["DISCORD_REDIRECT_URI"] = dc_callback_uri
discord = DiscordOAuth2Session(app)


# setup webserver
@app.route("/")
async def home():
    return await render_template("index.html", authorized=await discord.authorized)


@app.route("/login")
async def login():
    return await discord.create_session()


@app.route("/logout")
async def logout():
    discord.revoke()
    return redirect(url_for("home"))


@app.route("/callback")
async def callback():
    await discord.callback()
    return redirect(url_for("dashboard"))


@app.errorhandler(Unauthorized)
async def redirect_unauthorized(e):
    return redirect(url_for("login"))


@app.route("/dashboard")
@requires_authorization
async def dashboard():
    guild_count = await bot.get_guild_count()
    guild_ids = await bot.get_guild_ids()
    user_guilds = await discord.fetch_guilds()
    guilds = []
    for guild in user_guilds:
        if guild.permissions.administrator or guild.permissions.manage_guild or guild.permissions.manage_messages:
            guild.class_color = "green-border" if guild.id in guild_ids else "red-border"
            guilds.append(guild)

    guilds.sort(key=lambda x: x.class_color == "red-border")
    name = (await discord.fetch_user()).name
    return await render_template("dashboard.html", guild_count=guild_count, guilds=guilds, username=name)


@app.route("/dashboard/<int:guild_id>", methods=["POST", "GET"])
@requires_authorization
async def dashboard_server(guild_id):
    if not await discord.authorized:
        return redirect(url_for("login"))
    guild = await bot.get_guild(guild_id)
    if guild is None:
        return redirect(
            f'https://discord.com/oauth2/authorize?&client_id={app.config["DISCORD_CLIENT_ID"]}&scope=bot&permissions=534723951680&guild_id={guild_id}&response_type=code&redirect_uri={app.config["DISCORD_REDIRECT_URI"]}')
    # return guild["name"]
    return await render_template("ui.html", guild=guild["name"], guild_id=guild_id)

if __name__ == "__main__":  # run webserver
    thread.start()
    app.run(debug=True, port=80)
