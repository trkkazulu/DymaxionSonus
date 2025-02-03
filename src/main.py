from gui.main_window import MainWindow
from modules.test_module import TestModule
from PyQt6.QtWidgets import QApplication
import sys

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    
    # Add a test module
    test_module = TestModule()
    window.add_module(test_module)
    
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 