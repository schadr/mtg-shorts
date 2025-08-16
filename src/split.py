import argparse
import os
import json
from moviepy import VideoFileClip

def split_video(video_file_path, config_file_path):
    with open(config_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    video = VideoFileClip(video_file_path)
    booster_count = 0
    for booster in config["boosters"]:
        start = booster["first_frame"]
        end = booster["last_frame"]
        # editing the video
        output_filename = f"{os.path.splitext(video_file_path)[0]}_booster_{booster_count}.mp4"
        subclip = video.subclipped(start / video.fps, (end + 1) / video.fps)
        subclip.write_videofile(output_filename)
        # editing the config
        for card in booster["cards"]:
            card["first_frame"] -= start
            card["last_frame"] -= start
        subconfig = {
            "total_frames": end - start,
            "text": [        
                {
                    "text": "Let's open a pack. What do you think we pull today?",
                    "first_frame": 0,
                    "last_frame": 70
                },
                {
                    "text": "Like and Subsribe",
                    "first_frame": 100,
                    "last_frame": 150
                },
                {
                    "text": "Did you like the pulls? Let me know in the comments",
                    "first_frame": end - start - 150,
                    "last_frame": end - start
                }
            ],
            "boosters": [booster]
        }
        subconfig_filename = f"cards-{os.path.basename(output_filename).replace('.', '-')}.json"
        subconfig_path = os.path.join(os.path.dirname(output_filename), subconfig_filename)
        with open(subconfig_path, 'w', encoding='utf-8') as json_file:
            json.dump(subconfig, json_file, indent=4)

        booster_count += 1

        

def main():
    parser = argparse.ArgumentParser(description="Config merge CLI")
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('input_file', help='Path to the input file')
    args = parser.parse_args()
    full_video_file = args.input_file
    base_name = os.path.basename(full_video_file)
    dir_name = os.path.dirname(full_video_file)
    config_file = os.path.join(dir_name, "cards-" + base_name.replace('.', '-') + ".json")
    split_video(full_video_file, config_file)

if __name__ == "__main__":
    main()