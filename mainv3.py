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

import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "database", "raw_normalized")
REF_DIR = os.path.join(BASE_DIR, "database", "references")

API_BASE = "http://127.0.0.1:8000/api"

# --- ORB Feature Extractor ---
def extract_orb_features(image):
    orb = cv2.ORB_create(nfeatures=500)
    keypoints, descriptors = orb.detectAndCompute(image, None)
    return keypoints, descriptors

# --- Image Selector Dialog ---
class ImageSelectorDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Probe Image")
        self.selected_image = None

        layout = QVBoxLayout()
        self.list_widget = QListWidget()

        try:
            response = requests.get(f"{API_BASE}/shoeprints")
            probe_files = response.json().get("files", [])
        except Exception as e:
            print(f"[ERROR] Failed to fetch probe images: {e}")
            probe_files = []

        for file in probe_files:
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
        dialog = ImageSelectorDialog()
        if dialog.exec_():
            filename = dialog.selected_image
            probe_path = os.path.join(RAW_DIR, filename)

            # Show probe image
            pixmap = QPixmap(probe_path).scaledToWidth(300, Qt.SmoothTransformation)
            self.image_label.setPixmap(pixmap)
            self.image_label.setText("")

            try:
                response = requests.get(f"{API_BASE}/match/{filename}")
                results = response.json().get("top_matches", [])
                self.display_matches(results)
            except Exception as e:
                print(f"[ERROR] Failed to match image: {e}")

    def display_matches(self, match_results):
        # Clear previous matches
        while self.results_layout.count():
            child = self.results_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for match in match_results:
            ref_path = match["path"]
            score = match["score"]

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
