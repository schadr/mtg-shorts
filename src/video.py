import cv2
from google import genai

def load_video(file_uri):
    vid = cv2.VideoCapture(file_uri)
    if vid.isOpened():
        return vid
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
    return card_number, mtg_set

def extract_card_info_from_video(video):
    cards_in_frame = []
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            print("Last frame reached")
            break
        cv2.imwrite("tmp.jpg", frame)
        card_number, mtg_set = extract_card_info_from_image("tmp.jpg")
        cards_in_frame.append((card_number, mtg_set))
    return cards_in_frame

def add_card_info_to_frame(frame, text, price):
    cv2.putText(frame, f"{text}", (10, 80),  cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 0, 0), 2)
    cv2.putText(frame, f"{price}", (530, 160), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 2)
    return frame

def add_card_info_to_video(video, cards_in_frame):
    frame_number = 0
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    out = cv2.VideoWriter('tmp.mp4', fourcc, fps, (width, height))

    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            print("Last frame reached")
            break
        mod_frame = frame
        if cards_in_frame[frame_number] != None:
            mod_frame = add_card_info_to_frame(frame, cards_in_frame[frame_number].name, f"${cards_in_frame[frame_number].price}")
        out.write(mod_frame) 
        frame_number += 1
    return out