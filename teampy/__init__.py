"""Module `teampy` provides support to manage readiness assurance tests (rats)
in Python.

## Contributing

`teampy` [is on GitHub](https://github.com/falkr/teams). Pull
requests and bug reports are welcome.

## Dependencies

* pyaml
* xlrd

"""
import os
from os.path import dirname, abspath
import yaml
import random
import numpy as np
import pandas as pd

from colorama import init, Fore, Style

from teampy.core import Questionaire, SolutionDocument, Students, Teams, Solution, Result, Teampy, RATContext, tell

# colorama
#init(convert=True) # only if trouble on windows
init(autoreset=True)

#from prompt_toolkit import prompt, print_formatted_text, HTML
#from prompt_toolkit.validation import Validator, ValidationError
#from prompt_toolkit.key_binding import KeyBindings

#bindings = KeyBindings()

__version__ = '0.1.0'
"""
The current version.
"""

def print_teams():
     print('  _____ ___   _   __  __ ___ ')
     print(' |_   _| __| /_\ |  \/  / __|')
     print('   | | | _| / _ \| |\/| \__ \\')
     print('   |_| |___/_/ \_\_|  |_|___/  {}'.format(__version__))





#if __name__ == "__main__":
    #print_teams()
    #rat_create()
#    rat_print()

#    print('Current directory: {}'.format(os.getcwd()))

#    student_file = os.path.join(os.getcwd(), 'students.xlsx')
#    if not os.path.isfile(student_file):
#        print('Cannot find the file with name students.xlsx')

    #print('Current parent directory: {}'.format(dirname(os.getcwd())))

    #print(students.get_ids())

    #
    #print_formatted_text(HTML('<ansired>This is red</ansired>'))
    #print_formatted_text(HTML('<ansigreen>This is green</ansigreen>'))
