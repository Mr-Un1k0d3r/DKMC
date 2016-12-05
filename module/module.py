class ModuleObject:
    
    def __init__(self):
        self.allowed = []
        self.allowed.append(("show", "Show module variables"))
        self.allowed.append(("set", "Set value (set key value)"))
        self.allowed.append(("run", "Run the module"))
        self.allowed.append(("exit", "Go back to the main menu"))
        
    def show_menu(self):
        self.ui.clearscreen()
        line = "=" * (len(self.description) + 4)
        emptyline = "|" + " " * (len(self.description) + 2) + "|\n"
        print "\n\n\033[33m" + line + "\n" + emptyline + "| " + self.description + " |\n" + emptyline + line + "\033[00m\n\n"
        print "Allowed options:\n"
        self.show_allowed()
        print "\nModule Variables description:\n"
        self.show_description()
        print "\n\nCurrent variable value:\n"
        self.show_vars()
        self.do_action()
        
    def show_allowed(self):
        for cmd in self.allowed:
            print "\t[*] (%s)\t%s" % cmd
        
    def show_description(self):
        for key in self.vars.keys():
            print "\t" + key + " " * (12 - len(key)) + self.vars[key][1]        
        
    def show_vars(self):
        for key in self.vars.keys():
            print "\t" + key + " " * (12 - len(key)) + "= " + self.vars[key][0] 
            
    def do_action(self):
        exit_module = False
        while not exit_module:
            data = self.ui.capture_input(self.module_name)
            if data == "exit":
                exit_module = True
            if self.is_an_action(data.split(" ", 1)[0]):
                self.exec_action(data)
            else:
                self.ui.print_error("%s is not a valid action." % data)
        
    def is_an_action(self, data):
        for action in self.allowed:
            if data == action[0]:
                return True
        return False
    
    def exec_action(self, data):
        action = data.split(" ", 1)[0]
        if action == "set":
            self.set_action(data)
        if action == "run":
            self.run_action()
        if action == "show":
            self.show_vars()
            
    def set_action(self, data):
        try:
            null, key, value = data.split(" ", 2)
        except:
            self.ui.print_error("invalid 'set' parameter.")
            return 
        if self.vars.has_key(key):
            self.ui.print_msg("%s value is set." % key)
            self.vars[key][0] = value
        else:
            self.ui.print_error("%s is not a valid variable." % key)