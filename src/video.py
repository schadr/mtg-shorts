import cv2 as cv

def load_video(file_uri):
    vid = cv.VideoCapture(file_uri)
    if vid.isOpened():
        return vid
    vid.release()
    return None

def extract_card_info(video):
    i = 0
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            print("Last frame reached")
            break
        print(f"Read frame {i}")
        i += 1