import os
import cv2
from tqdm import tqdm

# this script is for the bad data folder

base = r"../data/extracted_frames/extracted_frames"

for dirs in tqdm(os.listdir(base)):
    dirs = os.path.join(base, dirs)
    video_frames = {}
    path_to_file = False
    for dir, subdirs, files in os.walk(dirs):
        for file in files:
            if not file.endswith('jpg') and not file.endswith('.png'):
                continue
            path_to_file = os.path.join(dir, file)
            index = int(file[:-4])
            video_frames[index] = path_to_file
    frame_size = cv2.imread(path_to_file).shape
    vid_path = os.path.join(dirs, 'out.mp4')
    out = cv2.VideoWriter(vid_path, cv2.VideoWriter_fourcc(*'mp4v'), 20.0, (frame_size[1], frame_size[0]))

    for index in sorted(video_frames.keys()): 
        fp = video_frames[index]
        frame = cv2.imread(fp)
        out.write(frame)

    out.release()
