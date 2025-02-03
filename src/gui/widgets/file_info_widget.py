from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt

class FileInfoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        # Create labels for file information
        self.file_type_label = QLabel("File Type: --")
        self.sample_rate_label = QLabel("Sample Rate: --")
        self.bit_depth_label = QLabel("Bit Depth: --")
        self.channels_label = QLabel("Channels: --")
        
        # Add labels to layout with some spacing
        layout.addWidget(self.file_type_label)
        layout.addSpacing(20)
        layout.addWidget(self.sample_rate_label)
        layout.addSpacing(20)
        layout.addWidget(self.bit_depth_label)
        layout.addSpacing(20)
        layout.addWidget(self.channels_label)
        layout.addStretch()
        
    def update_info(self, file_path, sample_rate, dtype, channels):
        # Get file type from extension
        file_type = file_path.split('.')[-1].upper() if file_path else "--"
        
        # Map numpy dtype to bit depth
        bit_depth_map = {
            'float32': "32-bit float",
            'float64': "64-bit float",
            'int16': "16-bit",
            'int24': "24-bit",
            'int32': "32-bit",
        }
        bit_depth = bit_depth_map.get(str(dtype), str(dtype))
        
        # Update labels
        self.file_type_label.setText(f"File Type: {file_type}")
        self.sample_rate_label.setText(f"Sample Rate: {sample_rate} Hz")
        self.bit_depth_label.setText(f"Bit Depth: {bit_depth}")
        self.channels_label.setText(f"Channels: {channels}") 