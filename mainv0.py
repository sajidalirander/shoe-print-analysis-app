import cv2
import os
import numpy as np
from tqdm import tqdm

# Paths
ROOT = "./database"
SAMPLE_DIR = f"{ROOT}/raw"
REFERENCE_DIR = f"{ROOT}/references"

# ORB feature extractor
def extract_orb_features(image):
    orb = cv2.ORB_create(nfeatures=500)
    keypoints, descriptors = orb.detectAndCompute(image, None)
    return keypoints, descriptors

# Match features using Brute-Force Matcher
def match_descriptors(des1, des2):
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)
    return matches

# Load grayscale image
def load_image(path):
    return cv2.imread(path, cv2.IMREAD_GRAYSCALE)

# Compare one probe image to all references and return ranked matches
def match_probe_to_references(probe_path):
    probe_img = load_image(probe_path)
    kp1, des1 = extract_orb_features(probe_img)

    results = []

    for ref_file in tqdm(os.listdir(REFERENCE_DIR), desc="Matching"):
        ref_path = os.path.join(REFERENCE_DIR, ref_file)
        ref_img = load_image(ref_path)
        kp2, des2 = extract_orb_features(ref_img)

        if des1 is None or des2 is None:
            continue

        matches = match_descriptors(des1, des2)
        total_distance = sum([m.distance for m in matches])
        avg_distance = total_distance / len(matches) if matches else 1e9

        results.append((ref_file, avg_distance, matches, ref_img, kp2))

    # Sort results by ascending average distance
    results.sort(key=lambda x: x[1])
    return results[:5], probe_img, kp1

# Display probe vs best match
def display_top_matches(probe_img, top_matches):
    match_images = []
    scale_width = 900  # standard match image width

    for i, (ref_file, _, _, ref_img, _) in enumerate(top_matches):
        print(f"Match {i+1}: {ref_file}")

        # Resize reference image
        h, w = ref_img.shape[:2]
        new_h = int(scale_width * h / w)
        resized_match = cv2.resize(ref_img, (scale_width, new_h))

        # Convert to BGR and add label
        if len(resized_match.shape) == 2:
            resized_match = cv2.cvtColor(resized_match, cv2.COLOR_GRAY2BGR)

        cv2.putText(resized_match, f"Match #{i+1}: {ref_file}",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        match_images.append(resized_match)

    # Stack all match images vertically
    match_panel = cv2.vconcat(match_images)

    # Resize probe image to match panel height
    probe_height = match_panel.shape[0]
    probe_width = int(probe_img.shape[1] * (probe_height / probe_img.shape[0]))
    probe_resized = cv2.resize(probe_img, (probe_width, probe_height))
    probe_resized = cv2.cvtColor(probe_resized, cv2.COLOR_GRAY2BGR)

    # Final side-by-side layout
    final_result = cv2.hconcat([probe_resized, match_panel])

    # Show result
    window_name = "Top 5 Visual Matches (No Keypoints)"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(window_name, final_result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



if __name__ == "__main__":
    # Choose a test probe image
    probe_image_name = "00001.jpg"  # Change as needed
    probe_path = os.path.join(SAMPLE_DIR, probe_image_name)

    top_matches, probe_img, kp1 = match_probe_to_references(probe_path)
    if not top_matches:
        print("[WARNING] No matches found.")
        exit()
        
    print("\nTop 5 Matches:")
    for i, (ref_file, avg_dist, _, _, _) in enumerate(top_matches):
        print(f"{i+1}. {ref_file} | Avg Distance: {avg_dist:.2f}")

    # Show best match visually
    display_top_matches(probe_img, top_matches)
