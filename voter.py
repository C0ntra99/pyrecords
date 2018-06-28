import glob

class train:

    def __init__(self, cli):

        self.imported_modules = {}
        self.load_modules(cli)
        self.mainmenu_commands = {
        "list": "List available modules",
        "set": "Set a specific variable",
        "use": "Use a module"
        "options": "Show options",
        "exit": "Exit the program",
        "clear": "Clear the screen"
        }
        self.command_line_options = cli

    ##For command line use
    def list_modules(self):
        print("[*]Modules")
        tool_counter = 1
        for key, mod in sorted(self.imported_modules.items()):
            print('\t' + str(tool_counter) + ')\t' + tool.cli_name)
            tool_counter += 1
        print()
        return

    ##For UI use
    def load_modules(self, command):
        for mod in glob.glob('modules/*.py'):
            loaded_mod = imp.load_source(mod.replace('/','.').rstrip('.py'), name)
            self.imported_modules[mod] = loaded_mod.Tools(command)
        return

    def main_menu(self):
        main_command = ""
        show_header = True

        try:

            while True:

                if show_header:
