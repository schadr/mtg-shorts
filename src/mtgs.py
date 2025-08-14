#!/bin/python3

import json
import os
import shutil
import tempfile
import cv2
import argparse

from src.caption_generation import load_captions_from_file, smooth_captions
from src.pricing import Card, convert_to_cards, create_totals
from src.video import add_card_info_to_video, add_coin_sound_effects, add_music, extract_card_info_from_video, load_video

def process_video(file_path, collector=False, use_config=False, cost=0, rotate=False):
    video = load_video(file_path)
    smooth_captions = []
    text_in_frame = {}
    filename = os.path.basename(file_path)
    path = os.path.dirname(file_path)
    if not use_config:
        cards_in_frame = extract_card_info_from_video(video)
        smoothed_captions = smooth_captions(cards_in_frame)
    else:
        smoothed_captions, text_in_frame = load_captions_from_file(os.path.join(path,f"cards-{filename.replace('.','-')}.json"))
    cards = convert_to_cards(smoothed_captions)
    totals = create_totals(cards, cost)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4", mode="w") as temp_file:
        temp_file_path = temp_file.name
        out_file = os.path.join(path,f"edited-{filename}")
        add_card_info_to_video(video, text_in_frame, cards, totals, cost, temp_file_path, rotate, video.get(cv2.CAP_PROP_FPS), collector)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4", mode="w") as temp_file_music:
            temp_file_music_path = temp_file_music.name
            add_coin_sound_effects(temp_file_path, cards, video.get(cv2.CAP_PROP_FPS), file_path, temp_file_music_path)
            add_music(temp_file_music_path, out_file)

def create_fps_video(file_path, collector=False, use_config=False, cost=0, rotate=False):
    video = load_video(file_path)
    num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    cards_in_frame = [Card("uuid", f"Frame: {i} / {num_frames}", i, "set", i, i) for i in range(num_frames)]
    filename = os.path.basename(file_path)
    path = os.path.dirname(file_path)
    add_card_info_to_video(video, {}, cards_in_frame, [i for i in range(num_frames)], cost, os.path.join(path,f"frame-{filename}"), rotate, 1)
    source = "templates/template-play-booster.json"
    if collector:
        source = "templates/template-collector-booster.json" 
    shutil.copyfile(source, f"{path}/cards-{filename.replace('.','-')}.json")
    # Update "total_frames" in the JSON file
    json_path = f"{path}/cards-{filename.replace('.','-')}.json"
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["total_frames"] = num_frames
        data["text"][-1]["first_frame"] = num_frames - 110
        data["text"][-1]["last_frame"] = num_frames
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description="MTG Shorts CLI")
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--file', type=str, help='Path to the video file that needs to be edited')
    group.add_argument('--folder', type=str, help='Folder containing video files to be processed')
    parser.add_argument('--fps', action="store_true", default=False, help='Outputs videos with with framenumber captions at 1 fps')
    parser.add_argument('--collector', action="store_true", default=False, help='Video(s) are of collector packs')
    parser.add_argument('--use-config', action="store_true", default=False, help='Use config file for video processing')
    parser.add_argument('--cost', type=float, default=6.0, help='Cost of the booster pack')
    parser.add_argument('--rotate', action="store_true", default=False, help="Rotate output video")
    args = parser.parse_args()

    processor = None
    if args.fps:
        processor = create_fps_video
    else:
        processor = process_video

    if args.file:
        processor(args.file, args.collector, args.use_config, args.cost, args.rotate)
        
    if args.folder:
        for item in os.listdir(args.folder):
            file_name = os.path.join(args.folder, item)
            if file_name.endswith(".json"):
                continue
            if os.path.basename(file_name).startswith("frame-"):
                continue
            if os.path.isfile(file_name):
                processor(os.path.join(args.folder, file_name), args.collector, args.use_config, args.cost, args.rotate)

if __name__ == "__main__":
    main()