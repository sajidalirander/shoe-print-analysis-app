# src/ui/components.py

from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

def create_match_widget(image_path, score):
    image_label = QLabel()
    pixmap = QPixmap(image_path).scaledToWidth(200, Qt.SmoothTransformation)
    image_label.setPixmap(pixmap)
    image_label.setAlignment(Qt.AlignCenter)

    score_label = QLabel(f"Score: {score:.2f}")
    score_label.setAlignment(Qt.AlignCenter)

    layout = QVBoxLayout()
    layout.addWidget(image_label)
    layout.addWidget(score_label)

    container = QWidget()
    container.setLayout(layout)
    return container
