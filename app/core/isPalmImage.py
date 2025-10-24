import cv2
import numpy as np
import mediapipe as mp
import base64

# -------------------------
# Initialize MediaPipe Hands
# -------------------------
mp_hands = mp.solutions.hands

def is_palm_image(image: np.ndarray, hand: str = None, min_detection_confidence: float = 0.7) -> bool:
    """
    Check if an image contains a palm (hand).
    
    Args:
        image: OpenCV BGR or grayscale image (numpy array)
        hand: Optional, 'left' or 'right' to enforce hand orientation
        min_detection_confidence: float between 0-1, confidence threshold
    
    Returns:
        True if a palm is detected (and matches hand if specified), False otherwise
    """
    # Convert grayscale to RGB if needed
    if len(image.shape) == 2 or image.shape[2] == 1:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    else:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    with mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=1,
        min_detection_confidence=min_detection_confidence
    ) as hands:
        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:
            detected_hand = results.multi_handedness[0].classification[0].label.lower()  # 'left' or 'right'
            if hand:
                return detected_hand == hand.lower()
            return True
        else:
            return False


def base64_to_cv2(base64_str: str) -> np.ndarray:
    img_bytes = base64.b64decode(base64_str)
    arr = np.frombuffer(img_bytes, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return img