import os

from src.mtgs import create_fps_video

def test_create_fps_video():
    create_fps_video("files/test-video-720p.mov")
    assert os.path.exists("files/frame-test-video-720p.mov")
    assert os.path.exists("files/cards-test-video-720p-mov.json")

def test_create_fps_video_collector():
    create_fps_video("files/test-video-720p.mov", True)
    assert os.path.exists("files/frame-test-video-720p.mov")
    assert os.path.exists("files/cards-test-video-720p-mov.json")