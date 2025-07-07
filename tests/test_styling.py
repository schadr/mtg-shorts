import cv2

from src.video import add_card_info_to_frame

def test_card_style():
    image = cv2.imread('files/test-picture-of-card.png')
    add_card_info_to_frame(image, "Cornered by Black Mages", "$1.12", 2.12, 5.0)
    cv2.imwrite('style.png', image)