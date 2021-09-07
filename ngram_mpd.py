"""
Handle Creation and evaluation of ngram model from json file of Million Playlist Dataset.
"""
import json
import os
import sys
import argparse
import subprocess
import random

from nltk.lm import MLE
from nltk.util import bigrams
from nltk.util import ngrams
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk import word_tokenize, sent_tokenize 

import nltk
nltk.download('punkt')

def get_playlists(data):
    return [ " ".join([track["track_uri"].split("spotify:track:")[1] for track in playlist["tracks"]]) for playlist in data["playlists"] if playlist["tracks"]!=[]]
    

def main():
    parser = argparse.ArgumentParser(description='Generate N-Gram model from Million Playlist Dataset.')
    parser.add_argument('--n', type=str, default="3")
    parser.add_argument('--train_file', type=str, default='./train')
    parser.add_argument('--test_file', type=str, default='./test')

    args = parser.parse_args()

    with open(args.train_file, 'r') as f:
        train_playlists = [line.split() for line in f.readlines()]

    with open(args.test_file, 'r') as f:
        test_playlists = [line.split() for line in f.readlines()]

    print(list(bigrams(train_playlists[0])))
    print(list(ngrams(train_playlists[0],n=3)))
    
    #corpus = [word_tokenize(playlist) for playlist in train_playlists]

    train, vocab = padded_everygram_pipeline(args.n, train_playlists)
    
    print("Number of songs", len(list(vocab)))

    lm = MLE(args.n)
    lm.fit(train, vocab)

    print("Number of songs", len(vocab))
    print(lm.counts['3clX2NMmjaAHmBjeTSa9vV'])
    print(lm.counts['3clX2NMmjaAHmBjeTSa9vV']['7GPq5i4Dn95yDaqxdoeKNW'])

    """
    #train N-Gram using SRILM
    result = subprocess.run(
        ["ngram-count", "-order", args.n, "-text", args.train_file, "-lm", args.lm]
    )

    #evaluate on test set
    result = subprocess.run(
    ["ngram", "-lm", args.lm , "-ppl", args.test_file]
    )
    """


    

if __name__ == "__main__":
    main()


