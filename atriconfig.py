import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")
GUILD_IDS = []
GUILD_IDS.append(int(os.getenv("MAIN_GOLDEN_LAND_GUILD_ID")))
GUILD_IDS.append(int(os.getenv("OLD_GOLDEN_LAND_GUILD_ID")))
GUILD_IDS.append(int(os.getenv("NEZUMI_GUILD_ID")))

TENOR_API_KEY = os.getenv("TENORAPI")

yes_or_no = ("images-atri/ATRI-no.jpg", "images-atri/ATRI-yes.jpg")
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }