import os
import shutil
import cv2

# this script is for the bad data folder

base = fr"/mnt/e/data/bad/data"

# incident_frames = [
#     '5_32.jpg',
#     'test_27.jpg',
#     'test1_16.jpg',
#     'test3_27.jpg',
#     'test4_29.jpg',
#     'test7_24.jpg',
#     'test11_18.jpg',
#     'test12_11.jpg',
#     'test13_10.jpg',
#     'test14_11.jpg',
#     'test15_4.jpg',
#     'test16_20.jpg',
#     'test17_15.jpg',
#     'test18_22.jpg',
#     'test19_22.jpg',
#     'test20_16.jpg',
#     'test22_11.jpg',
#     'test23_10.jpg',
#     'test24_24.jpg',
#     'test25_23.jpg',
#     'test26_13.jpg',
#     'test27_8.jpg',
#     'test28_15.jpg',
#     'test29_10.jpg',
#     'test30_8.jpg',
# ]


# for dir, subdirs, files in os.walk(base):
#     for file in files:
#         print(file)
#         if '_' not in file:
#             continue
#         folder, no = file.split('_')
#         newfolder = os.path.join(base, folder)
#         # print(newfolder)
#         if not os.path.exists(newfolder):
#             os.mkdir(newfolder)

#         old_path = os.path.join(dir, file)
#         new_path = os.path.join(newfolder, file)

#         if not os.path.exists(new_path):
#             shutil.copy(old_path, new_path)


# for i, dirs in enumerate(os.listdir(base)):

#     folder_path = os.path.join(base, dirs)
#     before_folder = os.path.join(folder_path, 'before')
#     after_folder = os.path.join(folder_path, 'after')
    
#     if not os.path.exists(before_folder):
#         os.mkdir(before_folder)
#     if not os.path.exists(after_folder):
#         os.mkdir(after_folder)

#     accident_index = False
#     dict = {}
#     for file in os.listdir(folder_path):

#         if not file.endswith('jpg') and not file.endswith('.png'):
#             continue

#         index = int(file.split('_')[1][:-4])

#         if file in incident_frames:
#             accident_index = index

#         dict[index] = file

#     print(dict)
#     print(accident_index)
#     if accident_index:
#         for index in dict:
#             file = dict[index]
#             src = os.path.join(folder_path, file)
#             if index >= accident_index:
#                 des = os.path.join(after_folder, file)
#             else:
#                 des = os.path.join(before_folder, file)

#     #     src = os.path.join(folder_path, file)
#     #     if has_accident_occurred and index >= accident_index and not accident_index:
#     #         des = os.path.join(after_folder, file)
#     #     else:
#     #         des = os.path.join(before_folder, file)

#     #     print(" ")
#             print('src', src)
#             print('des', des)
#             shutil.move(src, des)


for i, dirs in enumerate(os.listdir(base)):
    dirs = os.path.join(base, dirs)
        # frameSize = (160, 256)
    # env = minedojo.make(task_id='harvest_wool_with_shears_and_sheep', image_size=frameSize)
    # out = cv2.VideoWriter('outputs/ahhhh.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 20.0, (frameSize[1], frameSize[0]))
    video_frames = {}
    path_to_file = False
    for dir, subdirs, files in os.walk(dirs):
        for file in files:
            path_to_file = os.path.join(dir, file)
            if not file.endswith('jpg') and not file.endswith('.png'):
                continue

            index = int(file.split('_')[1][:-4])
            video_frames[index] = path_to_file

    frame_size = cv2.imread(path_to_file).shape
    vid_path = os.path.join(dirs, 'out.mp4')
    out = cv2.VideoWriter(vid_path, cv2.VideoWriter_fourcc(*'mp4v'), 5.0, (frame_size[1], frame_size[0]))

    for index in sorted(video_frames.keys()):
        fp = video_frames[index]
        frame = cv2.imread(fp)
        out.write(frame)

    out.release()
