from src.caption_generation import smooth_captions

def test_smooth_caption():
    expected_caption = [(), (), ("FIN", 13), ("FIN", 13), ("FIN", 13), ("FIN", 13), (), (), ("FIN", 14), ("FIN", 14), ("FIN", 14), (), (), ("FIN", 15), (), (), ("FIN", 16), ()]

    frame_captions = [(),(),("FIN", 13),(),(),("FIN", 13),(),(),("FIN", 14),(),("FIN", 14),(),(),("FIN", 15),(),(),("FIN", 16),()]
    smoothed_caption = smooth_captions(frame_captions)
    assert len(smoothed_caption) == len(frame_captions), "Smoothed caption length should match input frame captions length"
    assert smoothed_caption[0] == (), "First frame caption should remain empty"
    assert smoothed_caption[-1] == (), "Last frame caption should remain empty"
    assert smoothed_caption == expected_caption, f"Expected {expected_caption}, but got {smoothed_caption}"