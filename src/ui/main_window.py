import os

from ui.components import create_match_widget
from api.backend_client import get_match_results
from ui.image_selector import ImageSelectorDialog

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSplitter


# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.getcwd()
RAW_DIR = os.path.join(BASE_DIR, "database", "raw_normalized")

class ShoeprintMatcherApp(QWidget):
    def __init__(self, screen_geometry):
        super().__init__()
        self.screen_geometry = screen_geometry
        self.setWindowTitle("Shoeprint Matcher")
        self.resize(232*9, 1000)
        self.move(self.screen_geometry.left(), self.screen_geometry.top())

        splitter = QSplitter(Qt.Orientation.Horizontal, self)

        splitter.setSizes([232, 232*5])
        
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        
        button = QPushButton("Select Probe Image")
        button.setFixedSize(320, 40)
        button.clicked.connect(self.open_image_dialog)
        
        self.image_label = QLabel("Selected probe image will appear here")
        self.image_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(320, 900)
        self.image_label.setStyleSheet("border: 1px solid gray;")

        left_layout.addWidget(button)
        left_layout.addWidget(self.image_label)
        left_widget.setLayout(left_layout)
        
        
        right_widget = QWidget()
        
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignTop)
        right_layout.setContentsMargins(0, 60, 0, 0)
        
        title_label = QLabel("Top 5 Matches")
        title_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        right_layout.addWidget(title_label)
        
        self.results_layout = QHBoxLayout()
        # self.results_layout.setContentsMargins(0, 50, 0, 0)  # (left, top, right, bottom)
        self.results_layout.setAlignment(Qt.AlignLeft)
        right_layout.addLayout(self.results_layout)
        
        right_widget.setLayout(right_layout)
        
        # Add the widgets to the splitter
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)
        

    def open_image_dialog(self):
        dialog = ImageSelectorDialog()
        if dialog.exec_():
            filename = dialog.selected_image
            probe_path = os.path.join(RAW_DIR, filename)

            # Show probe image
            # pixmap = QPixmap(probe_path).scaledToWidth(300, Qt.SmoothTransformation)
            pixmap = QPixmap(probe_path)
            self.image_label.setPixmap(pixmap)
            self.image_label.setText("")
            self.image_label.setScaledContents(True)

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
