import sys
import os
import cv2
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QDialog, QListWidget,
    QListWidgetItem, QVBoxLayout as QVBox, QWidget as QW
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


# Paths
ROOT = "./database"
RAW_DIR = f"{ROOT}/raw_normalized"
REF_DIR = f"{ROOT}/references"

# --- ORB Feature Extractor ---
def extract_orb_features(image):
    orb = cv2.ORB_create(nfeatures=500)
    keypoints, descriptors = orb.detectAndCompute(image, None)
    return keypoints, descriptors

# --- Image Selector Dialog ---
class ImageSelectorDialog(QDialog):
    def __init__(self, image_dir):
        super().__init__()
        self.setWindowTitle("Select Probe Image")
        self.selected_image = None

        layout = QVBoxLayout()
        self.list_widget = QListWidget()

        for file in sorted(os.listdir(image_dir)):
            if file.endswith((".jpg", ".png")):
                item = QListWidgetItem(file)
                self.list_widget.addItem(item)

        self.list_widget.itemClicked.connect(self.select_image)
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

    def select_image(self, item):
        self.selected_image = item.text()
        self.accept()

# --- Main App Window ---
class ShoeprintMatcherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shoeprint Matcher")
        self.setGeometry(100, 100, 1400, 700)

        self.image_label = QLabel("Selected probe image will appear here")
        self.image_label.setAlignment(Qt.AlignCenter)

        self.button = QPushButton("Select Probe Image")
        self.button.clicked.connect(self.open_image_dialog)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.image_label)

        # Match result area
        self.results_layout = QHBoxLayout()
        layout.addLayout(self.results_layout)

        self.setLayout(layout)

    def open_image_dialog(self):
        dialog = ImageSelectorDialog(RAW_DIR)
        if dialog.exec_():
            filename = dialog.selected_image
            full_path = os.path.join(RAW_DIR, filename)

            # Show probe image
            pixmap = QPixmap(full_path).scaledToWidth(300, Qt.SmoothTransformation)
            self.image_label.setPixmap(pixmap)
            self.image_label.setText("")

            # Start matching process
            probe_img = cv2.imread(full_path, cv2.IMREAD_GRAYSCALE)
            _, probe_des = extract_orb_features(probe_img)

            results = []
            for ref_file in sorted(os.listdir(REF_DIR)):
                if not ref_file.endswith(".png"):
                    continue

                ref_path = os.path.join(REF_DIR, ref_file)
                ref_img = cv2.imread(ref_path, cv2.IMREAD_GRAYSCALE)
                _, ref_des = extract_orb_features(ref_img)

                if probe_des is None or ref_des is None or len(probe_des) == 0 or len(ref_des) == 0:
                    continue

                bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
                matches = bf.match(probe_des, ref_des)
                if len(matches) == 0:
                    continue

                avg_distance = np.mean([m.distance for m in matches])
                results.append((ref_path, avg_distance))

            results.sort(key=lambda x: x[1])
            top5 = results[:5]

            self.display_matches(top5)

    def display_matches(self, match_results):
        # Clear previous matches
        while self.results_layout.count():
            child = self.results_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for ref_path, score in match_results:
            label = QLabel()
            pixmap = QPixmap(ref_path).scaledToWidth(200, Qt.SmoothTransformation)
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignCenter)

            score_label = QLabel(f"Score: {score:.2f}")
            score_label.setAlignment(Qt.AlignCenter)

            vbox = QVBox()
            vbox.addWidget(label)
            vbox.addWidget(score_label)

            container = QW()
            container.setLayout(vbox)
            self.results_layout.addWidget(container)

# --- Run the App ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShoeprintMatcherApp()
    window.show()
    sys.exit(app.exec_())
