import argparse
import csv
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', "--homage-dir", type=str, help="the root directory of HOMAGE")
    parser.add_argument('-o', "--output-dir", default='./output', type=str, help="the output directory for generated files")
    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)

    actions = []
    with open(os.path.join(args.homage_dir, 'classInds', 'classInd_atomic.txt')) as f:
        #csvreader = csv.reader(f)
        for line in f:
            row = line.strip().split(' ')
            if len(row) <= 1:
                print('empty row')
                continue
            actions.append(f"{row[0]} {row[1]}\n")

    if len(actions) != 448:
        print("ERROR! Should be 448 actions, but loaded", len(actions))
        return

    print("Loaded", len(actions), "actions.")
    
    header = ['id','action','verb','noun']
    with open(os.path.join(args.output_dir, 'mapping_bf.txt'), 'w', encoding='UTF8') as f:
        f.writelines(actions)

    print("done!")

if __name__ == '__main__':
    main()

