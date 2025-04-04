import cv2
import numpy as np
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "database", "raw_normalized")
REF_DIR = os.path.join(BASE_DIR, "database", "references")

def extract_orb_features(image):
    orb = cv2.ORB_create(nfeatures=500)
    kp, des = orb.detectAndCompute(image, None)
    return des

def get_probe_image_path(filename):
    return os.path.join(RAW_DIR, filename)

def match_probe_to_references(probe_filename):
    probe_path = get_probe_image_path(probe_filename)
    probe_img = cv2.imread(probe_path, cv2.IMREAD_GRAYSCALE)
    probe_des = extract_orb_features(probe_img)

    if probe_des is None:
        return []

    matches_info = []

    for ref_file in os.listdir(REF_DIR):
        if not ref_file.endswith((".png", ".jpg")):
            continue

        ref_path = os.path.join(REF_DIR, ref_file)
        ref_img = cv2.imread(ref_path, cv2.IMREAD_GRAYSCALE)
        ref_des = extract_orb_features(ref_img)

        if ref_des is None:
            continue

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(probe_des, ref_des)

        if len(matches) == 0:
            continue

        avg_distance = np.mean([m.distance for m in matches])
        matches_info.append({
            "ref_image": ref_file,
            "score": float(avg_distance),
            "path": ref_path
        })

    # Sort by ascending distance (best matches first)
    matches_info.sort(key=lambda x: x["score"])
    return matches_info[:5]
