from src.video import load_video
from src.video import extract_card_info
from src.video import load_text_detection

def test_load_video():
    assert load_video('files/test-video-720p.mov') != None

def test_extract_card_info():
    video = load_video('files/test-video-720p.mov')
    extract_card_info(video)

def test_load_text_dectection():
    assert load_text_detection((320, 320)) != None # update the size