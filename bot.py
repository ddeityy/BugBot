import os
import discord
from dotenv import load_dotenv
import random
import datetime
from moviepy.editor import VideoFileClip
from pygifsicle import optimize

load_dotenv()
TOKEN = os.getenv('TOKEN')

client = discord.Client(intents=discord.Intents.all())
coconut = '<:emoji_17:1022025700875718677>'

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

counter: int = 7000

lowest_roll: float = 0.0005

def mp4_to_gif(message):

    res = 0.05

    while os.stat("gif.gif").st_size > 8388608:
        video_clip = VideoFileClip("video.mp4").resize(float(message.content) - res)
        video_clip.write_gif("gif.gif", fps=video_clip.fps, program='ffmpeg')
        optimize("gif.gif")
        res += 0.05

@client.event
async def on_message(message):

    global counter
    global lowest_roll

    if message.author == client.user:
        return

    if not message.guild and message.attachments and message.attachments[0].url.endswith("mp4"):

        await message.attachments[0].save("video.mp4")

        videoClip = VideoFileClip("video.mp4")

        videoClip.write_gif("gif.gif", fps=videoClip.fps, program='ffmpeg')

        optimize("gif.gif")

        if message.content:
            mp4_to_gif(message)

        await message.channel.send(file=discord.File("gif.gif"))

        os.remove("gif.gif")
        os.remove("video.mp4")

    if message and message.guild:
        time = datetime.datetime.now()
        time_strf = time.strftime("%d.%m.%Y %H:%M:%S")
        roll = round(random.random(), 4)
        counter += 1
        lowest_roll = min(roll, lowest_roll)
        print(f'{time_strf}:  {str(roll)} | {message.author.name}: {message.content}  {counter}')
        if roll == 0.0001:
            await message.add_reaction(coconut)
            await message.channel.send(f'@everyone\n@{message.author.name} got absolutely cock nutted :coconut: :elephant: :coconut:')
            await message.channel.send(f'https://media.discordapp.net/attachments/955476947784335410/1039129118480023552/00015-3038639051.png')
            await message.channel.send(f'It only took {counter} messages!')
            counter = 0
            lowest_roll = 0.0

    if "$lowest_roll" in message.content.lower():
        await message.reply(lowest_roll)

    if "bug" in message.content.lower():
        await message.add_reaction("🐛")

client.run(TOKEN)
