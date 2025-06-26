from src.video import load_video
from src.video import extract_card_info

def test_load_video():
    assert load_video('files/test-video-720p.mov') != None

def test_extract_card_info():
    video = load_video('files/test-video-720p.mov')
    extract_card_info(video)