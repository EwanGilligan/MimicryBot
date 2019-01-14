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
    if message.content.startswith("!mimicry_setup"):
        await client.send_message(message.channel, "Setting up")
        await read_message_history(message.server)
    if message.content.startswith("!mimic"):
        await mimic_fusion(message)


async def read_message_history(server):
    # Gets all channels the client has access to
    for channel in server.channels:
        # Gets all the messages from each client.
        async for message in client.logs_from(channel, limit=credentials["message_limit"]):
            # Writes the messages to the file listed by the users name
            if message.author != client.user:
                await write_message(message)


async def write_message(message):
    # Filepath is created from the author of the message.
    filePath = credentials["data_path"] + '/' + message.author.id + ".txt"
    with open(filePath, 'a+') as file:
        # Writes the message content to the file.
        file.write(message.content + '\n')


async def generate_sentence(ids):
    filePaths = []
    for id in ids:
        # Filepath for the generated sentence.
        filePaths.append(credentials["data_path"] + '/' + id + ".txt")
    # Builds the model
    model = generator.build_model(filePaths)
    # Creates a sentence
    sentence = model.make_sentence()
    # Alternative for if the sentence creation fails.
    if sentence is None:
        current_tries = 100
        limit = credentials["maximum_attempts"]
        while sentence is None and current_tries < limit:
            sentence = model.make_sentence(tries=current_tries)
            current_tries *= 10
        # Behaviour for if it still fails.
        if sentence is None:
            return "Unable to generate sentence."
    else:
        return sentence


# Redundant.
async def mimic(message):
    # Checks first that the message is of the correct format.
    if re.search("^!mimic [0-9]{18}$", message.content):
        # Generates the sentence with the chosen id.
        ID = str(re.search("[0-9]{18}", message.content).group())
        sentence = await generate_sentence(ID)
        await client.send_message(message.channel, sentence)
    else:
        await client.send_message(message.channel, "Invalid syntax.")


async def mimic_fusion(message):
    # Checks first that the message is of the correct format.
    if re.search("^!mimic (([0-9]{18})|([0-9]{18} )+([0-9]{18}))$", message.content):
        # Finds all the ids to use.
        ids = re.findall("([0-9]{18})", message.content)
        # Generates the sentence.
        sentence = await generate_sentence(ids)
        # Sends the sentence.
        await client.send_message(message.channel, sentence)
    else:
        await client.send_message(message.channel, "Invalid syntax.")


def run():
    client.run(credentials["token"])
