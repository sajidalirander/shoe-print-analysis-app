# src/app.py

import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import ShoeprintMatcherApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    screens = app.screens()
    screen_geometry = screens[0].geometry()
    window = ShoeprintMatcherApp(screen_geometry)
    window.show()
    sys.exit(app.exec_())
