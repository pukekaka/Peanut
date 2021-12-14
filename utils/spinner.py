# -*- coding: utf-8 -*-
from utils.notebook import is_notebook

if is_notebook():
    from halo import HaloNotebook as Halo
else:
    from halo import Halo

spinner_enable = True

if spinner_enable:
    class Spinner:
        def __init__(self, text):
            self.spinner = Halo(text=text, spinner='dots')

        def start(self):
            if spinner_enable:
                self.spinner.start()

        def stop(self):
            if spinner_enable:
                self.spinner.stop()

        def succeed(self):
            if spinner_enable:
                self.spinner.succeed()

        def fail(self):
            if spinner_enable:
                self.spinner.fail()

else:
    class Spinner:
        def __init__(self, text):
            pass

        def start(self):
            pass

        def stop(self):
            pass

        def succeed(self):
            pass

        def fail(self):
            pass
