class BaseModule:
    def __init__(self):
        self.name = "Base Module"
        self.parameters = {}
        
    def get_csound_code(self):
        """Return the Csound orchestra code for this module"""
        raise NotImplementedError
        
    def update_parameter(self, param_name, value):
        """Update a module parameter"""
        if param_name in self.parameters:
            self.parameters[param_name] = value 