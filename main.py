import os
import threading
import bot
from dotenv import load_dotenv
from quart import Quart, redirect, render_template, url_for
from quart_discord import DiscordOAuth2Session


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
    try:
        await discord.callback()
    except Exception:
        pass

    return redirect(url_for("dashboard"))


if __name__ == "__main__":  # run webserver
    thread.start()
    app.run(debug=True, port=80)
