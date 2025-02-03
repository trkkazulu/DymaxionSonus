from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QFileDialog)
from .widgets.module_panel import ModulePanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cecilia Clone")
        self.setGeometry(100, 100, 1024, 768)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        
        # Create toolbar with basic controls
        toolbar = QHBoxLayout()
        main_layout.addLayout(toolbar)
        
        # Add buttons
        self.play_button = QPushButton("Play")
        self.stop_button = QPushButton("Stop")
        self.load_button = QPushButton("Load File")
        
        toolbar.addWidget(self.play_button)
        toolbar.addWidget(self.stop_button)
        toolbar.addWidget(self.load_button)
        toolbar.addStretch()
        
        # Connect button signals
        self.play_button.clicked.connect(self.play)
        self.stop_button.clicked.connect(self.stop)
        self.load_button.clicked.connect(self.load_file)
        
        # Create area for module panels
        self.modules_layout = QVBoxLayout()
        main_layout.addLayout(self.modules_layout)
        
        # Add stretch to push everything up
        main_layout.addStretch()
        
    def add_module(self, module):
        """Add a new module to the interface"""
        panel = ModulePanel(module)
        self.modules_layout.addWidget(panel)
        
    def play(self):
        """Start audio processing"""
        print("Play clicked")  # Placeholder
        
    def stop(self):
        """Stop audio processing"""
        print("Stop clicked")  # Placeholder
        
    def load_file(self):
        """Open file dialog to load audio file"""
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open Audio File",
            "",
            "Audio Files (*.wav *.aif *.aiff);;All Files (*.*)"
        )
        if file_name:
            print(f"Loading file: {file_name}")  # Placeholder 