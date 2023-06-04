def test():
    import cv2

    cap = cv2.VideoCapture(0)

    phototwofinger = cv2.imread("data/images/two-finger/image-0.png")

    #  pip install cvzone, mediapipe
    from cvzone.HandTrackingModule import HandDetector

    detector = HandDetector(maxHands=1)

    fPhoto = detector.findHands(phototwofinger, draw=False)

    cv2.imshow("my photo", phototwofinger)
    print(cv2.waitKey())
    cv2.destroyAllWindows()

    hand = detector.findHands(phototwofinger, draw=False)
    if hand:
        lmList = hand[0]
        totalFinger = detector.fingersUp(lmList)
        if totalFinger == [0, 1, 1, 0, 0]:
            print("i know 2 finger is up")
        elif totalFinger == [0, 1, 0, 0, 0]:
            print("i know 1 finger is up")
        else:
            print("No finger is up.")


import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)


def detectHand(image):
    detector = HandDetector(maxHands=1)
    hand = detector.findHands(image, draw=False)
    totalFinger = None
    if hand:
        lmList = hand[0]
        totalFinger = detector.fingersUp(lmList)
    return totalFinger


def liveDetector():
    while True:
        status, photo = cap.read()

        cv2.imshow("my photo", photo)
        detection = detectHand(photo)

        if detection != None:
            print(detection)

        if cv2.waitKey(100) == 27:
            break

    cv2.destroyAllWindows()
    cap.release()
