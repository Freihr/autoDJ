"""
This script parses json file from Million Playlist Dataset.
Output two files, one for training and one for testing, containing "sentences" of songs ID describing the playlist.
Splitting is done 80/20 at random, but playlists containing unseen songs in training are excluded from the test set.
"""
import argparse
import os
import json
import random
import itertools

def get_playlists(data):
    #only keep playlist with atleast 3 songs
    return [ " ".join([track["track_uri"].split("spotify:track:")[1] for track in playlist["tracks"]]) for playlist in data["playlists"] if len(playlist["tracks"])>3]

def main():
    parser = argparse.ArgumentParser(description='Parse JSON files from MPD')
    parser.add_argument('--path',type=str)
    parser.add_argument('--all', default=False, action='store_true')
    parser.add_argument('--train_file', type=str, default='./train')
    parser.add_argument('--test_file', type=str, default='./test')
    parser.add_argument('--target_file', type=str, default='./target')

    args = parser.parse_args()

    if args.all: #merge all json files in path
        playlists = []
        for filename in os.listdir(args.path):
            f = os.path.join(args.path, filename)
            if os.path.isfile(f):
                with open(f, 'r') as file:
                    data = json.load(file)
                playlists += get_playlists(data)
    
    else:
        with open(args.path,'r') as f:
            data = json.load(f)
            playlists = get_playlists(data)

    #Split sentences into training and test set 80/20 at random
    
    random.shuffle(playlists)

    train_playlists = playlists[:int(len(playlists)*0.8)]
    test_playlists = playlists[int(len(playlists)*0.8):]


    #Remove playlists whose last songs does not appear in the training set (as it is used to be evaluated)
    #Also remove playlists who contains no song from the training set

    train_songs = set([i for i in itertools.chain.from_iterable([p.split() for p in train_playlists])])
    print('Number of songs in training', len(list(train_songs)))

    print('Number of testing playlist before removing', len(test_playlists))
    test_playlists = [ playlist for playlist in test_playlists if any(x in train_songs for x in playlist.split()) and playlist.split()[-1] in train_songs ]
    
            
    print('Number of testing playlists', len(test_playlists))

    #Remove last song of each test playlist to be used as target
    test_targets = []

    for i in range(len(test_playlists)):
        temp = test_playlists[i].split()
        test_targets.append(temp.pop())
        
        test_playlists[i] = " ".join(temp)
    


    with open(args.train_file, 'w') as f:
        f.write("\n".join(train_playlists))
    
    with open(args.test_file, 'w') as f:
        f.write("\n".join(test_playlists))

    with open(args.target_file, 'w') as f:
        f.write("\n".join(test_targets))


if __name__ == "__main__":
    main()