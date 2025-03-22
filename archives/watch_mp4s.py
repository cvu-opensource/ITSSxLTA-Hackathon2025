"""
Helpful script to video play a video and note down what frame has what.
"""

import pygame
import cv2
import copy
import os
from pathlib import Path

def play_video(fp):
    video = cv2.VideoCapture(fp)
    success, video_image = video.read()
    fps = video.get(cv2.CAP_PROP_FPS)

    window = pygame.display.set_mode(video_image.shape[1::-1])
    clock = pygame.time.Clock()

    run = success # control exit loop condition
    current_frame_idx = -1  # current index to the list of frames that is being shown.
    paused = False  # pause!
    go_back = False
    go_forward = False
    frames = {}
    while run:
        clock.tick(fps)
        go_back = False
        go_forward = False

        for event in pygame.event.get():  # yoink the keyboard event
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = True if not paused else False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            run = False
        elif paused:  # only allow forward and back when paused
            if keys[pygame.K_LEFT]:
                go_back = True
            elif keys[ pygame.K_RIGHT]:
                go_forward = True

            
        
        # only if not paused, then increment the current frame index (at the end)
        if not paused:  # try to read the next frame, either from cv2 capture or frame list.
            current_frame_idx += 1  # auto increment current frame
        else:  # currently in paused state.
            maybe_next_frame_idx = current_frame_idx
            if go_back:
                maybe_next_frame_idx -= 1
            elif go_forward:
                maybe_next_frame_idx += 1
            else:
                pass  # dont alter current frame index

            if maybe_next_frame_idx not in frames and maybe_next_frame_idx < 0:
                print("Cannot move further backwards.")
            else:
                current_frame_idx = maybe_next_frame_idx

        try: # try to read the current frame, now that logic is all sorted out
            video_image = frames[current_frame_idx]
            success = True
        except KeyError:
            success, video_image = video.read()
            frames[current_frame_idx] = video_image  # cache it

        if success:  # add text and prepare to show it
            cv2.putText(
                video_image,
                "image " + str(current_frame_idx),
                (30,30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                thickness=4
            )  # does alter the base image but who cares
            
            # whatever video_image is, show it
            video_surf = pygame.image.frombuffer(
            video_image.tobytes(), video_image.shape[1::-1], "BGR")
                    
            window.blit(video_surf, (0, 0))
            pygame.display.flip()
        else:
            run = False
            print('no more frames left to show for video', fp)

    pygame.quit()

root_directories = [
    r'../data/extracted_frames/extracted_frames'
]  # for multiple root directories

# for dir in root_directories:
#     for d, subdirs, files in os.walk(dir):
#         for file in files:
#             fp = os.path.join(d, file)
#             if fp.endswith("mp4"):
#                 print("PLAYING VIDEO", fp)
#                 print("\n")
#                 play_video(fp)

for dir in root_directories:
    for fp in sorted(Path(dir).rglob('*.mp4'), reverse=True):
        print("PLAYING VIDEO", fp)
        play_video(fp)
