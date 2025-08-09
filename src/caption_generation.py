import json


def smooth_captions(frame_captions):
    smoothed_captions = []
    skipped_frames = 0
    last_caption = None
    for i in range(len(frame_captions)):
        if last_caption is not None and frame_captions[i] == ():
            skipped_frames += 1
        elif last_caption == frame_captions[i]:
            for j in range(skipped_frames + 1):
                smoothed_captions.append(last_caption)
            skipped_frames = 0
        else:
            for j in range(skipped_frames):
                smoothed_captions.append(())
            last_caption = frame_captions[i]
            smoothed_captions.append(last_caption)
            skipped_frames = 0
        if last_caption is None:
            smoothed_captions.append(frame_captions[i])
    for j in range(skipped_frames):
        smoothed_captions.append(())
    return smoothed_captions

def load_captions_from_file(file_path):
    data = None
    with open(file_path, 'r') as file:
        data = json.load(file)
    smoothed_captions = []
    text_in_frame = {}
    current_index = 0
    for text in data["text"]:
        start = int(text["first_frame"])
        end = int(text["last_frame"])
        text_text = text["text"]
        for i in range(start,end):
            text_in_frame[i] = text_text

    for booster in data["boosters"]:
        num_cards = 0
        for card in booster:
            start = card["first_frame"]
            end = card["last_frame"]
            if end == 0 and num_cards + 1 < len(booster):
                end = booster[num_cards + 1]["first_frame"] - 10
            for i in range(current_index, start):
                smoothed_captions.append(())
            for i in range(start, end + 1):
                smoothed_captions.append((card["mtg_set"], card["card_number"], card["foil"] if "foil" in card else False))
            current_index = end + 1
            num_cards += 1
    for i in range(current_index, int(data["total_frames"])+1):
        smoothed_captions.append(())
    return smoothed_captions, text_in_frame