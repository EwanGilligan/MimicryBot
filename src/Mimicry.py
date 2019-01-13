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
    if message.content.startswith("!mimicry_setup"):
        await client.send_message(message.channel, "Setting up")
        await read_message_history(message.server)


async def read_message_history(server):
    # Gets all channels the client has access to
    for channel in server.channels:
        # Gets all the messages from each client.
        async for message in client.logs_from(channel, limit=100):
            # Writes the messages to the file listed by the users name
            if message.author != client.user:
                print(message.content)
                await write_message(message)


async def write_message(message):
    filePath = credentials["data_path"] + '/' + message.author.id
    with open(filePath, 'a+') as file:
        file.write(message.content + '\n')


client.run(credentials["token"])
