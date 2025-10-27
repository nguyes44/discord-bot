import discord
import random
import os
from discord.ext import commands
from dotenv import load_dotenv

# discord channel ID that appears in browser URL
# ex. 123 / 456
# 2nd part is channel ID
load_dotenv()
channel_id = os.getenv("TEST_CHANNEL")
api_key = os.getenv("API_KEY")

# Define which intents you want to use
intents = discord.Intents.default()  # This enables the default intents
intents.messages = True  # Enable the message intent if not already covered by default
intents.message_content = True  # Necessary to read message content

# Create the bot instance with the specified intents
bot = commands.Bot(command_prefix='!', intents=intents)

# runs automatically when the bot is started
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# runs when the bot detects a !r message in the channel specified by FETCH_CHANNEL
@bot.command()
async def r(ctx):
    target_channel = (bot.get_channel(channel_id) or await bot.fetch_channel(channel_id))
    if target_channel is None:
        await ctx.send("Could not find the target channel.")
        return
    
    videos = []

    # Fetch messages from the channel
    async for message in target_channel.history(limit=20000):
        for attachment in message.attachments:
            if any(attachment.filename.endswith(ext) for ext in ['.mp4', '.webm']):
                videos.append(attachment.url)

    if videos:
        video_url = random.choice(videos)
        await ctx.send(f'Random video: {video_url}')
    else:
        await ctx.send("No videos found in this channel.")



if __name__ == "__main__":
    bot.run(api_key)