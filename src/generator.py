import markovify

def build_model(filePath):
    with open(filePath) as file:
        text = file.read()

    text_model = markovify.NewlineText(text)
    for i in range(5):
        print(text_model.make_sentence())