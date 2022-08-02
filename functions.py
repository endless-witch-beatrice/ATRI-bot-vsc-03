import io
import json
import random
from string import ascii_lowercase

import aiohttp, asyncio
from bs4 import BeautifulSoup

from atriconfig import TENOR_API_KEY, headers


async def get_gif_from_tenor(search_term):
    search_term = randomize_search(search_term)
    lmt = 1
    ckey = "ATRI"
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f'https://tenor.googleapis.com/v2/search?q={search_term}&key={TENOR_API_KEY}&client_key={ckey}&limit={lmt}') as r:
            if r.status == 200:
                top_gifs = json.loads(await r.text())
                gif = top_gifs["results"][0]["url"]
            else:
                gif = None
    return gif

def choose_headpat(headpat_type):

    match headpat_type:
        case "comfort":
            key = "comfort pat"
        case "pig":
            key = "pig"
        case "goodgirl":
            key = "good girl"
        case "boy":
            key = "boy patted"
        case "tiny":
            key = "tiny"
        case "robot":
            key = "robot"
        case "dog":
            key = "dog"
        case "cat":
            key = "cat"
        case "3dgirl":
            key = "human girl"
        case _:
            key = "ordinary pat-pats"

    return key

def randomize_search(search_term):
    if search_term is None:
        search_term = f"{random.choice(ascii_lowercase)} cute anime {str(random.randint(0, 20))} "
    else:
        search_term += f" cute {random.choice(ascii_lowercase)} anime "

    for _ in range(random.randint(2,8)):
        search_term += search_term.join(random.choice(ascii_lowercase))

    return search_term

async def get_maid_data():
    reddit_maid_link = "https://www.reddit.com/r/ImaginaryMaids/top/?t=week"
    maid_image_links = []
    async with aiohttp.ClientSession() as session:
        async with session.get(reddit_maid_link, headers=headers) as resp:
            if resp.status != 200:
                return
            soup = BeautifulSoup(await resp.text(), "lxml")
            images = soup.findAll('img')
            for image in images:
                if image.get("alt") == "Post image":
                    maid_image_links.append(image["src"])
    async with aiohttp.ClientSession() as session2:
        async with session2.get(random.choice(maid_image_links), headers=headers) as resp2:
            if resp2.status != 200:
                return
            return io.BytesIO(await resp2.read())