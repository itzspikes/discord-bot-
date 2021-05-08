import discord
from discord import client, member
from discord.ext import commands
import youtube_dl
import os

bot = discord.Client()

client = commands.Bot(command_prefix="!")

@client.command()
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


@bot.event
async def on_message(message):
    # do something with message
    print(message.content)

    if message.content == 'hello spikes bot':
        await message.channel.send('hello!')
    if message.content == 'Hello Everything Bot':
        await message.channel.message.send('hello!')
    if message.content == 'how are you':
        await message.channel.send('i am good how are you')
    if message.content == 'i am good':
        await message.channel.send('that is good')
    if message.content == 'not good':
        await message.channel.send('that is not good think happy thoughts :)')
    if message.content == 'im fine':
        await message.channel.send('that is ok what can make this day better')
    if message.content == 'i will be fine':
        await message.channel.send('what is wrong')
    if message.content == 'i dont know':
        await message.channel.send('how do you not know who you are feeling?')
    if message.content == 'tell me a joke':
        await message.channel.send('what does a cucumber have to do to become a pickle he has to go through a jarring experience')



bot.run('')
