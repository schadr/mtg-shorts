def smooth_captions(frame_captions):
    smoothed_captions = []
    skipped_frames = 0
    last_caption = None
    for i in range(len(frame_captions)):
        if last_caption is not None and frame_captions[i] == ():
            skipped_frames += 1
        elif last_caption == frame_captions[i]:
            for j in range(skipped_frames + 1):
                smoothed_captions.append(last_caption)
            skipped_frames = 0
        else:
            for j in range(skipped_frames):
                smoothed_captions.append(())
            last_caption = frame_captions[i]
            smoothed_captions.append(last_caption)
            skipped_frames = 0
        if last_caption is None:
            smoothed_captions.append(frame_captions[i])
    for j in range(skipped_frames):
        smoothed_captions.append(())
    return smoothed_captions