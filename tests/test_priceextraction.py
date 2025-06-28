from src.video import load_video
from src.video import extract_card_info_from_image
from src.video import extract_card_info_from_video
from src.video import add_card_info_to_frame


import cv2
import pytesseract

def test_load_video():
    assert load_video('files/test-video-720p.mov') != None

def test_card_image():
    card_number, mtg_set = extract_card_info_from_image('files/test-picture-of-card.png')

    assert card_number == 93
    assert mtg_set == "FIN"

def test_no_card_image():
    card_number, mtg_set = extract_card_info_from_image('files/test-no-card.png')
    
    assert card_number == None
    assert mtg_set == None

def test_full_video():
    cards_in_frame = extract_card_info_from_video(load_video('files/test-video-720p.mov'))
    assert len(cards_in_frame) == 691
    # todo verify the frames have the correct card numbers and sets

def test_add_card_info_to_frame():
    image = cv2.imread('files/test-picture-of-card.png')
    add_card_info_to_frame(image, "Cornered by Black Mages", "$"+str(1.12))