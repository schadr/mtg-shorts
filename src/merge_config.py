import argparse
import json
import os



def main():
    parser = argparse.ArgumentParser(description="Config merge CLI")
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('--folder', type=str, help='Folder containing config files to be merged.')
    args = parser.parse_args()

    merged_config = {"total_frames": 0, "text": [{"text": "Let's open a booster diplay! Wish me luck!", "first_frame": 0, "last_frame": 250}, {"text": "Like and Subscribe!", "first_frame": 251, "last_frame": 340}], "boosters": []}

    json_files = [f for f in os.listdir(args.folder) if f.endswith('.json')]

    booster_count = -1
    for item in json_files:
        booster_count += 1
        with open(os.path.join(args.folder, item), 'r', encoding='utf-8') as f:
            data = json.load(f)
        new_total_frames = data["total_frames"]
        new_boosters = data["boosters"]
        off_set = merged_config["total_frames"]
        

        for booster in new_boosters:
            for card in booster:
                card["first_frame"] += off_set
                card["last_frame"] += off_set if card["last_frame"] != 0 else 0
            merged_config["boosters"].append(booster)
        if len(new_boosters) != 0:
            text = {"text": f"booster {booster_count} / {len(json_files)-1}. What will we pull?", "first_frame": off_set+1, "last_frame": off_set+1+150}
            merged_config["text"].append(text)
        merged_config["total_frames"] += new_total_frames
    output_file = os.path.join(args.folder, 'cards-merged-mp4.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_config, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()