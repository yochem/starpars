#!/usr/bin/env python3

import nltk
import starpars as sp

def header(title):
    """Construct a nice looking header."""
    star_count = int((20 - len(title) - 2)/2)
    head = '\n' + '*'*20 + '\n'\
        + '*'*star_count \
        + ' ' + title.upper() + ' ' \
        + '*'*star_count + '\n'\
        + '*'*20
    return head


def analyze():
    """
    Print information about the corpus. The information contains:
    - 5 most used words;
    - Total word count;
    - Word count without duplicates (size vocab);
    - Sentence count;
    - average word length;
    """
    print(header('general'))
    # ignored characters
    print(f'- Ignored punction: {sp.IGNR_CHARS}')

    print(header('words'))
    # total word count
    print(f'- The corpus contains {len(words)} words')

    # vocab size
    print(f'- The vocabulary size is {len(set(words))}')

    # average word length
    average_word_length = sum(len(word) for word in words) / len(words)
    print(f'- Average word length: {average_word_length:.1f} characters')


    # get word frequency
    word_freq = nltk.FreqDist(tags).most_common()

    # search for most used words and print them with count
    most_word = [(wt[0], c) for (wt,c) in word_freq]
    print('- Most used words in the corpus:')
    for n, (word, count) in enumerate(most_word[:5], 1):
        print(f'    {n}. {word:5}: {count:3.0f}')

    # search for most used verbs and print them with count
    most_verb = [(wt[0], c) for (wt,c) in word_freq if 'V' in wt[1]]
    print('- Most used verbs in the corpus:')
    for n, (word, count) in enumerate(most_verb[:5], 1):
        print(f'    {n}. {word:5}: {count:2.0f}')

    # search for most used nouns and print them with count
    most_noun = [(wt[0], c) for (wt,c) in word_freq if wt[1][0] == 'N']
    print('- Most used nouns in the corpus:')
    for n, (word, count) in enumerate(most_noun[:5], 1):
        print(f'    {n}. {word:9}: {count:2.0f}')

    least_words = [wt[0] for (wt, c) in word_freq if c == 1]

    # number of lonely words
    print(f'- The corpus has {len(least_words)} hapaxes')

    # all part of speech tags used
    tag_dict = {}
    for _, tag in tags:
        if tag not in tag_dict:
            tag_dict[tag] = 1
        else:
            tag_dict[tag] += 1

    print('- All part of speech tags and their count:')
    for tag, count in tag_dict.items():
        print(f'    - {tag:5}: {count:3.0f}')

    print(header('sentences'))
    # sentence count
    print(f'- The corpus contains {len(sentences)} sentences')

    # average sentences length
    sum_words = 0
    for sentence in sentences:
        wc = len([x for x in nltk.word_tokenize(sentence) if x not in sp.IGNR_CHARS])
        sum_words += wc

    average_sent_length = sum_words / len(sentences)
    print(f'- Average sentences length: {average_sent_length:.1f} words')


if __name__ == '__main__':
    sentences, words, tags = sp.tokenize_corpus('data/corpus.txt')
    analyze()
