# src/app.py

import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import ShoeprintMatcherApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShoeprintMatcherApp()
    window.show()
    sys.exit(app.exec_())
