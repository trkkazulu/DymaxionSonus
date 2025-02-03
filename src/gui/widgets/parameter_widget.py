from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider
from PyQt6.QtCore import Qt, pyqtSignal

class ParameterWidget(QWidget):
    valueChanged = pyqtSignal(str, float)  # Emits (parameter_name, value)
    
    def __init__(self, name, min_val=0, max_val=1, default=0.5, parent=None):
        super().__init__(parent)
        self.name = name
        self.min_val = min_val
        self.max_val = max_val
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Label showing parameter name and current value
        self.value_label = QLabel(f"{name}: {default:.2f}")
        layout.addWidget(self.value_label)
        
        # Slider for parameter control
        self.slider = QSlider(Qt.Orientation.Vertical)
        self.slider.setMinimum(0)
        self.slider.setMaximum(1000)  # For finer control
        self.slider.setValue(int(1000 * (default - min_val) / (max_val - min_val)))
        self.slider.valueChanged.connect(self._on_slider_changed)
        layout.addWidget(self.slider)
        
    def _on_slider_changed(self, value):
        # Convert slider value (0-1000) to parameter range
        normalized = value / 1000.0
        actual_value = self.min_val + normalized * (self.max_val - self.min_val)
        self.value_label.setText(f"{self.name}: {actual_value:.2f}")
        self.valueChanged.emit(self.name, actual_value) 