# autoDJ
Code for MALIS Project on Next-Track Music Recommendation

## Usage

### Prepare data from Million Playlist Dataset

` python prepare_data.py --path path --target_file target --train_file train --test_file test `

### Generate Session-Nearest Neighbor recommendations 

` python knn_mpd.py --output_file output --train_file train --test_file test `

### Generate N-Gram model

` python ngram_mpd.py --n n --train_file train `

### Evaluate recommendations

` python evaluate.py --pred_file output --target_file target `



