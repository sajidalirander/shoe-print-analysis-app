import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QFileDialog, QHBoxLayout, QDialog,
    QListWidget, QListWidgetItem, QGridLayout
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

ROOT = "./database"
RAW_DIR = f"{ROOT}/raw_normalized"

class ImageSelectorDialog(QDialog):
    def __init__(self, image_dir):
        super().__init__()
        self.setWindowTitle("Select Image")
        self.selected_image = None

        layout = QVBoxLayout()
        self.list_widget = QListWidget()

        for file in sorted(os.listdir(image_dir)):
            if file.endswith(".jpg"):
                item = QListWidgetItem(file)
                self.list_widget.addItem(item)

        self.list_widget.itemClicked.connect(self.select_image)
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

    def select_image(self, item):
        self.selected_image = item.text()
        self.accept()

class ShoeprintMatcherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shoeprint Matching")
        self.setGeometry(100, 100, 1000, 600)

        self.image_label = QLabel("Selected probe image will appear here")
        self.image_label.setAlignment(Qt.AlignCenter)

        self.button = QPushButton("Select Image")
        self.button.clicked.connect(self.open_image_dialog)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.image_label)

        self.setLayout(layout)

    def open_image_dialog(self):
        dialog = ImageSelectorDialog(RAW_DIR)
        if dialog.exec_():
            filename = dialog.selected_image
            full_path = os.path.join(RAW_DIR, filename)
            pixmap = QPixmap(full_path).scaledToWidth(300, Qt.SmoothTransformation)
            self.image_label.setPixmap(pixmap)
            self.image_label.setText("")  # remove placeholder text
            print(f"[INFO] Selected image: {filename}")
            # TODO: Run matching here and update results display

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShoeprintMatcherApp()
    window.show()
    sys.exit(app.exec_())
