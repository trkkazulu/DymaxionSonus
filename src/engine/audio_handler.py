import soundfile as sf
import sounddevice as sd
import numpy as np
from PyQt6.QtCore import QTimer

class AudioHandler:
    def __init__(self):
        self.audio_data = None
        self.sample_rate = None
        self.file_path = None
        self.current_frame = 0
        self.is_playing = False
        self.stream = None
        self.blocksize = 2048
        self.channels = None
        self.dtype = None
        
    def load_file(self, file_path):
        """Load an audio file and store its data"""
        try:
            # Clean up any existing playback
            self.stop()
            
            # Load new file and store info
            self.audio_data, self.sample_rate = sf.read(file_path)
            self.file_path = file_path
            self.dtype = self.audio_data.dtype
            self.channels = self.audio_data.shape[1] if len(self.audio_data.shape) > 1 else 1
            
            # Convert to mono if stereo
            if self.channels > 1:
                self.audio_data = np.mean(self.audio_data, axis=1)
            
            # Convert to float32 and normalize
            self.audio_data = self.audio_data.astype(np.float32)
            # Normalize if not already in [-1, 1] range
            max_val = np.max(np.abs(self.audio_data))
            if max_val > 1.0:
                self.audio_data = self.audio_data / max_val
                
            self.current_frame = 0
            return True
        except Exception as e:
            print(f"Error loading audio file: {e}")
            self.audio_data = None
            self.sample_rate = None
            self.file_path = None
            self.channels = None
            self.dtype = None
            return False
            
    def get_duration(self):
        """Get duration in seconds"""
        if self.audio_data is not None and self.sample_rate is not None:
            return len(self.audio_data) / self.sample_rate
        return 0
        
    def get_channel_data(self):
        """Return audio data for visualization"""
        return self.audio_data if self.audio_data is not None else np.array([])
    
    def play(self, callback=None):
        """Start audio playback"""
        if self.audio_data is None or self.is_playing:
            return
            
        # Close any existing stream
        if self.stream is not None:
            self.stream.close()
            self.stream = None
            
        def callback_wrapper(outdata, frames, time, status):
            if status:
                print(status)
            
            if self.current_frame + frames > len(self.audio_data):
                # End of file reached
                remaining = len(self.audio_data) - self.current_frame
                outdata[:remaining, 0] = self.audio_data[self.current_frame:len(self.audio_data)]
                outdata[remaining:, 0] = 0
                raise sd.CallbackStop()
            else:
                outdata[:, 0] = self.audio_data[self.current_frame:self.current_frame + frames]
                self.current_frame += frames
                if callback:
                    callback(self.current_frame)
        
        try:
            # Configure stream with larger buffer size and proper sample rate
            self.stream = sd.OutputStream(
                channels=1,
                samplerate=self.sample_rate,
                callback=callback_wrapper,
                blocksize=self.blocksize,
                dtype=np.float32
            )
            self.stream.start()
            self.is_playing = True
        except Exception as e:
            print(f"Error starting playback: {e}")
            self.is_playing = False
            if self.stream:
                self.stream.close()
                self.stream = None
    
    def stop(self):
        """Stop audio playback"""
        self.is_playing = False
        if self.stream:
            try:
                self.stream.stop()
                self.stream.close()
            except Exception as e:
                print(f"Error stopping stream: {e}")
            self.stream = None
        self.current_frame = 0
    
    def pause(self):
        """Pause audio playback"""
        self.is_playing = False
        if self.stream:
            try:
                self.stream.stop()
                self.stream.close()
            except Exception as e:
                print(f"Error pausing stream: {e}")
            self.stream = None
    
    def get_playback_position(self):
        """Get current playback position in seconds"""
        if self.sample_rate:
            return self.current_frame / self.sample_rate
        return 0
        
    def __del__(self):
        """Cleanup when object is destroyed"""
        self.stop() 