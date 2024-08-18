import asyncio
from datetime import datetime

import discord
from discord.ext import commands

from update_proposal_status import update_proposal_status


async def check_proposal_ages(
    proposal_times: dict[int, datetime], bot: commands.Bot
) -> None:
    await bot.wait_until_ready()
    while not bot.is_closed():
        for guild in bot.guilds:
            for channel in guild.text_channels:
                try:
                    async for message in channel.history(limit=None):
                        if (
                            len(message.embeds) > 0
                            and message.embeds[0].title
                            == "Neuer Projekt-Pitch erfolgreich erstellt!"
                        ):
                            embed = message.embeds[0]
                            current_points = int(embed.fields[1].value)
                            await update_proposal_status(
                                proposal_times, message, embed, current_points
                            )
                except discord.errors.Forbidden:
                    continue
                except Exception as e:
                    print(f"Error checking channel {channel.name} in {guild.name}: {e}")

        await asyncio.sleep(3600)
