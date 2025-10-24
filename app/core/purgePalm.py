from typing import List
import cv2
import numpy as np
from mediapipe import solutions as mp_solutions

mp_hands = mp_solutions.hands


def crop_palm(image: np.ndarray) -> np.ndarray:
    if len(image.shape) == 2 or image.shape[2] == 1:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    else:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    with mp_hands.Hands(static_image_mode=True, max_num_hands=1) as hands:
        results = hands.process(image_rgb)
        if not results.multi_hand_landmarks:
            return image  # fallback if no hand detected

        hand_landmarks = results.multi_hand_landmarks[0]
        h, w = image.shape[:2]
        xs = [lm.x * w for lm in hand_landmarks.landmark]
        ys = [lm.y * h for lm in hand_landmarks.landmark]
        x_min, x_max = int(min(xs)), int(max(xs))
        y_min, y_max = int(min(ys)), int(max(ys))
        cropped = image[y_min:y_max, x_min:x_max]
        return cropped