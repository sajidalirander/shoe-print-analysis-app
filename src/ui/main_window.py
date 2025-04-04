# src/ui/main_window.py

import os
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from ui.image_selector import ImageSelectorDialog
from ui.components import create_match_widget
from api.backend_client import get_match_results

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "backend", "database", "raw_normalized")

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

            results = get_match_results(filename)
            self.display_matches(results)

    def display_matches(self, match_results):
        while self.results_layout.count():
            child = self.results_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for match in match_results:
            widget = create_match_widget(match["path"], match["score"])
            self.results_layout.addWidget(widget)
