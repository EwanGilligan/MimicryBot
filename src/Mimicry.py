import discord
import json

with open("credentials.json") as credentialsFile:
    credentials = json.load(credentialsFile)

client = discord.Client()

@client.event
async def on_ready():
    print("Squawk")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == "Hello":
        await client.send_message(message.channel, "Squawk")

client.run(credentials["token"])

