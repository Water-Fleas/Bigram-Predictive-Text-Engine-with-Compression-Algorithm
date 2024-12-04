import json
from queue import PriorityQueue

class PredictiveTextEngine:
    bigram = None
    known_words = None

    def __init__(self, filepath, filepath_dict):
        self.bigram = self.load_file(filepath)
        self.known_words = self.load_file(filepath_dict)

    def predict_word(self, previous, current):
        node = self.known_words
        legal_words = self.find_words(node, current)
        if legal_words == None:
            print(f"no legal words compress to this {current}")
            return set()
        
        pq = PriorityQueue()
        if previous not in self.bigram:
            print(f'{previous} not in bigram')
            return set()
        
        for item in self.bigram[previous]:
            if item in legal_words:
                pq.put((self.bigram[previous][item]*-1, item))
        
        guesses = set()
        for i in range(min(3,pq.qsize())):
            guesses.add(pq.get()[1])

        return guesses

    def find_words(self, node, current): # scuffed but it works and i refuse to touch it any more
        node = self.known_words
        words = set()
        for char in current:
            if char not in node:
                return
            node = node[char]

        if "_end" in node:
            words.update(node["_end"])

        for char, child in node.items():
            if char != "_end":
                words.update(self.find_words(child, current + char))

        return words

    def load_file(self, filepath):
        try:
            with open(filepath, "r") as file:
                corpus = json.load(file)
        except FileNotFoundError:
            print("The file was not found.")
        except json.JSONDecodeError:
            print("Invalid JSON format.")
        return corpus

