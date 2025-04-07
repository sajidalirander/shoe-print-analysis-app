import os
import cv2


BASE_DIR = os.getcwd()
RAW_DIR = os.path.join(BASE_DIR, "database", "raw_normalized")
REF_DIR = os.path.join(BASE_DIR, "database", "references")

def extract_orb_features(image):
    orb = cv2.ORB_create(nfeatures=500)
    _, descriptors = orb.detectAndCompute(image, None)
    return descriptors

def compute_match_score(des1, des2):
    if des1 is None or des2 is None:
        return float('inf')
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = matcher.match(des1, des2)
    if not matches:
        return float('inf')
    avg_dist = sum(m.distance for m in matches) / len(matches)
    return avg_dist

def match_probe_to_references(filename, top_k=5):
    probe_path = os.path.join(RAW_DIR, filename)
    if not os.path.exists(probe_path):
        return []

    probe_img = cv2.imread(probe_path, cv2.IMREAD_GRAYSCALE)
    des1 = extract_orb_features(probe_img)

    scores = []
    for ref_file in os.listdir(REF_DIR):
        ref_path = os.path.join(REF_DIR, ref_file)
        ref_img = cv2.imread(ref_path, cv2.IMREAD_GRAYSCALE)
        des2 = extract_orb_features(ref_img)
        score = compute_match_score(des1, des2)
        scores.append((ref_file, score, ref_path))

    scores.sort(key=lambda x: x[1])
    return [{"file": f, "score": s, "path": p} for f, s, p in scores[:top_k]]

def list_probe_files():
    return sorted([f for f in os.listdir(RAW_DIR)
                   if f.lower().endswith((".png", ".jpg", ".jpeg"))
                   ])
