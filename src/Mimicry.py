import discord
import json
import generator
import re

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
    if message.content.startswith("!mimic"):
        await mimic(message)




async def read_message_history(server):
    # Gets all channels the client has access to
    for channel in server.channels:
        # Gets all the messages from each client.
        async for message in client.logs_from(channel, limit=10000):
            # Writes the messages to the file listed by the users name
            if message.author != client.user:
                await write_message(message)


async def write_message(message):
    filePath = credentials["data_path"] + '/' + message.author.id + ".txt"
    with open(filePath, 'a+') as file:
        file.write(message.content + '\n')

async def generate_sentence(ID):
    filePath = credentials["data_path"] + '/' + ID + ".txt"
    model = generator.build_model(filePath)
    return model.make_sentence()


async def mimic(message):
    #Checks first that the message is of the correct format.
    if re.search("!mimic [0-9]{18}", message.content):
        #Generates the sentence with the chosen id.
        sentence  = await generate_sentence(str(re.search("[0-9]{18}", message.content).group()))
        await client.send_message(message.channel, sentence)
    else:
        await client.send_message(message.channel, "Invalid syntax")




client.run(credentials["token"])
