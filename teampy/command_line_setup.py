import teampy
import os
from colorama import init, Fore

import click

def print_teampy():
    print(' _                                   ')
    print('| |_ ___  __ _ _ __ ___  _ __  _   _ ')
    print('| __/ _ \/ _` | \'_ ` _ \| \'_ \| | | |')
    print('| ||  __/ (_| | | | | | | |_) | |_| |')
    print(' \__\___|\__,_|_| |_| |_| .__/ \__, |')
    print('                        |_|    |___/ ')

@click.group()
@click.version_option(teampy.__version__)
def teampy():
    """
    Teampy is a collection of tools for team-based learning.
    """
    pass

@teampy.command()
def setup():
    """
    Create default setup for a course.
    """
    click.echo('Setup a new course.')

if __name__ == "__main__":
    rat()
