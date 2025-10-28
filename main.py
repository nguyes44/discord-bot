import discord
import random
import os
from discord.ext import commands
from dotenv import load_dotenv

# discord channel ID that appears in browser URL
# ex. 123 / 456
# 2nd part is channel ID
load_dotenv()
read_channel_id = os.getenv("PROD_READ_CHANNEL")
post_channel_id = os.getenv("PROD_POST_CHANNEL")
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
    read_channel = (bot.get_channel(read_channel_id) or await bot.fetch_channel(read_channel_id))
    post_channel = (bot.get_channel(post_channel_id) or await bot.fetch_channel(post_channel_id))
    videos = []

    # Fetch messages from the channel
    async for message in read_channel.history(limit=100000):
        for attachment in message.attachments:
            if any(attachment.filename.endswith(ext) for ext in ['.mp4', '.webm']):
                videos.append(attachment.url)

    if videos:
        video_url = random.choice(videos)
        await post_channel.send(f'Random video: {video_url}')
    else:
        await post_channel.send("No videos found in this channel.")

    quit(0)

if __name__ == "__main__":
    bot.run(api_key)