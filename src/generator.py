import markovify

def build_model(filePaths):
    models = []
    for filePath in filePaths:
        with open(filePath) as file:
            text = file.read()
        models.append(markovify.NewlineText(text))
    text_model = markovify.combine(models)
    return text_model