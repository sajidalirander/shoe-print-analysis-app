from api.backend_client import get_probe_files
from PyQt5.QtWidgets import QDialog, QListWidget, QVBoxLayout, QListWidgetItem


class ImageSelectorDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Probe Image")
        self.selected_image = None

        layout = QVBoxLayout()
        self.list_widget = QListWidget()

        for file in get_probe_files():
            item = QListWidgetItem(file)
            self.list_widget.addItem(item)

        self.list_widget.itemClicked.connect(self.select_image)
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

    def select_image(self, item):
        self.selected_image = item.text()
        self.accept()
