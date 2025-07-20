#!/bin/python3

import json
import os
import shutil
import tempfile
import cv2
import argparse

from src.caption_generation import load_captions_from_file, smooth_captions
from src.pricing import Card, convert_to_cards, create_totals
from src.video import add_card_info_to_video, add_coin_sound_effects, extract_card_info_from_video, load_video

def process_video(file_path, collector=False, use_config=False, cost=0):
    video = load_video(file_path)
    smooth_captions = []
    text_in_frame = {}
    filename = os.path.basename(file_path)
    path = os.path.dirname(file_path)
    if not use_config:
        cards_in_frame = extract_card_info_from_video(video)
        smoothed_captions = smooth_captions(cards_in_frame)
    else:
        data = None
        smoothed_captions, text_in_frame = load_captions_from_file(f"{path}/cards-{filename.replace(".","-")}.json")
    cards = convert_to_cards(smoothed_captions)
    totals = create_totals(cards, cost)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4", mode="w") as temp_file:
        temp_file_path = temp_file.name
        add_card_info_to_video(video, text_in_frame, cards, totals, cost, temp_file_path, video.get(cv2.CAP_PROP_FPS), collector)
        add_coin_sound_effects(temp_file_path, cards, video.get(cv2.CAP_PROP_FPS), file_path)

def create_fps_video(file_path, collector=False, use_config=False, cost=0):
    video = load_video(file_path)
    num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    cards_in_frame = [Card("uuid", f"Frame: {i}", i, "set", i, i) for i in range(num_frames)]
    filename = os.path.basename(file_path)
    path = os.path.dirname(file_path)
    add_card_info_to_video(video, {}, cards_in_frame, [i for i in range(num_frames)], cost, f"{path}/frame-{filename}", 1)
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
    group.add_argument('--cost', type=float, default=6.0, help='Cost of the booster pack')
    args = parser.parse_args()

    processor = None
    if args.fps:
        processor = create_fps_video
    else:
        processor = process_video

    if args.file:
        processor(args.file, args.collector, args.use_config, args.cost)
        
    if args.folder:
        for item in os.listdir(args.folder):
            file_name = os.path.join(args.folder, item)
            if os.path.isfile(file_name):
                processor(os.path.join(args.folder, file_name), args.collector, args.use_config, args.cost)

if __name__ == "__main__":
    main()