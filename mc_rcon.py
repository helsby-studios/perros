from mcrcon import MCRcon
import os
from dotenv import load_dotenv

load_dotenv()
MC_RCON_PASSWORD = os.getenv('MC_RCON_PASSWORD')
MC_RCON_HOST = os.getenv('MC_RCON_HOST')

mcr = MCRcon(MC_RCON_HOST, MC_RCON_PASSWORD)

def whitelist_player(player_name):
    mcr.connect()
    mcr.command("whitelist add " + player_name)
    mcr.disconnect()

def unwhitelist_player(player_name):
    mcr.connect()
    mcr.command("whitelist remove " + player_name)
    mcr.disconnect()

def banlist():
    mcr.connect()
    result = mcr.command("banlist")
    mcr.disconnect()

    if result != "There are no bans":
        result = result.split(".")
        wip = result[0].split(":", 1)
        wip.pop(0)
        result.pop(0)
        result.insert(0, wip[0])
        result.pop(len(result) - 1)
        return result
    else:
        return None
