import json
import re

def load_file(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
        return lines

def create_trie(filepath):
    word_list = load_file(filepath)
    the_holy_trie = {}
    for word in word_list:
        compressed_word = compression(word)
        add_to_trie(the_holy_trie, compressed_word, word)
    
    with open('knownWords.json', 'w', encoding='utf-8') as file:
        json.dump(the_holy_trie, file, indent=4)

def add_to_trie(trie, word, og_word):
    node = trie
    # traversing trie
    for char in word:
        if char not in node:
            node[char] = {}
        node = node[char]
    # Add the word to the leaf node (stored as an array at the final level)
    if "_end" not in node:
        node["_end"] = []
    node["_end"].append(og_word)

def compression(word: str):
    new_word = word.lower()
    # extra step: removing non letter characters
    new_word = re.sub(r"[^\w]", "", new_word)
    # 5.1 Replace each occurrence of CE, CI , CY  S
    new_word = new_word.replace("ce", "s")
    new_word = new_word.replace("ci", "s")
    new_word = new_word.replace("cy", "s")
    # 5.2 Replace each occurrence of GE, GI, GY  J
    new_word = new_word.replace("ge", "j")
    new_word = new_word.replace("gi", "j")
    new_word = new_word.replace("gy", "j")
    # 5.3 Replace each occurrence of WR  R
    new_word = new_word.replace("wr", "r")
    # 5.4 Replace each occurrence of GN, KN, PN  N
    new_word = new_word.replace("gn", "n")
    new_word = new_word.replace("kn", "n")
    new_word = new_word.replace("pn", "n")
    # 5.5 Replace each occurrence of CK  K
    new_word = new_word.replace("ck", "k")
    # 5.6 Replace each occurrence of DGE  J
    new_word = new_word.replace("dge", "j")
    # 5.7 Replace each occurrence of OUL  U
    new_word = new_word.replace("oul", "u")
    # 5.8 Replace each occurrence of OUGH  F
    new_word = new_word.replace("ough", "f")
    # 5.9 Replace each occurrence of SH  S
    new_word = new_word.replace("sh", "s")
    # 5.10 Replace each occurrence of GHT  T
    new_word = new_word.replace("ght", "t")
    # 6. Remove all the vowels from the resultant target text except if it is the first character of the given text.
    return new_word[0]+"".join([char for char in new_word[1:] if char not in "aeiouy"])

create_trie('allwords.txt')