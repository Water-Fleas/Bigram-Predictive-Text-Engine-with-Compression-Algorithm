import json
import re

def load_corpus(filepath):
    try:
        with open(filepath, "r") as file:
            corpus = json.load(file)
    except FileNotFoundError:
        print("The file was not found.")
    except json.JSONDecodeError:
        print("Invalid JSON format.")
    return corpus

def createBigram(corpus):
    last_word = "<s>"
    bigram = {}
    for utterance in corpus:
        for upword in utterance.split():
            word = "".join(re.findall(r"\b[a-zA-Z]+(?:['-][a-zA-Z]+)*\b", upword))
            if word == "":
                continue
            if last_word not in bigram:
                bigram[last_word] = {}
            if word not in bigram[last_word]:
                bigram[last_word][word] = 0
            bigram[last_word][word]+=1
            last_word = word
        last_word = '<s>'

    with open('bigram.json', 'w', encoding='utf-8') as file:
        json.dump(bigram, file, indent=4)