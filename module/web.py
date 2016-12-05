from module import ModuleObject
import BaseHTTPServer
import SimpleHTTPServer
import ssl
import os

class WebModule(ModuleObject):
    
    def __init__(self, ui):
        ModuleObject.__init__(self)
        self.ui = ui
        self.vars = {}
        self.vars["folder"] = [os.getcwd() + "/output/", "Base folder used to deliver files"]
        self.vars["port"] = ["80", "Port used to bind the web server"]
        self.vars["https"] = ["false", "Use HTTPS"]
        self.vars["certificate"] = ["core/util/cert/default.pem", "Certificate path"]
        self.description = "Module to launch a web server"
        self.module_name = "web"
    
    def run_action(self):
        current_cwd = os.getcwd()
        self.ui.print_msg("Starting web server on port %s" % self.vars["port"][0])
        print "\033[33m"
        try:
            httpd = BaseHTTPServer.HTTPServer(('0.0.0.0', int(self.vars["port"][0])), SimpleHTTPServer.SimpleHTTPRequestHandler)
            if self.vars["https"][0].lower() == "true":
                httpd.socket = ssl.wrap_socket(httpd.socket, certfile=self.vars["certificate"][0], server_side=True)
            os.chdir(self.vars["folder"][0])
            httpd.serve_forever()
        except KeyboardInterrupt:
            print "\033[00m"
            self.ui.print_msg("Stopping web server")
        except:
            print "\033[00m"
            self.ui.print_error("The web server raised an exception")
            
        os.chdir(current_cwd)