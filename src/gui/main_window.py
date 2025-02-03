from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QFileDialog)
from PyQt6.QtCore import QTimer
from .widgets.module_panel import ModulePanel
from .widgets.waveform_widget import WaveformWidget
from engine.audio_handler import AudioHandler
from .widgets.file_info_widget import FileInfoWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DymaxionSonus")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize audio handler
        self.audio_handler = AudioHandler()
        
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
        self.pause_button = QPushButton("Pause")
        self.load_button = QPushButton("Load File")
        
        toolbar.addWidget(self.play_button)
        toolbar.addWidget(self.stop_button)
        toolbar.addWidget(self.pause_button)
        toolbar.addWidget(self.load_button)
        toolbar.addStretch()
        
        # Add file info widget
        self.file_info = FileInfoWidget()
        main_layout.addWidget(self.file_info)
        
        # Add waveform widget
        self.waveform = WaveformWidget()
        main_layout.addWidget(self.waveform)
        
        # Create area for module panels
        self.modules_layout = QVBoxLayout()
        main_layout.addLayout(self.modules_layout)
        
        # Connect button signals
        self.play_button.clicked.connect(self.play)
        self.stop_button.clicked.connect(self.stop)
        self.load_button.clicked.connect(self.load_file)
        self.pause_button.clicked.connect(self.pause)
        
        # Create timer for updating playhead (reduced update frequency)
        self.update_timer = QTimer()
        self.update_timer.setInterval(100)  # 100ms update interval
        self.update_timer.timeout.connect(self.update_playhead)
        
        # Add stretch to push everything up
        main_layout.addStretch()
        
    def add_module(self, module):
        """Add a new module to the interface"""
        panel = ModulePanel(module)
        self.modules_layout.addWidget(panel)
        
    def load_file(self):
        """Open file dialog to load audio file"""
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open Audio File",
            "",
            "Audio Files (*.wav *.aif *.aiff);;All Files (*.*)"
        )
        if file_name and self.audio_handler.load_file(file_name):
            self.waveform.plot_waveform(
                self.audio_handler.get_channel_data(),
                self.audio_handler.sample_rate
            )
            # Update file info display
            self.file_info.update_info(
                self.audio_handler.file_path,
                self.audio_handler.sample_rate,
                self.audio_handler.dtype,
                self.audio_handler.channels
            )
            
    def play(self):
        """Start audio playback"""
        if self.audio_handler.audio_data is not None:
            self.audio_handler.play(callback=None)  # We'll handle updates via timer
            self.update_timer.start()
            
    def stop(self):
        """Stop audio playback"""
        self.audio_handler.stop()
        self.update_timer.stop()
        self.waveform.update_playhead(0)
        
    def pause(self):
        """Pause audio playback"""
        self.audio_handler.pause()
        self.update_timer.stop()
        
    def update_playhead(self):
        """Update the playhead position"""
        if self.audio_handler.is_playing:
            position = self.audio_handler.get_playback_position()
            self.waveform.update_playhead(position) 