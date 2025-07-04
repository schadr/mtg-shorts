#!/bin/python3

import json
import os
import shutil
import cv2
import argparse

from src.caption_generation import load_captions_from_file, smooth_captions
from src.pricing import Card, convert_to_cards
from src.video import add_card_info_to_video, extract_card_info_from_video, load_video

def process_video(file_path, collector=False, use_config=False):
    video = load_video(file_path)
    smooth_captions = []
    if not use_config:
        cards_in_frame = extract_card_info_from_video(video)
        smoothed_captions = smooth_captions(cards_in_frame)
    else:
        filename = os.path.basename(file_path)
        path = os.path.dirname(file_path)
        data = None
        smoothed_captions = load_captions_from_file(f"{path}/cards-{filename.replace(".","-")}.json")
    add_card_info_to_video(video, convert_to_cards(smoothed_captions))

def create_fps_video(file_path, collector=False, use_config=False):
    video = load_video(file_path)
    num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    cards_in_frame = [Card("uuid", f"Frame: {i}", i, "set", i, i) for i in range(num_frames)]
    filename = os.path.basename(file_path)
    path = os.path.dirname(file_path)
    add_card_info_to_video(video, cards_in_frame, f"{path}/frame-{filename}", 1)
    source = "templates/template-play-booster.json"
    if collector:
        source = "templates/template-collector-booster.json" 
    shutil.copyfile(source, f"{path}/cards-{filename.replace(".","-")}.json")


def main():
    parser = argparse.ArgumentParser(description="MTG Shorts CLI")
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--file', type=str, help='Path to the video file that needs to be edited')
    group.add_argument('--folder', type=str, help='Folder containing video files to be processed')
    group.add_argument('--fps', type=bool, default=False, help='Outputs videos with with framenumber captions at 1 fps')
    group.add_argument('--collector', type=bool, default=False, help='Video(s) are of collector packs')
    group.add_argument('--use-config', type=bool, default=False, help='Use config file for video processing')
    args = parser.parse_args()

    processor = None
    if args.fps:
        processor = create_fps_video
    else:
        processor = process_video

    if args.file:
        processor(args.file, args.collector, args.use_config)
        
    if args.folder:
        for item in os.listdir(args.folder):
            file_name = os.path.join(args.folder, item)
            if os.path.isfile(file_name):
                processor(os.path.join(args.folder, file_name), args.collector, args.use_config)

if __name__ == "__main__":
    main()