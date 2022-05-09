import argparse
import csv
import os
from pathlib import Path
import tqdm

def load_mappings_file(fpath: Path) -> list:
    """
    Read the mappings file shared by Abu farha (CVPR'18) to read the class
    names.
    """
    res = []
    with open(fpath, 'r') as fin:
        for line in fin:
            if line:
                res.append(line.rpartition(' ')[-1].strip())
    # convert to dict
    return dict(zip(res, range(len(res))))

def read_homage_annotations(annots_path: Path, root: Path, action_classes: dict, view='mixed', fps=30):
    all_segments = []
    with open(annots_path) as fin:
        for line in fin:
            if not line:
                continue
            data = line.split(',')
            assert len(data) % 4 == 0

            for i in range(len(data) // 4):
                base_idx = i * 4
                video_name = data[base_idx].split('/')[-1]
                scene_name = video_name.split('_')[0]
                view_name = video_name.split('_')[2]
                path_name = f'{scene_name}/{video_name}'
                # load depending on view type
                if view_name == 'v000' and view == 'tpv':
                    continue
                elif view_name != 'v000' and view == 'ego':
                    continue
                
                start, end, action = data[base_idx+1 : base_idx+4]
                label = action_classes[action.strip()]
                p, r, v, a = video_name.split('_')
                # FIXME: temporary; fix path
                #video_path = os.path.join(root, p, video_name)
                all_segments.append({
                    'path_name': path_name,
                    'scene_name': scene_name,
                    'video_name': video_name,
                    'start': int(start),
                    'end': int(end),
                    'label': label,
                    'label_name': action.strip()
                })
    return all_segments

def convert_data(root_dir, output_dir):
    classes_fpath = os.path.join(root_dir, 'classInds', 'classInd_atomic.txt')
    action_classes = load_mappings_file(classes_fpath)
    
    gt_dir = os.path.join(output_dir, 'groundTruth')
    if not os.path.exists(gt_dir):
        os.mkdir(gt_dir)

    for mode in ['train', 'test']:
        annot_path = os.path.join(root_dir, 'annotations', 'atomic', f"{mode}_split_atomic.csv")
        action_segments = read_homage_annotations(annot_path, None, action_classes, 'ego')
        print("Loaded", len(action_segments), "action segments for", mode, "set.")

        lines = ['#bundle\n']

        segs_by_video  = dict()
        for segment in action_segments:
            path = segment['path_name']
            if path  not in segs_by_video:
                segs_by_video[path] = []
            segs_by_video[path].append(segment)

        for path, segments in tqdm.tqdm(segs_by_video.items()):
            frame_path = os.path.join(root_dir, 'frames', path)
            num_frames = sum([1 if a.endswith('jpg') else 0 for a in os.listdir(frame_path)])
            #num_frames = len(glob.glob(os.path.join(root_dir, 'frames', path, '*.jpg')))
            #print('num frames is', num_frames, 'for', path)

            video_name = segments[0]['video_name']
            out_file = os.path.join(gt_dir, f"{video_name}.txt")

            actions = []
            for i in range(1, num_frames+1):
                action = 'none'
                best_center_dist = 0
                for segment in segments:
                    if segment['start'] <= i and i <= segment['end']:
                        seg_center = (segment['start'] + segment['end'])/2
                        center_dist = abs(i-seg_center)
                        if action == 'none' or center_dist < best_center_dist:
                            best_center_dist = center_dist
                            action = segment['label_name']
                
                actions.append(action + "\n")

            with open(out_file, 'w', encoding='UTF8') as f:
                f.writelines(actions)

            lines.append(out_file + "\n")

        bundle_path = os.path.join(output_dir, f'{mode}.split1.bundle')
        with open(bundle_path, 'w', encoding='UTF8') as f:
            f.writelines(lines)
            
        
        #with open(os.path.join(args.output_dir, f'{outname}.csv'), 'w', encoding='UTF8') as f:
        #    writer = csv.writer(f)
        #    for i, segment in enumerate(action_segments):
        #        row = list(segment)
        #        writer.writerow(row)

        print("done!")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', "--homage-dir", type=str, help="the root directory of HOMAGE")
    parser.add_argument('-o', "--output-dir", default='./output', type=str, help="the output directory for generated files")
    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)

    convert_data(args.homage_dir, args.output_dir)

if __name__ == '__main__':
    main()

