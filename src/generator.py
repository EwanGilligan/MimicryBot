import markovify

def build_model(filePath):
    with open(filePath) as file:
        text = file.read()

    text_model = markovify.NewlineText(text)
    return text_model