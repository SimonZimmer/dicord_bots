from datetime import datetime
from os import getenv
import logging
import asyncio

import discord

from check_proposal_ages import check_proposal_ages
from update_points import update_points


intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True

bot = discord.ext.commands.Bot(command_prefix="!", intents=intents)

proposal_times: dict[int, datetime] = dict()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

points_lock = asyncio.Lock()
current_points: dict[int, int] = {}


@bot.event
async def on_ready() -> None:
    print(f"Bot is ready. Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
    bot.loop.create_task(check_proposal_ages(proposal_times, bot))


@bot.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User) -> None:
    logging.info(f"Reaction added: {reaction.emoji} by {user}")
    await update_points(
        current_points, points_lock, proposal_times, bot, True, user, reaction
    )


@bot.event
async def on_reaction_remove(reaction: discord.Reaction, user: discord.User) -> None:
    logging.info(f"Reaction removed: {reaction.emoji} by {user}")
    await update_points(
        current_points, points_lock, proposal_times, bot, False, user, reaction
    )


@bot.tree.command(name="pitch", description="Erstelle einen neuen Projekt-Pitch")
@discord.app_commands.describe(proposal="Projekt-Pitch den du vorstellen möchtest")
async def proposal(interaction: discord.Interaction, proposal: str) -> None:
    embed = discord.Embed(
        title="Projekt-Pitch",
        description=proposal,
        color=discord.Color.blue(),
    )
    embed.add_field(name="Status", value="Im Gange", inline=False)
    embed.add_field(name="Punktestand", value="0", inline=False)
    embed.set_footer(
        text="Reagiere mit 👎 um Abneigung auszudrücken (10 Punkte) oder mit 🤔 wenn du Bedenken hast (3 Punkte). Bei mehr als 10 Punkten gilt das Projekt als blockiert und es besteht weiterer Redebedarf."
    )
    message = await interaction.channel.send(embed=embed)
    await message.add_reaction("👎")
    await message.add_reaction("🤔")
    proposal_times[message.id] = datetime.now()
    await interaction.response.send_message(
        "Projekt-Pitch erfolgreich erstellt!", ephemeral=True
    )


bot.run(getenv("ABOT_TOKEN"))
