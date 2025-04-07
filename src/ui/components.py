from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget


def create_match_widget(image_path, score):
    image_label = QLabel()
    pixmap = QPixmap(image_path).scaledToWidth(320, Qt.SmoothTransformation)
    image_label.setPixmap(pixmap)
    image_label.setAlignment(Qt.AlignCenter)

    score_label = QLabel(f"Score: {score:.2f}")
    score_label.setAlignment(Qt.AlignCenter)

    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignTop)
    layout.addWidget(image_label)
    layout.addWidget(score_label)

    container = QWidget()
    container.setLayout(layout)
    container.setFixedSize(320, 900)
    return container
