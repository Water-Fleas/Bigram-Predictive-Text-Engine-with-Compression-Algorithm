import json
import numpy as np
from createBigram import createBigram
import pte
import re
from trieCreation import compression

def load_file(filepath):
    try:
        with open(filepath, "r") as file:
            corpus = json.load(file)
    except FileNotFoundError:
        print("The file was not found.")
    except json.JSONDecodeError:
        print("Invalid JSON format.")
    return corpus

def load_words(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
    return lines


k = 5

total_corpus = load_file("processedUtterances.json") # list of comments (strings)
known_words = load_file("knownWords.json") # prepared beforehand
known_words_uncompressed = set()
for word in load_words('allwords.txt'):
    known_words_uncompressed.add(word)

corpus_array = np.array(total_corpus)
np.random.shuffle(corpus_array)

record = []
attempts = 0
successes = 0
utterancenum = 0
testing_set = corpus_array[:1000]
training_set = corpus_array[1000:]
    
createBigram(training_set) # dumps a bigram into bigram.json
pte_instance = pte.PredictiveTextEngine("bigram.json", "knownWords.json")

for utterance in testing_set:
    last_word = '<s>'
    utterancenum +=1
    print(utterancenum)
    for upword in utterance.split():
        word = "".join(re.findall(r"\b[a-zA-Z]+(?:['-][a-zA-Z]+)*\b", upword))
        if word not in known_words_uncompressed:
            last_word = word
            continue
        attempts +=1
        compressed_word = compression(word)

        current_attempt = 0
        success = False
        for z in range(len(compressed_word)):
            current_attempt+=1
            predictions = pte_instance.predict_word(last_word, compressed_word[:z])
            if word in predictions:
                success = True
                successes+=1
                break
        record.append((success, len(compressed_word)-current_attempt))
        last_word = word

print(attempts)
print(successes)
with open('record.json', 'w', encoding='utf-8') as file:
    json.dump(record, file, indent=4)