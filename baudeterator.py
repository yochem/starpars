#!/usr/bin/env python3

import os

import nltk
nltk.download('punkt')

def tokenize_corpus(filename):
    """Tokenize the corpus and strip the newline characters (\n)."""
    script_path = os.path.abspath(os.path.dirname(__file__))

    if filename in os.listdir('.'):
        corpus_file = 'corpus.txt'
    elif filename in os.listdir(script_path):
        corpus_file = script_path + '/corpus.txt'
    else:
        raise FileNotFoundError

    with open(corpus_file) as f:
        cont = f.read()
        sentence_list = [l.replace('\n', ' ') for l in nltk.sent_tokenize(cont)]
        word_list = []
        for w in nltk.word_tokenize(cont):
            # don't add non-words
            if w != '.' and w != ',' and w != '?':
                word_list.append(w)

    return sentence_list, word_list


def analyze():
    """
    Print information about the corpus. The information contains:
    - 5 most used words;
    - Total word count;
    - Word count without duplicates (size vocab);
    - Sentence count.
    """
    word_count = {}

    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    top_words = sorted(word_count, key=word_count.get, reverse=True)[:5]

    print('Top 5 most used words:')
    for tw in top_words:
        print(f'{tw}: {word_count[tw]}')

    print(f'Word count: {len(words)}')
    print(f'Vocabulary size: {len(vocab)}')
    print(f'Sentence count: {len(sentences)}')


if __name__ == '__main__':
    sentences, words = tokenize_corpus('corpus.txt')
    vocab = set(words)
