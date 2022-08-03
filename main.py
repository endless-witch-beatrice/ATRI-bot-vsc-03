import json
import random
import aiohttp, asyncio


import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

import cooldowns
from cooldowns import CallableOnCooldown

from atriconfig import GUILD_IDS, yes_or_no, TOKEN
from functions import choose_headpat, get_gif_from_tenor, get_maid_data

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
        await interaction.send(f"Apologies, ATRI dosen't want to sleep yet.", ephemeral=True, delete_after=10)
    else:
        await interaction.response.send_message(f"Sweet dreams, {user.mention}")
        await interaction.followup.send(random.choice(g_nightgifs["regular goodnight"]))

@bot.slash_command(guild_ids=GUILD_IDS, name = "headpat", description="Atri headpats a user with a gif")
@cooldowns.cooldown(2, 90, bucket=cooldowns.SlashBucket.author)
async def headpat(interaction: Interaction,
                  user: nextcord.Member = SlashOption(name="username", description="whom do you want to pat? (optional)", required=False),
                  headpat_type:str = SlashOption(name="secret_code", description="don't touch this option, unless...", required=False)):

    with open('images-atri/headpatgifs.json') as f:
        headpats = json.load(f)

    key = choose_headpat(headpat_type)

    if user is None:
        await interaction.response.send_message(random.choice(headpats[key]))
    elif user == bot.user:
        await interaction.response.send_message(f"{interaction.user.name} pat-pats me :blush: ")
        await interaction.followup.send(random.choice(headpats["robot"]))
    elif user == interaction.user:
        await interaction.response.send_message(f"{interaction.user.name} pat-pats themselves.")
        await interaction.followup.send(random.choice(headpats["self"]))   
    else:
        await interaction.response.send_message(f"{interaction.user.name} pat-pats {user.mention}")
        await interaction.followup.send(random.choice(headpats[key]))

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

@bot.listen()
async def on_message(message):
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

bot.run(TOKEN)


