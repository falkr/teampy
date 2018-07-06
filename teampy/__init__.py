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


class Students:
    def __init__(self, filename):
        self.df = pd.read_excel(filename)
        self.df = self.df.set_index('id')

    def get_ids(self):
        return self.df.index.values

    def get_student_ids_of_team(self, team_id):
        return self.df[self.df['team']==team_id].index.values

    def get_name(self, student_id):
        student = self.df.loc[student_id]
        return '{} {}'.format(student['firstname'], student['lastname'])


class Teams:
    def __init__(self, filename):
        self.df = pd.read_excel(filename)
        self.df = self.df.set_index('id')

    def get_ids(self):
        return self.df.index.values


class Question:
    def __init__(self, question_lines, figure, number):
        self.question = ' '.join(question_lines)
        self.fake = []
        self.figure = figure
        self.number = number

    def set_true(self, line):
        self.true = line

    def add_fake(self, line):
        self.fake.append(line)

    def get_rolled_answers(self, key):
        answers = []
        answers.append(self.true)
        answers.extend(self.fake)
        # now roll so that the true answer is at position of the key
        array = np.asarray(answers)
        hops = ord('a') - ord(key)
        return np.roll(array, hops).tolist()

    def write_latex(self, number, key):
        lines = []
        lines.append('\\paragraph{{Question {}:}}\n'.format(number))
        lines.append('{}\n'.format(self.question))
        lines.append('\n')
        if self.figure is not None:
            lines.append('\\begin{{figure}}\\centering\n')
            lines.append('\includegraphics{{{}}}\n'.format(figure))
            lines.append('\caption{{}}\end{{figure}}\n')
        lines.append('\\begin{enumerate}[label=\\textbf{{\\Alph*}},labelindent=0pt, labelsep=1.5em, parsep=0.2em]\n')
        for answer in self.get_rolled_answers(key):
            lines.append('\\item {}\n'.format(answer))
        lines.append('\\end{enumerate}\n')
        return "".join(lines)


class Questionaire:

    def __init__(self):
        self.questions = []

    def _parse(self, lines):

        def remove_answer_prefix(line):
            if line.startswith('{1} true:'):
                return line[len('{1} true:'):].strip()
            elif line.startswith('{2} fake:'):
                return line[len('{2} fake:'):].strip()
            elif line.startswith('{3} fake:'):
                return line[len('{3} fake:'):].strip()
            elif line.startswith('{4} fake:'):
                return line[len('{4} fake:'):].strip()

        state = 'initial'
        linenumber = 0
        preamble = []
        question = []
        question_under_construction = None
        figure = None
        for line in lines:
            linenumber = linenumber + 1
            line = line.strip()
            if not line:
                continue
            if state == 'initial':
                if line.startswith('---'): # yaml preamble start
                    state = 'preamble'
                else:
                    print('Error in line {}: Quiz needs a Yaml preamble, starting with ---.'.format(linenumber))
            elif state == 'preamble':
                if line.startswith('---'): # yaml preamble end
                    preamble = yaml.load('\n'.join(preamble))
                    if not preamble['title']:
                        print('The file must contain a line with a title: attribute.')
                        self.title = None
                    else:
                        self.title = preamble['title']
                    state = 'body'
                else:
                    preamble.append(line)
            elif state == 'body':
                if line.startswith('#'):
                    # create a new question
                    state = 'question'
            elif state == 'question':
                if line.startswith('{'):
                    # finish the question, start answers
                    number = len(self.questions) + 1
                    question_under_construction = Question(question, figure, number)
                    question = []
                    self.questions.append(question_under_construction)
                    figure = None
                    if line.startswith('{1} true:'):
                        question_under_construction.set_true(remove_answer_prefix(line))
                        state = 'answers'
                elif line.startswith('![]('):
                    figure = line[4:-1]
                else:
                    question.append(line)
            elif state == 'answers':
                if line.startswith('{'):
                    question_under_construction.add_fake(remove_answer_prefix(line))
                elif line.startswith('#'):
                    # create a new question
                    state = 'question'

    def read_questionaire(filename):
        with open(filename, 'r') as file:
            content = file.readlines()
            questionaire = Questionaire()
            questionaire._parse(content)
            return questionaire

    def write_latex(self, solution_document, teams, students):
        page_break = '\\cleardoublepage\n\\newpage\n\n'
        lines = []
        # add latex preamble
        abs_file_path = os.path.join(os.path.dirname(__file__), 'resources', 'latex_preamble.tex')
        with open (abs_file_path, "r") as myfile:
            preamble = myfile.read() #.replace('\n', '')
            lines.append(preamble)

        # all question in original order, with 'a' as correct answer
        for q in self.questions:
            print(type(q))
            lines.append(q.write_latex(q.number, 'a'))
        lines.append(page_break)

        # list all solutions on the front page, for all teams
        lines.append('\\subsubsection*{{Scratchcards for Teams}}\n')
        for team_id in teams.get_ids():
            solution = solution_document.solutions[team_id].to_string()
            lines.append('Team {}: {}\\\\\n'.format(team_id, solution))

        # list all solution for all students of each team
        for team_id in teams.get_ids():
            #lines.append('\\subsubsection*\{Team {}\}\n'.format(team_id))
            lines.append('\\subsubsection*{{Team {}}}\n'.format(team_id))
            for student_id in students.get_student_ids_of_team(team_id):
                name = students.get_name(student_id)
                solution = solution_document.solutions[student_id].to_string()
                lines.append('{}:{}\\\\\n'.format(name, solution))
        lines.append(page_break)

        # TODO list solution for extra student

        # questionaire for each team:
        for team_id in teams.get_ids():
            lines.append('\\teamprefix{{{}}}\n\n'.format(team_id))
            solution = solution_document.solutions[team_id]
            for question in self.questions:
                key = solution.answers[question.number-1]
                lines.append(question.write_latex(question.number, key))
            lines.append(page_break)

        for student_id in students.get_ids(): # TODO sort by table
            name = students.get_name(student_id)
            lines.append('\\individualprefix{{{}}}{{{}}}{{{}}}\n\n'.format(name, student_id, team_id))
            solution = solution_document.solutions[student_id]
            # sort question according to solution for this student
            index = 0
            for question_number in solution.questions:
                index += 1
                question = self.questions[question_number - 1]
                key = solution.answers[index - 1]
                lines.append(question.write_latex(index, key))
            lines.append(page_break)

        lines.append('\\end{document}')

        # TODO questionaire for each extra sheet
        return "".join(lines)

