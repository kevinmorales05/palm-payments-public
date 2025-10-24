import cv2
import numpy as np
import base64
import hmac
import hashlib
from typing import Optional, List
from pydantic import BaseModel, Field

from app.core.purgePalm import crop_palm

# -------------------------
# BiometricImage model
# -------------------------
class BiometricImage(BaseModel):
    image_id: Optional[str] = Field(None, description="Optional image identifier")
    image_base64: str = Field(..., description="Base64-encoded palm image")
    hand: Optional[str] = Field(None, description="Which hand: 'left' or 'right'")
    position: Optional[str] = Field(None, description="Optional capture angle or position info")

# -------------------------
# Base64 -> OpenCV grayscale
# -------------------------
def base64_to_cv2(base64_str: str) -> np.ndarray:
    img_bytes = base64.b64decode(base64_str)
    arr = np.frombuffer(img_bytes, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Cannot decode image from base64")
    return img

# -------------------------
# ORB descriptors -> fixed vector
# -------------------------
def extract_orb_template_from_cv2(img: np.ndarray, template_dim=128) -> np.ndarray:
    orb = cv2.ORB_create(nfeatures=500)
    kps, des = orb.detectAndCompute(img, None)
    if des is None:
        des = np.zeros((0, 32), dtype=np.float32)
    else:
        des = des.astype(np.float32)
    mean = des.mean(axis=0) if des.shape[0] > 0 else np.zeros(32, dtype=np.float32)
    std = des.std(axis=0) if des.shape[0] > 0 else np.zeros(32, dtype=np.float32)
    vec = np.concatenate([mean, std])
    if vec.size < template_dim:
        vec = np.tile(vec, int(np.ceil(template_dim / vec.size)))[:template_dim]
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec /= norm
    return vec.astype(np.float32)

# -------------------------
# Secure hashed template
# -------------------------
def create_secure_template(vec: np.ndarray, secret_key: bytes, bits_per_feature: int = 8) -> List[str]:
    """Quantize vector and HMAC each feature to create a secure template"""
    q = np.floor((vec + 1.0) / 2.0 * (2**bits_per_feature - 1)).astype(int)
    hashes = [hmac.new(secret_key, val.to_bytes(1, 'big'), hashlib.sha256).hexdigest() for val in q]
    return hashes

# -------------------------
# Compare secure templates
# -------------------------
def compare_secure_templates(template1: List[str], template2: List[str]) -> float:
    if len(template1) != len(template2):
        raise ValueError("Template length mismatch")
    matches = sum(h1 == h2 for h1, h2 in zip(template1, template2))
    return matches / len(template1)  # similarity fraction 0..1

# -------------------------
# Register palm images
# -------------------------
def register_palm_images(images: List[BiometricImage], secret_key: bytes, template_dim: int = 128, hand: str = None) -> List[str]:
    """
    Generate secure template from one or multiple images, validating and cropping palms.
    """
    templates = []
    for img_obj in images:
        cv2_img = base64_to_cv2(img_obj.image_base64)
        
        # 1. Crop to palm region
        cropped_img = crop_palm(cv2_img)

        # 2. Extract ORB template
        vec = extract_orb_template_from_cv2(cropped_img, template_dim)
        templates.append(vec)

    # 3. Aggregate multiple images
    avg_template = np.mean(np.stack(templates), axis=0)

    # 4. Create secure hashed template
    secure_template = create_secure_template(avg_template, secret_key)
    return secure_template


# -------------------------
# Validate palm image
# -------------------------
def validate_palm_image(new_image: BiometricImage, stored_secure_template: List[str],
                        secret_key: bytes, template_dim: int = 128, threshold: float = 0.75) -> bool:
     # 1. Convert base64 to OpenCV image
    cv2_img = base64_to_cv2(new_image.image_base64)
    # 2. Crop to palm region
    cropped_img = crop_palm(cv2_img)

    # 4. Extract ORB features from cropped palm
    vec = extract_orb_template_from_cv2(cropped_img, template_dim)

    # 5. Create secure hashed template
    new_secure = create_secure_template(vec, secret_key)

    # 6. Compare with stored template
    similarity = compare_secure_templates(stored_secure_template, new_secure)
    print(f"Similarity fraction: {similarity:.4f}")

    # 7. Return whether similarity exceeds threshold
    return similarity >= threshold

# -------------------------
# Example usage
# -------------------------
if __name__ == "__main__":
    # Secret key for HMAC (keep this secure!)
    secret_key = b"super-secret-key"

    # Registration: list of BiometricImage objects
    registration_images = [
        BiometricImage(image_base64="iVBORw0KGgoAAAANSUhEUgAA..."),
        BiometricImage(image_base64="iVBORw0KGgoAAAANSUhEUgBB...")
    ]

    stored_secure_template = register_palm_images(registration_images, secret_key)
    print("Secure template stored (hashed):", stored_secure_template[:5], "...")  # truncated display

    # Validation: new BiometricImage
    new_image = BiometricImage(image_base64="iVBORw0KGgoAAAANSUhEUgCC...")
    match = validate_palm_image(new_image, stored_secure_template, secret_key)
    print("Palm image match:", match)
