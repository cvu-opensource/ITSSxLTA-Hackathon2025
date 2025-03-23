# We do a video classification
# so uhhh make csv or smth
import os
import pandas as pd
import cv2
from PIL import Image
import numpy as np
import random
import PIL

with open('/mnt/e/ITSSxLTA-Hackathon2025/labels.txt', 'r') as f:
    thing = f.read()
    ouchies = eval(thing)

# all the directories with all the mp4 files. recursion is used 
dirs = [fr"/mnt/e/data/cadp/extracted_frames-002/extracted_frames"]

data = {
        'image': [],  # list of fps
        'label': [], # list of 1s and 0s whether or not it is a video with an accident
        'video': [],
    }

sample_every = 5  # lots of frames that look very similar, wasting our resources
# training / evaling on them again. so sample every n frames.
tracker_dict = {}  # horrible naming!

for dir in dirs:

    for d, subds, files in os.walk(dir):
        for filename in files:
            fp = os.path.join(d, filename)
            if fp.endswith('jpg') or fp.endswith('png'):

                # try:
                #     im = Image.open(fp)
                # except PIL.UnidentifiedImageError as e:
                #     print(f'PIL couldnt find the filepath at {fp}, lets purge it for cleanliness sake')
                #     os.remove(fp)
                #     continue

                frame = int(filename[:-4])
                video_idx = int(d.split('/')[-1])

                if video_idx not in tracker_dict:  # create new list
                    tracker_dict[video_idx] = [frame] 

                if video_idx in ouchies:
                    accident_frame = ouchies[video_idx]

                    if frame >= accident_frame:
                        label = 1
                    else:
                        label = 0

                if frame >= tracker_dict[video_idx][-1] + sample_every:
                    tracker_dict[video_idx].append(frame)

                    data['image'].append(fp)
                    data['label'].append(label)
                    data['video'].append(video_idx)
                    # print('fp', fp)
                    # print('label', label)
        
                # ouchies.pop(video_idx)

df = pd.DataFrame(data)


# split???????????????????????????????????
train_ratio = 0.60
val_ratio = 0.30
test_ratio = 0.10

# df = pd.read_csv('/mnt/e/data/dataset_nosplit.csv')
video_idxes = df['video'].unique()
video_idxes = np.array(video_idxes)
empty_ds_list = {}
np.random.shuffle(video_idxes)

train_num = int(train_ratio * len(video_idxes))
val_num = int(train_num + val_ratio * len(video_idxes))
test_num = int(len(video_idxes) - train_num - val_num)

train, val, test = video_idxes[:train_num], video_idxes[train_num:val_num], video_idxes[val_num:]
all = np.concatenate((train, val, test))

for string, video_idxes in zip(['train', 'val', 'test'], [train, val, test]):
    for video_idx in video_idxes:
        empty_ds_list[video_idx] = string

df['split'] = df['video'].map(empty_ds_list)

df_train = df[df['split'] == 'train']
df_val = df[df['split'] == 'val']
df_test = df[df['split'] == 'test']

print(df_train.value_counts())
print(df_val.value_counts())
print(df_test.value_counts())

df_train.to_csv('/mnt/e/data/dataset_train.csv', index=False)
df_val.to_csv('/mnt/e/data/dataset_val.csv', index=False)
df_test.to_csv('/mnt/e/data/dataset_test.csv', index=False)