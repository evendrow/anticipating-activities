To train on data downloaded from the authors:

```
python main.py --model=rnn --action=train --vid_list_file=./data/train.split1.bundle
```

To train on homage data, after running data processing scripts in `homage_scripts/`, run
```
python main.py \
    --model=rnn \
    --action=train \
    --vid_list_file=./data_homage/train.split1.bundle \
    --mapping_file=./data_homage/mapping_bf.txt \
    --model_save_path=./save_dir/models/homage_rnn \
    --results_save_path=./save_dir/results/homage_rnn
```
