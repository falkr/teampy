import os
import teampy
from teampy import Questionaire, SolutionDocument, Students, Teams, Solution, Result, Teampy, RATContext, tell
from colorama import init, Fore, Style


import click
import shutil

def print_teampy():
    print('')
    print(' _                                   ')
    print('| |_ ___  __ _ _ __ ___  _ __  _   _ ')
    print('| __/ _ \/ _` | \'_ ` _ \| \'_ \| | | |')
    print('| ||  __/ (_| | | | | | | |_) | |_| |')
    print(' \__\___|\__,_|_| |_| |_| .__/ \__, |')
    print('                        |_|    |___/ ')
    print('')

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


def _load_rat_file(file_input):
    content = file_input.readlines()
    file_input.close()
    questionaire = Questionaire()
    code, message = questionaire._parse(content)
    if code == 1: # warnig
        print(Fore.YELLOW + message + Style.RESET_ALL)
        return None
    elif code == 2: # error
        print(Fore.RED + message + Style.RESET_ALL)
        return None
    return questionaire


def write_latex(latex, file_path):
    tex_file_name = os.path.splitext(os.path.basename(file_path))[0] + '.tex'
    tex_file_path = os.path.join(os.path.dirname(file_path), tex_file_name)
    # TODO check if file already exists
    with open(tex_file_path, "w", encoding='utf-8') as file:
        file.write(latex)
    # copy also ratbox figures
    copy_figures(os.path.dirname(file_path))
    tell('Write LaTeX into file {}.'.format(tex_file_path))

def rat_check(file_input, file_path):
    """
    Read the RAT questionaire, check for consistency, print it as tex document,
    but without solutions or fo specific students or teams.
    """
    questionaire = _load_rat_file(file_input)
    if questionaire is None:
        return

    # does not detect 4 fake answers, or several true answers, improve parser
    tell('The RAT has {} questions.'.format(len(questionaire.questions)))
    for question in questionaire.questions:
        fake = len(question.fake)
        if fake != 3:
            print(Fore.RED + 'Question {} has only {} fake answers. Must be 3.'.format(question.number, fake) + Style.RESET_ALL)
            return
        if question.true is None:
            print(Fore.RED + 'Question {} has no true answer. The first answer alternative must be the true one.'.format(question.number) + Style.RESET_ALL)
            return
    tell('The rat looks okay.')
    latex = questionaire.write_latex()
    write_latex(latex, file_path)

def parallel_file_path(file_path, alternative_extension):
    head, tail = os.path.split(file_path)
    tail_base = tail.split('.')[0]
    return os.path.join(os.path.dirname(file_path), '{}.{}'.format(tail_base, alternative_extension))

def rat_print(file_input, file_path, team_solution):
    """
    Create a document with RATs for all students and all teams.
    """
    t = Teampy()
    questionaire = _load_rat_file(file_input)
    if questionaire is None:
        return

    if team_solution in t.scratchcards:
        scratch_card_id = team_solution
        team_solution = t.scratchcards[team_solution]
        # TODO check if solution matches requirement from questionaire
        tell('Found scratch card {} with solution {}'.format(scratch_card_id, team_solution.to_string()))
    else:
        # TODO check if solution matches requirement from questionaire
        team_solution = Solution.create_solution_from_string(team_solution)

    # TODO check if team solution has correct number
    # TODO look for already existing solution document, load and update it

    # create a solution file
    sd = SolutionDocument()
    sd.create_solution_document(t.teams, t.students, questionaire, team_solution)
    solutions_file_path = parallel_file_path(file_path, 'solutions')
    sd.store(solutions_file_path)
    tell('Write solutions into file {}.'.format(solutions_file_path))

    latex = questionaire.write_latex(sd, t.teams, t.students)
    write_latex(latex, file_path)

    tell('Done! ')
    print('   As a next step, print the LaTeX document and do the RAT.')


def rat_grade(file_input, file_path):
    """
    Evaluate the results of a RAT.
    """
    teampy = Teampy()
    rat = RATContext(teampy)

    # read in the questionaire
    questionaire = _load_rat_file(click.open_file(rat.questionaire_file, encoding='latin-1'))
    if questionaire is None:
        tell('Could not read questions. Aborting.', 'error')
        return
    # read in the solutions file
    solutions = SolutionDocument()
    solutions.load(rat.solutions_file, teampy.students, teampy.teams)

    result = Result(teampy.students, teampy.teams, questionaire, solutions)
    result.load_results(file_input)

    results_file_path = parallel_file_path(file_path, 'xlsx')
    result.store_results(results_file_path)
    result.stats()

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
    print_teampy()
    click.echo('Create a new RAT.')
    # store as ISO-Latin-1
    # ask for a title
    # ask for number of questions
    # ask for answer alternatives

    #

    # example question?

    # a complete example document?

@rat.command()
#@click.argument('file', type=click.File('r'))
@click.argument('file', type=click.Path(exists=True))
def check(file):
    """
    Check a RAT file for consistency before printing.
    """
    print_teampy()
    rat_check(click.open_file(file, encoding='latin-1'), file)

@rat.command(name='print')
#@click.argument('file', type=click.File('r'))
@click.argument('file', type=click.Path(exists=True))
@click.option('--teamsolution', prompt='Team solution', help='Code of the team scratch card or team solution.')
def print_(file, teamsolution):
    """
    Print a RAT before class.
    """
    # TODO if no valid team solution code is shown, add prompt that also shows which scratch cards are available
    print_teampy()
    rat_print(click.open_file(file, encoding='latin-1'), file, teamsolution)

@rat.command()
@click.argument('file', type=click.Path(exists=True))
def grade(file):
    """
    Evaluate a RAT during class.
    """
    print_teampy()
    rat_grade(click.open_file(file, encoding='latin-1'), file)

if __name__ == "__main__":
    rat()
