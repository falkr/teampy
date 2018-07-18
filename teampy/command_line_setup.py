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

def create_scratch_card_file():
    s = ('# This file contains codes for scratch cards, so that you\n'
         '# do not have to read them in every time you use them.\n'
         '# Since we do not know the solutions on your scratch cards, you\n'
         '# have to edit this file on your own.\n'
         '#\n'
         '# All lines preceeded by a #, like these, are a comments.\n'
         '#\n'
         '# This is an example for an entry for a scratch card with name "F017":\n'
         '# F017: b c b a c d a c d c\n'
         '# Simply add your own cards in the lines below, but without any # in front.\n'
         )

@teampy.command()
@click.option('--example', is_flag=True, default=False, help='add example content')
def setup(example):
    """
    Create default setup for a course.

    This command creates the file skelettons for students, teams
    and scratch cards.

    If the --example option is specified, the command also populates the files
    with some content so you can play with the tool before creating your own
    course.
    """
    click.echo('Setup a new course.')


if __name__ == "__main__":
    rat()