class Solution:

    def __init__(self, id, questions, answers):
        self.id = id
        self.questions = questions
        self.answers = answers

    def create_solution_from_questionaire(id, questionaire):
        questions = []
        answers = []
        # for each question, select the right answer
        for question in range(1, len(questionaire.questions)+1):
            questions.append(question)
            answers.append(random.choice(['a', 'b', 'c', 'd']))
        # shuffle the sequence of questions
        random.shuffle(questions)
        solution = Solution(id, questions, answers)
        return solution

    def create_solution_from_string(id, solution_string):
        """
        A solution string looks like this:
        5a 6b 4c

        """
        questions = []
        answers = []
        for token in solution_string.split():
            token = token.strip()
            questions.append(token[0:-1])
            answers.append(token[-1:])
        return Solution(id, questions, answers)

    def to_string(self):
        s = ''
        for q, a in zip(self.questions, self.answers):
            s += str(q) + a + ' '
        return s.strip()

    def roll(answers, key):
        """
        Shift a list of answers according to the key.
        If the key is 'a', the first answer is the correct one and stays at its place.
        If the key is 'b', the first answer is rolled to the second place, and so on.

        a... roll by 0 (do nothing)
        b... roll by -1
        c... roll by -2
        d... roll by -3

        ord('a') == 97
        ord('b') == 98
        """
        array = np.asarray(answers)
        hops = ord('a') - ord(key)
        return np.roll(array, hops).tolist()

class SolutionDocument:
    def __init__(self):
        self.solutions = {}

    # add teams
    def create_solution_document(self, teams, students, questionaire, scratchcard_solution):
        for team_id in teams.get_ids():
            solution = Solution.create_solution_from_string(scratchcard_solution, scratchcard_solution)
            self.solutions[team_id] = solution
        for student_id in students.get_ids():
            solution = Solution.create_solution_from_questionaire(student_id, questionaire)
            self.solutions[student_id] = solution

    def store(self, filename):
        # create a data frame and store it
        content = []
        for key, solution in self.solutions.items():
            content.append({'id': key, 'solution': solution.to_string()})
        df = pd.DataFrame(content)
        df = df.set_index('id')
        df.to_excel(filename)

    def load(self, filename):
        df = pd.read_excel(filename)
        for index, row in df.iterrows():
            self.solutions[row['id']] = Solution.create_solution_from_string(row['id'], row['solution'])

    def printx(self):
        for key, solution in self.solutions.items():
            print('{} / {}'.format(key, solution.to_string()))

def load_students():
    # look for students file
    students = Students('../tests/data/students.xlsx')
    return students

def load_teams():
    # look for teams file
    teams = Teams('../tests/data/teams.xlsx')
    return teams

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

def rat_print():
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



if __name__ == "__main__":

    #print_teams()
    #rat_create()
    rat_print()

    #print('Current directory: {}'.format(os.getcwd()))
    #print('Current parent directory: {}'.format(dirname(os.getcwd())))

    #print(students.get_ids())



    #
    #print_formatted_text(HTML('<ansired>This is red</ansired>'))
    #print_formatted_text(HTML('<ansigreen>This is green</ansigreen>'))
