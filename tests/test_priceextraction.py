from src.video import load_video
from src.video import extract_card_info_from_image


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