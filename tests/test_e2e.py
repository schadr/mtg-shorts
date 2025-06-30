from src.pricing import convert_to_cards
from src.video import load_video
from src.video import add_card_info_to_video

from tests.test_video_frames import build_frames

def test_e2e_no_ocr():
    frames = build_frames()
    cards_per_frame = convert_to_cards(frames)
    video = load_video('files/test-video-720p.mov')
    mod_video = add_card_info_to_video(video, cards_per_frame)
    mod_video.release()