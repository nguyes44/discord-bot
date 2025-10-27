import discord
from discord.ext import commands, tasks
from datetime import datetime, time, timedelta
import random


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    send_random_video.start()  # Start the loop when the bot is ready

async def get_random_video_url(channel):
    videos = []
    async for message in channel.history(limit=200):
        for attachment in message.attachments:
            if any(attachment.filename.endswith(ext) for ext in ['.mp4', '.webm']):
                videos.append(attachment.url)
    return random.choice(videos) if videos else None

@tasks.loop(time=time(hour=9, minute=0))  # Set to run at 3:00 PM server time every day
async def send_random_video():
    channel = bot.get_channel("")  # Replace with your channel ID
    if channel:
        video_url = await get_random_video_url(channel)
        if video_url:
            await channel.send(f'Random video: {video_url}')
        else:
            await channel.send("No videos found in this channel.")

bot.run("")
