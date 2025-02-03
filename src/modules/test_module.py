from .base_module import BaseModule

class TestModule(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "Test Module"
        self.parameters = {
            "frequency": {
                "min": 20,
                "max": 2000,
                "default": 440
            },
            "amplitude": {
                "min": 0,
                "max": 1,
                "default": 0.5
            }
        }
        
    def get_csound_code(self):
        return """
        a1 oscili {amplitude}, {frequency}
        out a1
        """ 