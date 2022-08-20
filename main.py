import json
import random
import aiohttp, asyncio

import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

import cooldowns
from cooldowns import CallableOnCooldown

from atriconfig import GUILD_IDS, yes_or_no, TOKEN
from functions import get_gif_from_tenor, get_maid_data

bot = commands.Bot(intents=nextcord.Intents.all())

@bot.event
async def on_ready():
    print(f"nextcord = {nextcord.__version__}")
    print(f"We have logged in as {bot.user}")

@bot.event
async def on_application_command_error(inter: nextcord.Interaction, error):
    error = getattr(error, "original", error)
    if isinstance(error, CallableOnCooldown):
        await inter.send(f"Apologies, you're being rate-limited! Retry in `{error.retry_after}` seconds.", ephemeral=True, delete_after=10)
    else:
        await inter.send(f"{error}", ephemeral=True, delete_after=10)

async def atri_sleep(interaction: Interaction, gif_atri_sleep:str):
    await interaction.response.send_message("I'm off to bed.  :robot: :zzz: ")
    await interaction.followup.send(gif_atri_sleep)
    await bot.change_presence(status=nextcord.Status.offline, activity=None)
    global is_invizible
    is_invizible = False

async def atri_wake_up(interaction: Interaction, gif_atri_wakingup:str):
    await interaction.response.send_message("Rising up for a new day.  :robot: :coffee:")
    await interaction.followup.send(gif_atri_wakingup)
    await bot.change_presence(status=nextcord.Status.online, activity=None)
    global is_invizible
    is_invizible = True

@bot.slash_command(guild_ids=GUILD_IDS, name ="yea_or_nay", description="Atri responds with either YES or NO")
@cooldowns.cooldown(4, 90, bucket=cooldowns.SlashBucket.author)
async def yesno(interaction: Interaction):
    await interaction.send(file=nextcord.File(random.choice(yes_or_no)))

@bot.slash_command(guild_ids=GUILD_IDS, name ="good_night", description="Atri readies a user for sleep")
@cooldowns.cooldown(1, 90, bucket=cooldowns.SlashBucket.author)
async def goodnight(interaction: Interaction, user:nextcord.Member = SlashOption(name="username", description="choose a user to tuck in", required=True)):
    with open('images-atri/goodnightgifs.json') as f:
        g_nightgifs = json.load(f)
    if user == interaction.user:
        await interaction.response.send_message(f"{user.name} is going to bed :sleeping:")
        await interaction.followup.send(random.choice(g_nightgifs["goodnight user self"]))
    elif user == bot.user:
        await atri_sleep(interaction, random.choice(g_nightgifs["atri"]))
    else:
        await interaction.response.send_message(f"Sweet dreams, {user.name}!")
        await interaction.followup.send(random.choice(g_nightgifs["regular goodnight"]))

@bot.slash_command(guild_ids=GUILD_IDS, name ="cute_gif", description="Atri fetches a random gif for you")
@cooldowns.cooldown(4, 90, bucket=cooldowns.SlashBucket.author)
async def cute_gif(interaction: Interaction, search_term:str = SlashOption(required=False)):
    await interaction.response.send_message(await get_gif_from_tenor(search_term))

@bot.slash_command(guild_ids=GUILD_IDS, name ="anime_maid", description="Atri posts a maid picture")
@cooldowns.cooldown(2, 6000, bucket=cooldowns.SlashBucket.guild)
async def anime_maid(interaction: Interaction):
    await interaction.response.defer()
    data = await get_maid_data()
    await interaction.send(file=nextcord.File(data, 'cutemaid.jpg'))

