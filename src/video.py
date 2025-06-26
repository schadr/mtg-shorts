import cv2 as cv
import urllib.request
import tarfile
import io

def load_video(file_uri):
    vid = cv.VideoCapture(file_uri)
    if vid.isOpened():
        return vid
    vid.release()
    return None

def extract_card_info(video):
    i = 0
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            print("Last frame reached")
            break
        print(f"Read frame {i}")
        i += 1

east_uri = 'https://www.dropbox.com/s/r2ingd0l3zt8hxs/frozen_east_text_detection.tar.gz?dl=1'

def load_text_detection(inputSize):
    with urllib.request.urlopen(east_uri) as response:
            with tarfile.open(fileobj=response, mode="r:gz") as tar:
                tar.extractall(path=".")
    
    # values might need tuning
    conf_thresh = 0.8
    nms_thresh = 0.4
    mean = (122.67891434, 116.66876762, 104.00698793)
    
    textDetectorEAST = cv.dnn_TextDetectionModel_EAST('./frozen_east_text_detection.pb')
    textDetectorEAST.setConfidenceThreshold(conf_thresh)
    textDetectorEAST.setNMSThreshold(nms_thresh)
    textDetectorEAST.setInputParams(1.0, inputSize, mean, True)
    return textDetectorEAST