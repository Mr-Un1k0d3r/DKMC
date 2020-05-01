import os
from core.ui import UI
from core.menu import MenuUI
from module.gen import GenModule
from module.web import WebModule
from module.ps import PsModule
from module.shellcode import ShellcodeModule

if __name__ == "__main__":

    if not os.path.exists("output/"):
        os.makedirs("output/")

    options = []
    options.append(("gen", "Generate a malicious BMP image"))
    options.append(("web", "Start a web server and deliver malicious image"))
    options.append(("ps", "Generate Powershell payload"))
    options.append(("sc", "Generate shellcode from raw file"))
    options.append(("exit", "Quit the application"))
    
    exit_loop = False
    error = ""
    ui = UI()
    menu = MenuUI()
    
    while not exit_loop:
        try:
	        ui.banner()
        	choice = ui.show_menu(options, error)
	        error = ""
        	if menu.is_an_option(choice):
	            mod = None
        	    if choice == "exit":
                	exit(0)
	            if choice == "gen":
        	        mod = GenModule(ui)
	            if choice == "web":
        	        mod = WebModule(ui)
	            if choice == "ps":
        	        mod = PsModule(ui)
	            if choice == "sc":
        	        mod = ShellcodeModule(ui)
                    mod.show_menu()
        	else:
            		error = "%s is not a valid option" % choice
	except KeyboardInterrupt:
		print ""
		ui.print_error("Exiting")
		exit(0)
