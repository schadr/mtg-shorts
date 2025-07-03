#!/bin/python3

import os
import shutil
import cv2
import argparse

from src.caption_generation import smooth_captions
from src.pricing import Card
from src.video import add_card_info_to_video, extract_card_info_from_video, load_video

def process_video(file_path):
    video = load_video(file_path)
    cards_in_frame = extract_card_info_from_video(video)
    smoothed_captions = smooth_captions(cards_in_frame)
    add_card_info_to_video(video, smoothed_captions)

def create_fps_video(file_path):
    video = load_video(file_path)
    num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    cards_in_frame = [Card("uuid", f"Frame: {i}", i, "set", i, i) for i in range(num_frames)]
    filename = os.path.basename(file_path)
    path = os.path.dirname(file_path)
    add_card_info_to_video(video, cards_in_frame, f"{path}/frame-{filename}", 1)
    shutil.copyfile("templates/template-play-booster.json", f"{path}/cards-{filename.replace(".","-")}.json")


def main():
    parser = argparse.ArgumentParser(description="MTG Shorts CLI")
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--file', type=str, help='Path to the video file that needs to be edited')
    group.add_argument('--folder', type=str, help='Folder containing video files to be processed')
    group.add_argument('--fps', type=bool, help='Outputs videos with with framenumber captions at 1 fps')
    args = parser.parse_args()

    processor = None
    if args.fps:
        processor = create_fps_video
    else:
        processor = process_video

    if args.file:
        processor(args.file)
        
    if args.folder:
        for item in os.listdir(args.folder):
            file_name = os.path.join(args.folder, item)
            if os.path.isfile(file_name):
                processor(os.path.join(args.folder, file_name))

if __name__ == "__main__":
    main()