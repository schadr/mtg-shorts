import cv2 as cv
from google import genai

def load_video(file_uri):
    vid = cv.VideoCapture(file_uri)
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
    if response.text == "No card found":
        return None, None
    card_number = int(response.text.split('\n')[0])
    mtg_set = response.text.split('\n')[1]
    return card_number, mtg_set