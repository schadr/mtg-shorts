import cv2
from google import genai
import textwrap
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip

from src.pricing import Rarity 
import os
import random

def load_video(file_uri):
    vid = cv2.VideoCapture(file_uri)
    if vid.isOpened():
        return vid
    print("Error: Could not open video file.")
    vid.release()
    return None

prompt = "Extract the collector number and the information that is below the collector number but before the EN/JP from the card, which is an exactly the three character long string." \
       + "Remove any character from the collector number." \
       + "Please show the collector number on the first line response and the other on the second line and nothing else." \
       + "If there is no readable card please return 'No card found'."

def get_ai_client():    
    client = genai.Client()
    return client

def extract_card_info_from_image(filename):
    client = get_ai_client()
    myfile = client.files.upload(file=filename)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            myfile,
            "\n\n",
            prompt
        ],
    )
    print(response.text)
    if response.text.replace(".","") == "No card found": # Gemini sometimes adds the .
        return None, None
    card_number = int(response.text.split('\n')[0])
    mtg_set = response.text.split('\n')[1]
    foil = False
    return card_number, mtg_set, foil

def extract_card_info_from_video(video):
    cards_in_frame = []
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            print("Last frame reached")
            break
        cv2.imwrite("tmp.jpg", frame)
        card_number, mtg_set, foil = extract_card_info_from_image("tmp.jpg")
        cards_in_frame.append((card_number, mtg_set, foil))
    return cards_in_frame

def add_card_info_to_frame(frame, text, price, total, cost):
    height, width, _ = frame.shape
    
    # card title
    textSize, _ = cv2.getTextSize(f"{text}", cv2.FONT_HERSHEY_TRIPLEX, 2, 2)
    cv2.putText(frame, f"{text}", (20, int(height * .1)),  cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 0, 0), 10)
    cv2.putText(frame, f"{text}", (20, int(height * .1)),  cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 255, 255), 2)
    
    # card value
    textSize, _ = cv2.getTextSize(f"{price}", cv2.FONT_HERSHEY_SIMPLEX, 2.5, 2)
    cv2.putText(frame, f"{price}", (width-60-textSize[0], int(height * .15)), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (0, 0, 0), 8)
    cv2.putText(frame, f"{price}", (width-60-textSize[0], int(height * .15)), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (57, 255, 20), 2)
    
    # pack value
    textSize, _ = cv2.getTextSize(f"${total:.2f}/${cost:.2f}", cv2.FONT_HERSHEY_SIMPLEX, 3.5, 2)
    x = int((width - textSize[0])/2)
    pack_value_color = (0,0,255) if (total/cost) < 1 else (0,255,0)
    cv2.putText(frame, f"${total:.2f}/${cost:.2f}", (x, int(height * .92) - textSize[1]), cv2.FONT_HERSHEY_SIMPLEX, 3.5, (0, 0, 0), 8)
    cv2.putText(frame, f"${total:.2f}/${cost:.2f}", (x, int(height * .92) - textSize[1]), cv2.FONT_HERSHEY_SIMPLEX, 3.5, pack_value_color, 2)
    
    # right side box
    bar_width = 60
    bar_height = int(height / (3/2))
    bar_x = width - 10
    bar_y = height - bar_height
    bar_fill = int(min(1.0,total / cost) * bar_height)

    # background
    cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (0,0,0), 8)
    #excess
    cv2.rectangle(frame, (bar_x, max(0, bar_y - (int(total / cost * bar_height) - bar_height)) ), (bar_x+bar_width, bar_y), (0,255,255), -1)
    #empty
    cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + (bar_height - bar_fill)), (0, 0, 255), -1)
    #filled
    cv2.rectangle(frame, (bar_x, bar_y + (bar_height - bar_fill)), (bar_x + bar_width, bar_y + bar_height), (0, 255, 0), -1)
    cv2.line(frame, (bar_x - 10, bar_y + (bar_height - bar_fill)), (bar_x + bar_width, bar_y + (bar_height - bar_fill)), (0, 0, 0), 3)

    return frame

