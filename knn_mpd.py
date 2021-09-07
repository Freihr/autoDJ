import argparse
import json
import os
import sys
from scipy.spatial.distance import hamming
from collections import Counter
import numpy as np
import math as mt
import random
import itertools
import time



class NearestNeighborRecommender:
    def __init__(self, k=2000, distance='hamming'):
        super().__init__()

        if distance == 'hamming':
            self.distance = hamming
        else :
            self.distance = distance
        
        self.k = k

    def train(self, playlists):
        """
        Create features for training set and save counts of songs (for IDF)
        """
        self.n_playlist = len(playlists)
        self.idf = self.get_idf(playlists)

        self.songs = list(set([i for i in itertools.chain.from_iterable([p.split() for p in playlists])]))
        

        N = len(self.songs)
        print('Unique songs in training set', N)
        print('Playlists in training set', len(playlists))
        
        #Create "bag of word" features for training set (vector of size N=nb songs in training set, 1 if song i appear in playlist)
        self.train_features = self.bag_of_word_features(playlists)

        print(self.train_features.shape)
        
            
    
    def predict(self, playlists):
        """
        returns a score for each song in the training playlist and each playlist in test set
        It should reflect whether a song whether could be a good continuation for a given playlist
        We give more importance to less frequent items by weighting with IDF
        """
        test_features = self.bag_of_word_features(playlists)

        total_scores = []

        for test_playlist in test_features:
            
            #test_songs = [i for i, x in enumerate(test_playlist) if x == 1]
            #print('Songs in test playlist', test_songs)

            similarities = [ 1-self.distance(train_playlist, test_playlist) for train_playlist in self.train_features] 
            """
            for train_playlist in self.train_features:
                train_songs = [i for i, x in enumerate(train_playlist) if x == 1]
                
                if len(set(test_songs)&set(train_songs))>0: #only consider playlist with atleast one common track as possible neighbors
                    similarities.append(0)
                else:
                    similarities.append(1-hamming(train_playlist, test_playlist))
            """
            topSimilarities = sorted(similarities, reverse=True)[:self.k]
            neighborsIndex = [similarities.index(s) for s in topSimilarities] #index of neighbors in self.train_features
            
            neighbors = np.take(self.train_features, neighborsIndex, axis=0)

            scores = {song:0 for song in self.songs}
            
            for playlist in neighbors:
                for j in range(len(playlist)):
                    if playlist[j]==1:
                        scores[self.songs[j]] += (1-self.distance(playlist, test_playlist))*playlist[j]*self.idf[self.songs[j]]

            """
            for j in range(len(self.songs)):
                for playlist in neighbors:
                    try:
                        scores[self.songs[j]] += (1-self.distance(playlist, test_playlist))*playlist[j]*self.idf[self.songs[j]]
                    except KeyError:
                        scores[self.songs[j]] = (1-self.distance(playlist, test_playlist))*playlist[j]*self.idf[self.songs[j]]
            """

            total_scores.append(scores)
        
        return total_scores


    def bag_of_word_features(self, playlists): #shape : [nb_playlist, nb_song]
        features = []
        for playlist in playlists:
            
            playlist_feat = [0]*len(self.songs)
            songs_playlist = playlist.split()

            #We do not consider songs not appearing in the test set to compute our features
            playlist_feat = [ 1 if self.songs[i] in songs_playlist else 0 for i in range(len(self.songs))]
            """
            for j in range(len(playlist.split())):
                try:
                    playlist_feat[self.songs.index(playlist.split()[j])] = 1
                except KeyError: #We do not consider songs not appearing in the test set to compute our features
                    pass
            """

            features.append(playlist_feat)

        return np.array(features)

    def get_idf(self, playlists):
        #small trick : use set to count songs only once per playlist
        counts = sum([ Counter(set(playlist.split())) for playlist in playlists], Counter())
        return { k:mt.log(self.n_playlist/d) for k,d in counts.items()}
        

def main():
    parser = argparse.ArgumentParser(description='Train NearestNeighbor from Million Playlist Dataset.')
    parser.add_argument('--k', type=int, default=2000)
    parser.add_argument('--distance', type=str, default="hamming")
    parser.add_argument('--train_file', type=str, default='./train')
    parser.add_argument('--test_file', type=str, default='./test')
    parser.add_argument('--output_file', type=str, default='./output')

    args = parser.parse_args()
   


    with open(args.train_file, 'r') as f:
        train_playlists = [line for line in f.readlines()]

    
    with open(args.test_file, 'r') as f:
        test_playlists = [line for line in f.readlines()]
    

    recommender = NearestNeighborRecommender(args.k, args.distance)

    print('Training')
    start = time.time()
    recommender.train(train_playlists)
    end = time.time()
    print('Training took', end - start)

    print('Predicting')
    start = time.time()
    results = recommender.predict(test_playlists)
    end = time.time()
    print('Predicting took', end - start)

    print('Saving results in {}'.format(args.output_file))
    with open(args.output_file, 'w') as f:
        json.dump(results , f)

if __name__ == "__main__":
    main()


