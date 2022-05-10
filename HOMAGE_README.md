# Training and testing with HOMAGE

## First, a quick guide fo the old data

To train on data downloaded from the authors (Breakfast/50salads):

```
python main.py --model=rnn --action=train --vid_list_file=./data/train.split1.bundle
```
Next, predict and  evaluate with
```
python main.py --model=rnn --action=predict --vid_list_file=./data/test.split1.bundle

python eval.py \
    --obs_perc=.3 \
    --recog_dir=./save_dir/results/rnn/obs0.3-pred0.5 \
    --mapping_file=./data/mapping_bf.txt \
    --ground_truth_path=./data/groundTruth
```
This gives me `MoC  0.1964`, for reference.

## Now, onto HOMAGE:

To train on homage data, after running data processing scripts in `homage_scripts/`, run
```
python main.py \
    --model=rnn \
    --action=train \
    --vid_list_file=./data_homage/train.split1.bundle \
    --mapping_file=./data_homage/mapping_bf.txt \
    --model_save_path=./save_dir/models/homage_rnn \
    --results_save_path=./save_dir/results/homage_rnn \
    --input_type=gt \
    --max_seq_sz=150
```
Predict with
```
python main.py \
    --model=rnn \
    --action=predict \
    --vid_list_file=./data_homage/test.split1.bundle \
    --mapping_file=./data_homage/mapping_bf.txt \
    --model_save_path=./save_dir/models/homage_rnn \
    --results_save_path=./save_dir/results/homage_rnn \
    --input_type=gt \
    --max_seq_sz=150
```
Evaluate with
```
python eval.py \
    --obs_perc=.3 \
    --recog_dir=./save_dir/results/homage_rnn/obs0.3-pred0.5 \
    --mapping_file=./data_homage/mapping_bf.txt \
    --ground_truth_path=./data_homage/groundTruth
```
Gives `MoC  0.1536`.
