from datetime import datetime
import asyncio

import discord

from update_proposal_status import update_proposal_status


async def update_points(
    current_points: dict,
    lock: asyncio.Lock,
    proposal_times: dict[int, datetime],
    bot: discord.ext.commands.Bot,
    add: bool,
    user: discord.User,
    reaction: discord.Reaction,
) -> None:
    if user == bot.user:
        return
    message = reaction.message
    if len(message.embeds) == 0 or message.embeds[0].title != "Projekt-Pitch":
        return

    delta = 0
    if str(reaction.emoji) == "👎":
        delta = 10
    elif str(reaction.emoji) == "🤔":
        delta = 3
    if delta == 0:
        return

    async with lock:
        if message.id not in current_points:
            current_points[message.id] = int(message.embeds[0].fields[1].value)

        if add:
            current_points[message.id] += delta
        else:
            current_points[message.id] = max(0, current_points[message.id] - delta)

        new_points = current_points[message.id]

        embed = message.embeds[0].copy()
        embed.set_field_at(1, name="Punktestand", value=str(new_points), inline=False)

        try:
            await message.edit(embed=embed)
        except discord.errors.HTTPException:
            # If edit fails, reset the points to ensure consistency
            current_points[message.id] = int(message.embeds[0].fields[1].value)

    await update_proposal_status(proposal_times, reaction.message, embed, new_points)
