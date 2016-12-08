from module import ModuleObject
import os
import re

class ShellcodeModule(ModuleObject):
    
    def __init__(self, ui):
        ModuleObject.__init__(self)
        self.ui = ui
        self.vars = {}
        self.vars["source"] = ["", "Path to the raw shellcode file"]
        self.description = "Module to generate shellcode out of raw metasploit shellcode file"
        self.module_name = "shellcode"
    
    def run_action(self):
        if os.path.exists(self.vars["source"][0]):
            self.ui.print_msg("Shellcode:")
            print "\\x" + "\\x".join(re.findall("..", open(self.vars["source"][0], "rb").read().encode("hex")))
        else:
            self.ui.print_error("%s not found" % self.vars["source"][0])