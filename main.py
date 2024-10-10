import os
from typing import List, Optional
from dotenv import load_dotenv
import discord

from discord.guild import Guild, VoiceChannel
from discord.member import Member, VoiceState
from discord.channel import CategoryChannel


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

FOCUS_CHANNEL_NAME = "create-lobby"
CATEGORY = "LOBBY"


@client.event
async def on_voice_state_update(member: Member, before: VoiceState, after: VoiceState):
    guild: Guild = member.guild

    voice_channels = await delete_empty_voice_channels(guild=guild)
    await delete_category_without_voice_channel(guild=guild, voice_channels=voice_channels)

    if after.channel is None:
        return

    if not hasattr(after.channel, "name"):
        return

    if after.channel.name != FOCUS_CHANNEL_NAME:
        return

    await make_channel(guild=guild, member=member)


def get_category(guild: Guild) -> Optional[CategoryChannel]:
    return next((x for x in guild.categories if x.name == CATEGORY), None)


async def make_channel(guild: Guild, member: Member):
    category = get_category(guild=guild)
    if category is None:
        category = await guild.create_category(CATEGORY)

    channel = await guild.create_voice_channel(
        f"{member.name.capitalize()} | Lobby",
        category=category,
        user_limit=5
    )
    await member.move_to(channel)


async def delete_empty_voice_channels(guild: Guild) -> List[VoiceChannel]:
    channels = [x.voice_channels for x in guild.categories if x.name == CATEGORY]
    if not channels or channels == []:
        return []
    voice_channels = channels[0]
    for x in voice_channels:
        if x.members != []:
            continue
        voice_channels = [x for x in voice_channels if x.name != x.name]
        await x.delete()
    return voice_channels


async def delete_category_without_voice_channel(guild: Guild, voice_channels: List[VoiceChannel]):
    if not voice_channels == []:
        return
    category = get_category(guild=guild)
    if category is not None:
        await category.delete()


class TokenException(Exception):
    pass


def main():
    load_dotenv()
    TOKEN = os.getenv("TOKEN")
    if not TOKEN:
        raise TokenException("Provide token")
    client.run(os.getenv("TOKEN"))


if __name__ == "__main__":
    main()
