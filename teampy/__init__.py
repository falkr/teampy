"""Module `teampy` provides support to manage readiness assurance tests (rats)
in Python.

## Contributing

`teampy` [is on GitHub](https://github.com/falkr/teams). Pull
requests and bug reports are welcome.


"""
from os.path import dirname
from colorama import init, Fore
from teampy.core import (
    SolutionDocument,
    Students,
    Teams,
    Solution,
    Result,
    Questionaire,
    Teampy,
    RATContext,
    tell,
)

init(autoreset=True)

__version__ = "0.1.31"
"""
The current version.
"""