def add_message_to_center(frame, message, offset=0, text_color=(255,255,255)):
    height, width, _ = frame.shape
    textSize, _ = cv2.getTextSize(message, cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
    
    wrapped_text = textwrap.wrap(message, max(1, int(len(message) / (max(1,textSize[0]) / width))))
    lines = len(wrapped_text)

    center_x = int(width/2)
    center_y = int(height/2) + offset

    for line_counter, line in enumerate(wrapped_text):
        textSize, _ = cv2.getTextSize(line, cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        off_set = int(lines / 2) - line_counter

        x = center_x - int(textSize[0]/2)
        y = center_y - int(textSize[1]/2) - off_set * (textSize[1] + 15)

        cv2.putText(frame, line, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 10)
        cv2.putText(frame, line, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, text_color, 5)
    return frame

rare_shout_outs = {
    0: "",
    1: "",
    2: "!!double rare!!",
    3: "!!!tripple rare!!",
}

def add_card_info_to_video(video, text_in_frame, cards_in_frame, total_in_frame, cost, output_file='tmp.mp4', rotate=False, fps=None, collector=False, value_threshold = 10.0):
    frame_number = 0
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    dim = (width, height) if rotate==False else (height, width)
    if fps is None:
        fps = video.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, dim)
    
    rare_set = set()
    print(int(video.get(cv2.CAP_PROP_FRAME_COUNT)))

    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        mod_frame = frame if rotate==False else cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        card = cards_in_frame[frame_number]
        rare_set = set()
        if card != None:
            card_price = card.price_foil if card.foil else card.price
            if card_price >= value_threshold:
                mod_frame = add_message_to_center(mod_frame, "Oh YEAH!!!!", -100, (0,255,0))
        if card != None and card.rarity in [Rarity.RARE, Rarity.MYTHIC] and not collector:
            rare_set.add(card.name)
            mod_frame = add_message_to_center(mod_frame, rare_shout_outs[len(rare_set)])
        if card != None:
            price = card.price_foil if card.foil else card.price
            mod_frame = add_card_info_to_frame(mod_frame, card.name, f"${price}", total_in_frame[frame_number], cost)
        else:
            mod_frame = add_card_info_to_frame(mod_frame, "", "", total_in_frame[frame_number], cost)
        if frame_number in text_in_frame:
            mod_frame = add_message_to_center(mod_frame, text_in_frame[frame_number])
        out.write(mod_frame) 
        frame_number += 1
    return out

def add_coin_sound_effects(video_file_path, cards_in_frame, fps = 24, original_audio_file_path=None, out_file_path=None, sound_effect_file_path="sound-effects/cashier-sound-effect.mp3"):
    video_clip = VideoFileClip(video_file_path)
    
    # find card transition frames
    card_transition_frames = []
    previous_card = None
    for i, card in enumerate(cards_in_frame):
        if (previous_card == None and card != None) or (card != None and previous_card.uuid != card.uuid):
            card_transition_frames.append(i)
            previous_card = card

    audio_clips = []
    if original_audio_file_path != None:
        print(original_audio_file_path)
        audio_clips.append(VideoFileClip(original_audio_file_path).audio)
    for frame in card_transition_frames:
        audio_clip = AudioFileClip(sound_effect_file_path)
        audio_clip = audio_clip.with_volume_scaled(0.15)
        start_time = frame / fps
        audio_clips.append(audio_clip.with_start(start_time))

    video_clip = video_clip.with_audio(CompositeAudioClip(audio_clips))
    if out_file_path == None:
        video_file_path_no_ext = os.path.splitext(video_file_path)[0]
        ext = os.path.splitext(video_file_path)[1]
        out_file_path = video_file_path_no_ext + "-audio" + ext
    video_clip.with_duration(video_clip.duration).write_videofile(out_file_path)
    video_clip.close()

def add_music(video_file_path, out_file_path, music_path="../music/edm"):
    video_clip = VideoFileClip(video_file_path)
    music_files = [f for f in os.listdir(music_path) if os.path.isfile(os.path.join(music_path, f))]
    if not music_files:
        raise FileNotFoundError(f"No music files found in {music_path}")
    audio_clips = [VideoFileClip(video_file_path).audio.with_volume_scaled(0.8)]
    audio_duration = 0
    while audio_duration < video_clip.duration:
        selected_music = os.path.join(music_path, random.choice(music_files))
        audio_clip = AudioFileClip(selected_music).with_start(audio_duration - min(10, audio_duration)).with_volume_scaled(0.5)
        if audio_duration + audio_clip.duration - min(10, audio_duration) > video_clip.duration:
            audio_clip = audio_clip.with_duration(video_clip.duration - audio_duration + min(10, audio_duration))
        audio_duration += audio_clip.duration - min(10, audio_duration)
        audio_clips.append(audio_clip)
    video_clip = video_clip.with_audio(CompositeAudioClip(audio_clips))
    video_clip.write_videofile(out_file_path)