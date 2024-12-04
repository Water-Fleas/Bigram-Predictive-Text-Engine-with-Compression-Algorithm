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

def preprocess_comment(text):
    text = text.lower()
    replacements = [
        (r"\[removed\]|\[link\]|\[deleted\]", ""),
        (r"\[.*?\]\(.*?\)", ""),
        (r"&gt;|&mdash;|&amp;|&quot;", ""),
        (r"&[#\w]+(?:;\s*|(?=\s))|[#*^_~]|>!|!<", ""),
        (r"\[\s*\]|http\S+|\b\w+\.\w{2,3}(/\S*)?\b|\S+@\S+", ""),
        (r"(_+)(\w+)(_+)", r"\2"),
        (r'\s+', ' '),
        (r'/u/\S+', ''),
        (r'/r/\S+', ''),
        (r"[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U0001FB00-\U0001FBFF]", ""),
    ]
    for pattern, repl in replacements:
        text = re.sub(pattern, repl, text)
    
    return text

def refine_corpus(filepath):
    corpus = load_corpus(filepath)

    refined_corpus = []
    for utterance in corpus:
        if not utterance["user"] == "AutoModerator":
            refined_corpus.append(preprocess_comment(utterance["text"]))

    with open('processedUtterances.json', 'w') as file:
        json.dump(refined_corpus, file)

refine_corpus("utterances.json")