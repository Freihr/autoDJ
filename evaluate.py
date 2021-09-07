import argparse
import json
import matplotlib.pyplot as plt

def rankTrueTarget(predictions, targets):
    """
    Predictions contains a list of songs id in decreasing order of probability
    Returns the rank of the correct target in the predictions
    """
    
    return [ predictions[i].index(targets[i])+1 for i in range(len(predictions)) ]


def recallTopN(predictions, targets, N):
    """
    Predictions is [nb_test_playlist, nb_train_tracks] or [nb_test_playlist,N] with only the best rank predictions
    returns proportion of correct playlist continuations that are in the top N predicted values
    """
    return sum([1 if targets[i] in predictions[i][:N] else 0 for i in range(len(predictions))])/len(predictions)

def main():
    parser = argparse.ArgumentParser(description='Evaluate our models')
    parser.add_argument('--pred_file', type=str, default='./predictions')
    parser.add_argument('--target_file', type=str, default='./target')

    args = parser.parse_args()

    with open(args.pred_file, 'r') as f:
        preds = json.load(f)
    
    scores = [[]]*len(preds)

    for i in range(len(preds)):

        scores[i] = sorted(preds[i].items(), key=lambda x: x[1], reverse=True)

    predictions = [[score[0] for score in playlist] for playlist in scores]
        
        
    targets = []
    with open(args.target_file, 'r') as f:
        for line in f.readlines():
            targets.append(line.rstrip("\n"))

    ranks = rankTrueTarget(predictions, targets)

    print("Recall top 1", recallTopN(predictions, targets, 1))
    print("Recall top 5", recallTopN(predictions, targets, 5))
    print("Recall top 10", recallTopN(predictions, targets, 10))
    print("Recall top 20", recallTopN(predictions, targets, 20))
    print("Recall top 50", recallTopN(predictions, targets, 50))
    with open('ranks', 'w') as f:
        json.dump(ranks, f)
    

if __name__ == "__main__":
    main()
