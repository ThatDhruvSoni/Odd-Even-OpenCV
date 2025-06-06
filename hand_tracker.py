import cv2
import mediapipe as mp
import math

mp_hands = mp.solutions.hands # References Hands module from mediapipe
mp_draw = mp.solutions.drawing_utils # Mediapipe's drawing utility

# Instance of Hand detector with max number of hands detected set to 1 and the minimum confidence threshold to be 70%
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7) 


"""
Function to calculate the euclidean distance between 2 points in space a and b
"""
def euclidean_distance(a, b):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2) # Returns the euclidean distance between a and b


"""
count_fingers() is a function that is used to return the number of fingers the user is extending at the moment
It has one parameter
    hand_landmarks: Landmarks of the hand detected by mediapipe

We use various checks to determine if the thumb and the other fingers are extended

The check for other fingers is simple, if the tip of the finger is higher up than the pip, we consider them extended

The check of the thumb is more complicated, we consider the minimum distance of the tip of the thumb to the bases of the other
fingers and the middle of the middle finger, if the euclidean distance is over 0.085 or 8.5% of the diagonal length of the image,
we consider the thumb to be extended

The function returns the number of fingers extended
"""
def count_fingers(hand_landmarks):

    # Count of fingers extended
    count = 0

    thumb_tip = hand_landmarks.landmark[4] # Tip of thumb
    index_base = hand_landmarks.landmark[5] # Base of index finger
    middle_base = hand_landmarks.landmark[9] # Base of middle finger
    ring_base = hand_landmarks.landmark[13] # Base of ring finger
    pinky_base = hand_landmarks.landmark[17] # Base of pinky finger
    middle_middle = hand_landmarks.landmark[10] # Middle of middle finger

    # Distance between thumb tip and finger bases and middle of middle finger
    dist_to_index = euclidean_distance(thumb_tip, index_base)
    dist_to_middle = euclidean_distance(thumb_tip, middle_base)
    dist_to_ring = euclidean_distance(thumb_tip, ring_base)
    dist_to_pinky = euclidean_distance(thumb_tip, pinky_base)
    dist_to_middle_middle = euclidean_distance(thumb_tip, middle_middle)


    # Consider thumb folded if it's close to either finger base or to the middle of the middle finger
    # Along with a threshold based choice to determine if thumb is extended
    if min(dist_to_index, dist_to_middle, dist_to_ring, dist_to_pinky, dist_to_middle_middle) > 0.085:  
        count += 1

    # Tips and pips for other fingers
    finger_tips = [8, 12, 16, 20]
    finger_pips = [6, 10, 14, 18]

    # If the tip of a finger is higher up (in terms of y coordinates) than the pip, we consider it to be extended
    for tip, pip in zip(finger_tips, finger_pips):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y: # y coordinates decrease as we go up
            count += 1

    # Return the number of fingers extended
    return count


"""
The function detect_hand_and_count_fingers is used to detect a hand and return the number of fingers that are extended
as well as draw landmarks on the hand.
The function has one parameter:
    frame: The current frame collected from the webcam of the user

"""

def detect_hand_and_count_fingers(frame):
    # Converts image from BGR to RGB since mediapipe expects RGB but OpenCV collects in BGR
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 

    # Passes the image to the hands model, which processes it and returns the detected hand landmarks, if there are any
    result = hands.process(img_rgb)

    # Number of fingers extended
    finger_count = None

    # If the multi_hand_landmarks list is not None, that is, we have landmarks from hands
    if result.multi_hand_landmarks:

        # For a single hand's landmarks in the list of landmarks
        for handLms in result.multi_hand_landmarks:

            # Draw landmarks and connections of the hand directly on the frame
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

            # Count the number of fingers present based on the landmarks of the hand
            finger_count = count_fingers(handLms)

    # Return the frame with annotations drawn on it, and number of fingers
    return frame, finger_count