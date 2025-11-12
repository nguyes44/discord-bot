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
video_count = os.getenv("VIDEO_COUNT")
cache_location = os.getenv("CACHE_LOCATION")

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
    async for message in read_channel.history(limit=15000):
        for attachment in message.attachments:
            if any(attachment.filename.endswith(ext) for ext in ['.mp4', '.webm']):
                videos.append(attachment.url)

    # check cache
    with open(cache_location, "r") as file:    
        lines = file.read().splitlines()
        line_count = len(lines)

    # purge cache if necessary
    if line_count >= int(video_count):
        with open(cache_location, "w"):
            pass

    if videos:

        fetch_count = 0
        fetch_max = 5                               # to avoid infinite loops
        while fetch_count < fetch_max:
            video_url = random.choice(videos)       # fetch url

            if video_url in lines:                  # if cache contains
                video_url = random.choice(videos)   # get another
                fetch_count += 1
            else:                                   # otherwise, write url to cache
                with open(cache_location, "a") as file:
                    file.write(video_url + "\n")
                break

        await post_channel.send(f'Random video: {video_url}')
    else:
        await post_channel.send("Somebody fix the damn bot bruh, acc tweaking.")

    quit(0)

if __name__ == "__main__":
    bot.run(api_key)