
"""
This script parses traktor log files and output two files, one for training and one for testing, containing "sentences" of songs ID describing the playlist.

"""

from bs4 import BeautifulSoup as bs
import logging
import os
import itertools
import json
import random

DIR_PATH="/Users/raphaeltoumi/Documents/Native Instruments/Traktor 3.3.0/History/"
content = []

def parse_tracks(path):
    """
    Parse a history file.
    Return list [(title,artist)] of tracks in history file.
    """
    tracks = []
    with open(path, "r") as file:
        content = file.readlines()
        content = "".join(content)
        bs_content = bs(content, "lxml")
    for entry in bs_content.find_all("entry"):
        if entry.parent.name == "collection":
            try:
                tracks.append((entry["title"], entry["artist"]))
            except KeyError:
                try:
                    tracks.append((entry["title"],"NONE"))
                except KeyError:
                    try:
                        tracks.append(("NONE",entry["artist"]))
                    except KeyError:
                        tracks.append(("NONE", "NONE"))

    logging.info(f'{path} : {len(tracks)} tracks')

    return tracks



def main():
    sets = []
    for path in os.listdir(DIR_PATH):
        sets.append(parse_tracks(os.path.join(DIR_PATH,path)))

    print("Number of sets:", len(sets))

    songs = list(set([i for i in itertools.chain.from_iterable(sets)]))

    print("Number of unique tracks", len(songs))

    print("Total number of tracks", sum([len(tracklist) for tracklist in sets]))

    #Encode songs with index from songs
    tracklists = [ " ".join([str(songs.index(track)) for track in tracklist]) for tracklist in sets]
    
    with open('traktor_tracklist', 'w') as f:
        f.write("\n".join(tracklists))

    with open('songList', 'w') as f:
        json.dump(songs, f)
    
    #Split sentences into training and test set 80/20 at random
    
    random.shuffle(tracklists)

    train_tracklists = tracklists[:int(len(tracklists)*0.8)]
    test_tracklists = tracklists[int(len(tracklists)*0.8):]

    #Remove tracklists that contain songs not appearing in training set
    train_songs = set([i for i in itertools.chain.from_iterable([p.split() for p in train_tracklists])])
    print('Number of songs in training', len(list(train_songs)))
    
    print('Number of testing playlist before removing', len(test_tracklists))

    test_tracklists = [ playlist for playlist in test_tracklists if any(x in train_songs for x in playlist.split()) and playlist.split()[-1] in train_songs ]

    print('Number of testing playlists', len(test_tracklists))

    #Remove last song of each test playlist to be used as target
    test_targets = []

    for i in range(len(test_tracklists)):
        temp = test_tracklists[i].split()
        test_targets.append(temp.pop())
        
        test_tracklists[i] = " ".join(temp)
    
    with open('traktor_train', 'w') as f:
        f.write("\n".join(train_tracklists))

    with open('traktor_test', 'w') as f:
        f.write("\n".join(test_tracklists))
    
    with open('traktor_target', 'w') as f:
        f.write("\n".join(test_targets))

    with open('songList', 'w') as f:
        json.dump(songs, f)

    
    




"""
artist_counts = {}
for track in total_tracks:
    try:
        artist_counts[track[1]] += 1
    except KeyError:
        artist_counts[track[1]] = 1

tracks_counts = {}
for track in total_tracks:
    try:
        tracks_counts[track] += 1
    except KeyError:
        tracks_counts[track] = 1

def transition_counts(sets, k):
    #sets: list of tracklists, k: nb of tracks
    counts = {}
    for tracklist in sets:
        for i in range(len(tracklist)-k):
            try:
                counts[tuple(tracklist[i:i+k])] += 1
            except KeyError:
                counts[tuple(tracklist[i:i+k])] = 1
    return counts

def find_k_best(counts, k):
    top_k = [("",0)]*k

    for name,count in counts.items():
        if top_k[0][1] < count:
            top_k[0] = (name,count)
            top_k.sort(key=lambda x:x[1])
    return top_k

print("Number of artists:", len(artist_counts))
print("Number of tracks:", len(tracks_counts))

top_k_artist = find_k_best(artist_counts, 10)
top_k_tracks = find_k_best(tracks_counts, 10)

print(top_k_artist)
print(top_k_tracks)

trans2 = transition_counts(sets,2)
trans3 = transition_counts(sets),3)
trans4 = transition_counts(sets,4)
trans5 = transition_counts(sets,5)

for t in find_k_best(trans2, 10):
    print(t)
for t in find_k_best(trans3, 10):
    print(t)
for t in find_k_best(trans4, 10):
    print(t)
for t in find_k_best(trans5, 10):
    print(t)
"""

if __name__ == "__main__":
    main()

