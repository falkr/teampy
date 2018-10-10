import os
import teampy
import pandas as pd
from teampy import Questionaire, SolutionDocument, Students, Teams, Solution, Result, Teampy, RATContext, tell
from colorama import init, Fore, Style
import click
import shutil
import time

# sending email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from smtplib import SMTPHeloError, SMTPRecipientsRefused, SMTPNotSupportedError, SMTPAuthenticationError, SMTPSenderRefused, SMTPDataError, SMTPException
import getpass
import progressbar

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

    # TODO does not detect 4 fake answers, or several true answers, improve parser
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
    solutions_file_path = os.path.join(os.path.dirname(file_path), 'solutions.teampy')
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
    results_file_path = parallel_file_path(file_path, 'html')
    result.store_results_html(results_file_path)
    result.stats()

def create_message(student_id, row, result, teampy):
    msg = MIMEMultipart()
    msg['From'] = teampy.smtp_settings['from']
    msg['To'] = row['email']
    # TODO here the course code would be nice to have
    msg['Subject'] = 'RAT Feedback'
    html = """\
<html>
  <head></head>
  <body>
    <p>Hi {}!</p>
    <p>Here are the results form the latest RAT:</p>
    <table>
      <tr><td>Name:</td><td>{} {}</td><tr>
      <tr><td>ID:</td><td><code>{}</code></td><tr>
      <tr><td>Team:</td><td><code>{}</code></td><tr>
      <tr><td>RAT:</td><td><code>{}</code></td><tr>
      <tr><td>Date:</td><td><code>{}</code></td><tr>
""".format(row['firstname'], row['firstname'], row['lastname'], student_id, row['team'], result.name, result.date)
    html = html + """\
      <tr><td>Individual Answer:&nbsp;</td><td><code>{}</code></td><tr>
      <tr><td>Correct Solution:</td><td><code>{}</code></td><tr>
      <tr><td>Individual Score:</td><td><code>{}</code> &nbsp; <emph>(counts {}%)</emph></td><tr>
""".format(row['answer_i'], row['correct_i'], row['irat'], row['pi'])
    if row['trat'] is not None: # TODO check what a non-value in Excel looks like here
        html = html + """\
      <tr><td>Team Answer:</td><td><code>{}</code></td><tr>
      <tr><td>Correct Solution:</td><td><code>{}</code></td><tr>
      <tr><td>Team Score:</td><td><code>{}</code> &nbsp; <emph>(counts {}%)</emph></td><tr>
""".format(row['answer_t'], row['correct_t'], row['trat'], row['pt'])
    html = html + """\
      <tr><td>Final Score for this RAT:</td><td><b>{}</b></td><tr>
    </table>
    <p>This mail was automated, but you can reply to it.</p>
  </body>
</html>
""".format(row['score'])
    msg.attach(MIMEText(html, 'html'))
    return msg    


def rat_email(file_input, file_path):
    """
    Send the results of a RAT to students via email.
    """
    teampy = Teampy()
    
    if teampy.smtp_settings is None:
        tell('Your SMTP settings are not complete. Please check.', 'error')
        return
    
    # TODO give RAT context the directory relative to the file_input
    rat = RATContext(teampy)
    # read in the questionaire
    questionaire = _load_rat_file(click.open_file(rat.questionaire_file, encoding='latin-1'))
    if questionaire is None:
        tell('Could not read questions. Aborting.', 'error')
        return
    # read in the solutions file
    solutions = SolutionDocument()
    solutions.load(rat.solutions_file, teampy.students, teampy.teams)

    # read in the corresponding result file
    results_file_path = parallel_file_path(file_path, 'txt')
    result = Result(teampy.students, teampy.teams, questionaire, solutions)
    result.load_results(click.open_file(results_file_path, encoding='latin-1'))

    # read in the graded file
    df = pd.read_excel(file_path, dtype={'id': str, 'team': str, 'email':str, 'comment':str, 'feedback':str})
    df = df.set_index('id')

    # TODO check that table is consistent
    # TODO abort if there is nothing to send
    # TODO check if all email adresses are valid

    # create all messages first
    messages = {}
    for student_id, row in df.iterrows():
        # TODO check if we need to send email to this student
        if row['feedback'] != 'sent':
            messages[student_id] = create_message(student_id, row, result, teampy)
    if len(messages)==0:
        tell('There is nothing to send.')
        return
    else:
        tell('Will send messages to {} students.'.format(len(messages)))

    # connect to SMTP server
    print('\n')
    password = getpass.getpass(prompt='Password for the user {} on server {}: '.format(teampy.smtp_settings['from'], teampy.smtp_settings['smtp']))

    #create server
    server = smtplib.SMTP('{}: {}'.format(teampy.smtp_settings['smtp'], teampy.smtp_settings['port']))
    statuses = {}
    try:
        server.starttls()
        # Login Credentials for sending the mail
        server.login(teampy.smtp_settings['from'], password)

        # send email
        bar = progressbar.ProgressBar(max_value=len(messages), widgets=[progressbar.Percentage(), progressbar.Bar()])
        for student_id, message in messages.items():
            try:
                server.send_message(message)
                time.sleep(0.1)
                statuses[student_id] = 'sent'
            except (SMTPHeloError, SMTPRecipientsRefused, SMTPNotSupportedError, SMTPSenderRefused, SMTPDataError) as e:
                tell('There was an error sending a mail to {}.'.format(student_id))
                statuses[student_id] = 'error'
                print(e)
            bar += 1
    except (SMTPHeloError, SMTPAuthenticationError, SMTPNotSupportedError, SMTPException) as e:
        tell('There was an error connecting to the SMTP server {}'.format(teampy.smtp_settings['smtp']))
    bar.finish()
    server.quit()

    # update the status
    changes = False
    for student_id, status in statuses.items():
        df.at[student_id, 'feedback'] = status
        changes = True
    if changes:
        keep_trying = True
        while keep_trying:
            try:
                df.to_excel(file_path)
                tell('Updated results file with email send status.')
                keep_trying = False
            except PermissionError:
                tell('Can\'t write file {}. Maybe Excel is open? Close it and press enter.'.format(file_path), 'error')
                input("")



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
@click.argument('file', type=click.Path(exists=True))
def check(file):
    """
    Check a RAT file for consistency before printing.
    """
    print_teampy()
    rat_check(click.open_file(file, encoding='latin-1'), file)

@rat.command()
@click.argument('file', type=click.Path(exists=True))
def trial(file):
    """
    Print the RAT for a trial run, for instance with a colleague.
    Question sequence is original, but answers are shuffled.
    """
    print_teampy()
    file_path = file
    file = click.open_file(file, encoding='latin-1')
    questionaire = _load_rat_file(file)
    if questionaire is None:
        return
    latex = questionaire.write_trial_latex()
    write_latex(latex, file_path)

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

@rat.command()
@click.argument('file', type=click.Path(exists=True))
def email(file):
    """
    Send feedback to students via email.
    """
    print_teampy()
    rat_email(click.open_file(file, encoding='latin-1'), file)

if __name__ == "__main__":
    rat()
