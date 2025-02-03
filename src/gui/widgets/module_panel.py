from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from .parameter_widget import ParameterWidget

class ModulePanel(QWidget):
    def __init__(self, module, parent=None):
        super().__init__(parent)
        self.module = module
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Module title
        title = QLabel(module.name)
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        # Parameters area
        params_layout = QHBoxLayout()
        layout.addLayout(params_layout)
        
        # Create parameter widgets
        self.param_widgets = {}
        for param_name, param_info in module.parameters.items():
            widget = ParameterWidget(
                name=param_name,
                min_val=param_info.get('min', 0),
                max_val=param_info.get('max', 1),
                default=param_info.get('default', 0.5)
            )
            widget.valueChanged.connect(self._on_parameter_changed)
            params_layout.addWidget(widget)
            self.param_widgets[param_name] = widget
            
        # Add a frame for visual separation
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)
        
    def _on_parameter_changed(self, param_name, value):
        self.module.update_parameter(param_name, value) 