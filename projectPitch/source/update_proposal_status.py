from datetime import datetime, timedelta

import discord


async def update_proposal_status(
    proposal_times: dict[int, datetime],
    message: discord.Message,
    embed: discord.Embed,
    current_points: int,
) -> None:
    creation_time = proposal_times.get(message.id)
    if creation_time is None:
        return
    time_passed = datetime.now() - creation_time
    if current_points > 10:
        embed.set_field_at(0, name="Status", value="Blockiert", inline=False)
        embed.color = discord.Color.red()
    elif time_passed >= timedelta(days=14) and current_points <= 10:
        embed.set_field_at(0, name="Status", value="Zugestimmt", inline=False)
        embed.color = discord.Color.green()
    else:
        embed.set_field_at(0, name="Status", value="Im Gange", inline=False)
        embed.color = discord.Color.blue()
    await message.edit(embed=embed)
