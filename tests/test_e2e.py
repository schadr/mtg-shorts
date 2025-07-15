import cv2
from src.pricing import convert_to_cards, create_totals
from src.video import add_coin_sound_effects, load_video
from src.video import add_card_info_to_video

from tests.test_video_frames import build_frames

def test_e2e_no_ocr():
    frames = build_frames()
    cards_per_frame = convert_to_cards(frames)
    totals_per_frame = create_totals(cards_per_frame, 5.0)
    video = load_video('files/test-video-720p.mov')
    mod_video = add_card_info_to_video(video, {}, cards_per_frame, totals_per_frame, 5.0, 0.3)
    mod_video.release()
    add_coin_sound_effects("tmp.mp4", cards_per_frame, video.get(cv2.CAP_PROP_FPS), "files/test-video-720p.mov")