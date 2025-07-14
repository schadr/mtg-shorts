import math
import cv2
from google import genai

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
    textSize, _ = cv2.getTextSize(f"{text}", cv2.FONT_HERSHEY_TRIPLEX, 1, 2)
    cv2.putText(frame, f"{text}", (10, 50),  cv2.FONT_HERSHEY_TRIPLEX, min(1.0, (width-20)/textSize[0]), (0, 0, 0), 10)
    cv2.putText(frame, f"{text}", (10, 50),  cv2.FONT_HERSHEY_TRIPLEX, min(1.0, (width-20)/textSize[0]), (255, 255, 255), 2)
    
    # card value
    textSize, _ = cv2.getTextSize(f"{price}", cv2.FONT_HERSHEY_SIMPLEX, 1.5, 2)
    cv2.putText(frame, f"{price}", (width-40-textSize[0], 120), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 8)
    cv2.putText(frame, f"{price}", (width-40-textSize[0], 120), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (57, 255, 20), 2)
    
    # pack value
    textSize, _ = cv2.getTextSize(f"${total:.2f}/${cost:.2f}", cv2.FONT_HERSHEY_SIMPLEX, 1.5, 2)
    x = int((width - textSize[0])/2)
    pack_value_color = (0,0,255) if (total/cost) < 1 else (0,255,0)
    cv2.putText(frame, f"${total:.2f}/${cost:.2f}", (x, height - textSize[1] - 30), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 8)
    cv2.putText(frame, f"${total:.2f}/${cost:.2f}", (x, height - textSize[1] - 30), cv2.FONT_HERSHEY_SIMPLEX, 1.5, pack_value_color, 2)
    
    # right side box
    bar_width = 40
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

def add_card_info_to_video(video, cards_in_frame, total_in_frame, cost, output_file='tmp.mp4', fps=None):
    frame_number = 0
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if fps is None:
        fps = video.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            print("Last frame reached")
            break
        mod_frame = frame
        if cards_in_frame[frame_number] != None:
            mod_frame = add_card_info_to_frame(frame, cards_in_frame[frame_number].name, f"${cards_in_frame[frame_number].price}", total_in_frame[frame_number], cost)
        else:
            mod_frame = add_card_info_to_frame(frame, "", "", total_in_frame[frame_number], cost)
        out.write(mod_frame) 
        frame_number += 1
    return out