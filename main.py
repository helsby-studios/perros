import subprocess
import os
import sys
import time
import random
import json
import discord
import asyncio
import requests
import datetime
import mariadb
import threading
import bot
from quart import Quart, render_template, request, session, redirect, url_for
from quart_discord import DiscordOAuth2Session
from dotenv import load_dotenv

#start bott
thread = Thread(target=bot.run)
thread.start()

#load envs
load_dotenv()
db_user = os.getenv("DB_USER")
db_passwd = os.getenv("DB_PASSWD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_db = os.getenv("DB_DB")
token = os.getenv("DISCORD_TOKEN")
ipc_secret_key = os.getenv("IPC_SECRET_KEY")
dc_client_id = os.getenv("DISCORD_CLIENT_ID")
dc_client_secret = os.getenv("DISCORD_CLIENT_SECRET")
dc_callback_uri = os.getenv("DISCORD_CALLBACK_URI")

#connect to db
try:
    db = mariadb.connect(
        user=db_user,
        password=db_passwd,
        host=db_host,
        port=int(db_port),
        database=db_db
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)
cur = db.cursor()

#database functions
def create_table(table):
    sql = "CREATE TABLE IF NOT EXISTS %s (setting VARCHAR(255), value VARCHAR(255))" % table
    cur.execute(sql)

def insert(table, setting, value):
  sql = "INSERT INTO %s (setting, value) VALUES (%s, %s)"
  val = (table, setting, value)
  cur.execute(sql, val)
  cur.commit()


def read_all(table):
  mycursor.execute("SELECT * FROM %s" % table)
  result = cur.fetchall()
  for x in result:
    return x

def read_one(table, setting):
  mycursor.execute("SELECT value FROM %s WHERE setting=%s" % table % setting)
  result = cur.fetchone()
  return result

def update(table, setting, value):
    sql = "UPDATE %s SET value=%s WHERE setting=%s"
    val = (table, value, setting)
    cur.execute(sql, val)
    cur.commit()

def delete(table, setting):
    sql = "DELETE FROM %s WHERE setting=%s"
    val = (table, setting)
    cur.execute(sql, val)
    cur.commit()

#initiailize app
app = Quart(__name__)
ipc_client = ipc.Client(secret_key = ipc_secret_key)
app.config["SECRET_KEY"] = ipc_secret_key
app.config["DISCORD_CLIENT_ID"] = dc_client_id   
app.config["DISCORD_CLIENT_SECRET"] = dc_client_secret
app.config["DISCORD_REDIRECT_URI"] = dc_callback_uri
discord = DiscordOAuth2Session(app)

#setup webserver
@app.route("/")
async def home():
	return await render_template("index.html", authorized = await discord.authorized)

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


if __name__ == "__main__": #run webserver
	app.run(debug=True, port=80)