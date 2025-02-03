import ctcsound

class CsoundHandler:
    def __init__(self):
        self.cs = ctcsound.Csound()
        
    def initialize(self):
        self.cs.setOption("-odac")  # Set output to default audio device
        self.cs.setOption("-d")     # Suppress displays
        
    def compile_orc(self, orc_string):
        return self.cs.compileOrc(orc_string)
        
    def cleanup(self):
        self.cs.cleanup()
        self.cs.reset() 