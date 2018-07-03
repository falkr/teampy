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

from prompt_toolkit import prompt, print_formatted_text, HTML
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.key_binding import KeyBindings

bindings = KeyBindings()

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


class Question:
    def __init__(self, question_lines):
        self.question = ' '.join(question_lines)
        self.fake = []

    def set_true(self, line):
        self.true = line

    def add_fake(self, line):
        self.fake.append(line)


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
                    question_under_construction = Question(question)
                    self.questions.append(question_under_construction)
                    if line.startswith('{1} true:'):
                        question_under_construction.set_true(remove_answer_prefix(line))
                        state = 'answers'
                else:
                    self.questions.append(line)
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
        return ' '.join(['{}{}'] * len(self.questions)).format(*tuple(self.questions), *tuple(self.answers))

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

    def create_solution_document(self, students, questionaire):
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

class NumberValidator(Validator):
    def validate(self, document):
        text = document.text

        if text and not text.isdigit():
            i = 0

            # Get index of fist non numeric character.
            # We want to move the cursor here.
            for i, c in enumerate(text):
                if not c.isdigit():
                    break

            raise ValidationError(message='This input contains non-numeric characters',
                                  cursor_position=i)

@bindings.add('escape')
def _(event):
    " Do something if 'a' has been pressed. "
    print('escape')

def rat_create():
    """
    Create a template file for a RAT
    """
    print_formatted_text(HTML('<darkgray>Create a new template file for a RAT.</darkgray>'))
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

    # create a solution file
    sd = SolutionDocument()
    sd.create_solution_document(students, questionaire)
    sd.store('solution.xlsx')

    sd_2 = SolutionDocument()
    sd_2.load('solution.xlsx')
    sd_2.printx()


if __name__ == "__main__":

    print_teams()
    rat_create()
    #rat_print()

    print('Current directory: {}'.format(os.getcwd()))
    print('Current parent directory: {}'.format(dirname(os.getcwd())))

    #print(students.get_ids())



    #
    #print_formatted_text(HTML('<ansired>This is red</ansired>'))
    #print_formatted_text(HTML('<ansigreen>This is green</ansigreen>'))
