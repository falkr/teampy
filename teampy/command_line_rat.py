import teampy
import os
from teampy import Questionaire, SolutionDocument, Students, Teams, Solution
from colorama import init, Fore, Style

import click
import shutil

def print_teampy():
    print(' _                                   ')
    print('| |_ ___  __ _ _ __ ___  _ __  _   _ ')
    print('| __/ _ \/ _` | \'_ ` _ \| \'_ \| | | |')
    print('| ||  __/ (_| | | | | | | |_) | |_| |')
    print(' \__\___|\__,_|_| |_| |_| .__/ \__, |')
    print('                        |_|    |___/ ')

def copy_figures(rat_directory):
    # create the figures directory
    figures = os.path.join(rat_directory, 'figures')
    if not os.path.exists(figures):
        os.makedirs(figures)
    for filename in ['rat-box.pdf', 'scratch.pdf']:
        file = os.path.join(os.path.dirname(__file__), filename)
        shutil.copy(file, figures)

def rat_create():
    """
    Create a template file for a RAT
    """
    print_formatted_text(HTML('<darkgray>Create a new template file for a RAT.</darkgray>'))

    from prompt_toolkit.shortcuts import input_dialog

    text = input_dialog(
    title='Input dialog example',
    text='Please type your name:')

    # create directory
    #number = int(prompt('Number of the RAT: ', validator=NumberValidator(), key_bindings=bindings))
    number = prompt('Number of the RAT: ', validator=NumberValidator(), key_bindings=bindings)
    title = prompt(' Title of the RAT: ')
    rat_id = 'rat-' + str(number).zfill(2)
    # create template file
    directory = os.path.join(os.getcwd(), rat_id)
    if not os.path.exists(directory):
        os.makedirs(directory)
    file = os.path.join(directory, 'questions.md')

def rat_check(file_input, file_path):
    """
    Read the RAT questionaire, check for consistency, print it as tex document,
    but without solutions or fo specific students or teams.
    """
    content = file_input.readlines()
    file_input.close()
    questionaire = Questionaire()
    code, message = questionaire._parse(content)
    if code == 1: # warnig
        print(Fore.YELLOW + message + Style.RESET_ALL)
        return
    elif code == 2: # error
        print(Fore.RED + message + Style.RESET_ALL)
        return

    # does not detect 4 fake answers, or several true answers, improve parser
    print('The RAT has {} questions.'.format(len(questionaire.questions)))
    for question in questionaire.questions:
        fake = len(question.fake)
        if fake != 3:
            print(Fore.RED + 'Question {} has only {} fake answers. Must be 3.'.format(question.number, fake) + Style.RESET_ALL)
            return
        if question.true is None:
            print(Fore.RED + 'Question {} has no true answer. The first answer alternative must be the true one.'.format(question.number) + Style.RESET_ALL)
            return
    print(Fore.GREEN + 'OK' + Style.RESET_ALL)

    tex_file_name = os.path.splitext(os.path.basename(file_path))[0] + '.tex'
    tex_file_path = os.path.join(os.path.dirname(file_path), tex_file_name)
    # TODO check if file already exists
    with open(tex_file_path, "w") as file:
        file.write(questionaire.write_latex())
    # copy also ratbox figures
    copy_figures(os.path.dirname(file_path))


def rat_print(rat):
    """
    Create a document with RATs for all students and all teams.
    """
    # load the student file
    students = load_students()
    teams = load_teams()

    # find out which RAT to print
    #current working directory
    cwd = os.getcwd()
    print(cwd)
    from os.path import isfile, join
    for item in os.listdir(cwd):
        if isfile(join(cwd, item)):
            print(item)
    # read in Questionaire
    questionaire = Questionaire.read_questionaire('../tests/data/rat-01.md')
    for q in questionaire.questions:
        print(q)

    # create a solution file
    sd = SolutionDocument()
    sd.create_solution_document(teams, students, questionaire, '1c 2b 3c 4c 5b 6a 7a 8d 9a 10b')
    sd.store('solution.xlsx')

    latex = questionaire.write_latex(sd, teams, students)
    with open("questionaire.tex", "w") as text_file:
        text_file.write(latex)

@click.group()
@click.version_option(teampy.__version__)
def rat():
    """
    Teampy is a collection of tools for team-based learning.

    The rat command is used to create, print, evaluate and give feedback on
    readiness assurance tests.

    """
    pass

#@teampy.command(help='Handle quizzes.')
#@click.option('--new', 'operation', flag_value='new', default=True, help='Create a new quiz.')
#@click.option('--check', 'operation', flag_value='check', help='Check an existing quiz.')
@rat.command()
def new():
    """
    Create templates for a new RAT.
    """
    click.echo('Create a new RAT.')

@rat.command()
#@click.argument('file', type=click.File('r'))
@click.argument('file', type=click.Path(exists=True))
def check(file):
    """
    Check a RAT file for consistency before printing.
    """
    print(type(file))
    print(file)

    cwd = os.getcwd()
    print(cwd)
    from os.path import isfile, join
    j = join(cwd, file)
    abs = os.path.abspath(j)
    dir = os.path.dirname(abs)
    print(dir)
    print(isfile(j))
    print(type(j))
    rat_check(click.open_file(file), abs)

@rat.command(name='print')
@click.argument('file', type=click.File('r'))
def print_(file):
    """
    Print a RAT before class.
    """
    click.echo('Print the rat')
    print(type(file))

@rat.command()
def eval():
    """
    Evaluate a RAT during class.
    """
    click.echo('Evaluate a RAT.')

if __name__ == "__main__":
    rat()