@bot.slash_command(guild_ids=GUILD_IDS, name = "hug", description="Atri hugs a user with a gif")
@cooldowns.cooldown(3, 90, bucket=cooldowns.SlashBucket.author)
async def hug(interaction: Interaction,
                  user: nextcord.Member = SlashOption(name="username", description="who do you want to cuddle with?", required=False),
                  hug_type:str = SlashOption(name="secret_code", description="don't touch this option, unless...", required=False)):

    with open('images-atri/huggifs.json') as f:
        hugs = json.load(f)

    if hug_type in ("toy", "ask", "dog", "cat"):
        key = hug_type
    else:
        key = "regularhugs"

    if user is None:
        await interaction.response.send_message(random.choice(hugs[key]))
    elif user == bot.user:
        await interaction.response.send_message(f"Apologies, {interaction.user.name}, I don't want to be hugged.")
        await interaction.followup.send(random.choice(hugs["failed"]))
    elif user == interaction.user:
        await interaction.response.send_message(f"{interaction.user.name} practices self-love by hugging themselves.")
        await interaction.followup.send(random.choice(hugs["self"]))   
    else:
        if key == "ask":
            await interaction.response.send_message(f"{interaction.user.name} offers a hug to {user.name}.")
        else:
            await interaction.response.send_message(f"{interaction.user.name} hugs {user.name}.")
        await interaction.followup.send(random.choice(hugs[key]))

@bot.slash_command(guild_ids=GUILD_IDS, name ="good_morning", description="Atri sends a good morning wish to a user")
@cooldowns.cooldown(1, 90, bucket=cooldowns.SlashBucket.author)
async def goodmorning(interaction: Interaction, user:nextcord.Member = SlashOption(name="username", description="choose a sleepy user", required=True)):
    with open('images-atri/goodmorninggifs.json') as f:
        g_morninggifs = json.load(f)
    if user == interaction.user:
        await interaction.response.send_message(f"{user.name} is waking up :face_with_hand_over_mouth: ")
        await interaction.followup.send(random.choice(g_morninggifs["goodmorning user self"]))
    elif user == bot.user:
        """ await interaction.send(f"Don't talk to me until I've had my coffee :robot: :coffee:", ephemeral=True, delete_after=10) """
        await atri_wake_up(interaction, random.choice(g_morninggifs["atri"]))
    else:
        await interaction.response.send_message(f"Good morning, {user.name}!")
        await interaction.followup.send(random.choice(g_morninggifs["regular goodmorning"]))

@bot.slash_command(guild_ids=GUILD_IDS, name = "headpat", description="Atri headpats a user with a gif")
@cooldowns.cooldown(3, 90, bucket=cooldowns.SlashBucket.author)
async def headpat(interaction: Interaction,
                  user: nextcord.Member = SlashOption(name="username", description="whom do you want to pat? (optional)", required=False),
                  headpat_type:str = SlashOption(name="secret_code", description="don't touch this option, unless...", required=False)):

    with open('images-atri/headpatgifs.json') as f:
        headpats = json.load(f)

    if headpat_type in ("comfort", "tiny", "goodgirl", "boy", "pig", "cat", "dog", "humangirl"):
        key = headpat_type
    else: 
        key = "ordinary pat-pats"

    if user is None:
        await interaction.response.send_message(random.choice(headpats[key]))
    elif user == bot.user:
        await interaction.response.send_message(f"{interaction.user.name} pat-pats me :blush: ")
        await interaction.followup.send(random.choice(headpats["robot"]))
    elif user == interaction.user:
        await interaction.response.send_message(f"{interaction.user.name} pat-pats themselves.")
        await interaction.followup.send(random.choice(headpats["self"]))   
    else:
        await interaction.response.send_message(f"{interaction.user.name} pat-pats {user.name}.")
        await interaction.followup.send(random.choice(headpats[key]))

@bot.listen()
async def on_message(message):
    streamcord_id = 375805687529209857
    streamcord_msg = "We're live at https://twitch.tv/nezumicraft"
    if message.author.id == streamcord_id and streamcord_msg in message.content:
        emoji = "👍"
        await message.add_reaction(emoji)
        watching_nezu = nextcord.Activity(type=nextcord.ActivityType.watching, name = "twitch.tv/nezumicraft")
        await bot.change_presence(status=nextcord.Status.dnd, activity=watching_nezu)
        await asyncio.sleep(9700)
        await bot.change_presence(status=nextcord.Status.online, activity=None)
        global is_invizible
        is_invizible = False
    if "crab" in message.content:
        emoji = "🦀"
        await message.add_reaction(emoji)
    if "Jordan Peterson" in message.content or "jordan peterson" in message.content:
        emoji = "🦞"
        await message.add_reaction(emoji)

try:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
except:
    pass

is_invizible = False
bot.run(TOKEN)


