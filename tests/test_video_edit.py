from src.video import load_video
from src.video import add_card_info_to_frame
from src.video import add_card_info_to_video
from src.pricing import Card

import cv2

def test_add_card_info_to_frame():
    image = cv2.imread('files/test-picture-of-card.png')
    add_card_info_to_frame(image, "Cornered by Black Mages", "$"+str(1.12))

def test_add_card_info_to_video():
    video = load_video('files/test-video-720p.mov')
    info = []
    for i in range(691): # the video has 691 frames
        card = Card("uuid", f"Frame {i}", i, "FIN")
        card.price = i
        card.price_foil = i * 2
        info.append(card)
    mod_video = add_card_info_to_video(video, info)
    mod_video.release()
    assert mod_video != None