import cv2

from src.video import add_card_info_to_frame, add_message_to_center

def test_card_style_below_value():
    image = cv2.imread('files/test-picture-of-card.png')
    add_card_info_to_frame(image, "Cornered by Black Mages", "$1.12", 2.12, 5.0)
    cv2.imwrite('style.png', image)

def test_card_style_at_value():
    image = cv2.imread('files/test-picture-of-card.png')
    add_card_info_to_frame(image, "Cornered by Black Mages", "$1.12", 5.0, 5.0)
    cv2.imwrite('style.png', image)

def test_card_style_above_value():
    image = cv2.imread('files/test-picture-of-card.png')
    add_card_info_to_frame(image, "Cornered by Black Mages", "$1.12", 6.0, 5.0)
    cv2.imwrite('style.png', image)


def test_center_message_sinlge_line():
    image = cv2.imread('files/test-picture-of-card.png')
    add_message_to_center(image, "Cornered by Black Mages")
    cv2.imwrite('style.png', image)

def test_center_message_multi_line():
    image = cv2.imread('files/test-picture-of-card.png')
    add_message_to_center(image, "Cornered by Black Mages Cornered by Black Mages Cornered by Black Mages Cornered by Black Mages Cornered by Black Mages Cornered by Black Mages Cornered by Black Mages Cornered by Black Mages Cornered by Black Mages")
    cv2.imwrite('style.png', image)