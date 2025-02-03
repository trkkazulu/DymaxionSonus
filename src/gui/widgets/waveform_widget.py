from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class WaveformWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.playhead = None
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Create matplotlib figure
        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        # Add subplot for waveform
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Amplitude')
        self.ax.grid(True)
        
    def plot_waveform(self, audio_data, sample_rate):
        """Plot the waveform of the loaded audio file"""
        self.ax.clear()
        if len(audio_data) > 0:
            time = np.arange(len(audio_data)) / sample_rate
            self.ax.plot(time, audio_data, 'b-', linewidth=0.5)
            self.ax.set_xlim(0, len(audio_data) / sample_rate)
            self.ax.set_ylim(-1, 1)
            
            # Initialize playhead
            self.playhead = self.ax.axvline(x=0, color='r', linewidth=1)
        self.ax.grid(True)
        self.canvas.draw()
        
    def update_playhead(self, position):
        """Update playhead position"""
        if self.playhead:
            self.playhead.set_xdata([position, position])
            self.canvas.draw_idle()  # More efficient than full draw() 