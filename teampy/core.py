import os
from os.path import dirname, abspath
import yaml
import random
import numpy as np
import pandas as pd

from colorama import init, Fore, Style

# colorama
#init(convert=True) # only if trouble on windows
init(autoreset=True)

def tell(message, level='info'):
    # Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
    # Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
    # Style: DIM, NORMAL, BRIGHT, RESET_ALL
    if level == 'info':
        print(Fore.GREEN + Style.BRIGHT +  ' - ' + Style.RESET_ALL + message)
    elif level == 'warn':
        print(Fore.YELLOW + Style.BRIGHT +  ' - ' + Style.RESET_ALL + message)
    else:
        print(Fore.RED + Style.BRIGHT +  ' - ' + Style.NORMAL + message)

class Students:
    def __init__(self, filename):
        self.df = pd.read_excel(filename, dtype={'id': str, 'team': str, 'table':str})
        self.df = self.df.set_index('id')

    def get_ids(self):
        return self.df.index.values

    def get_student_ids_of_team(self, team_id):
        return self.df[self.df['team']==team_id].index.values

    def get_name(self, student_id):
        student = self.df.loc[student_id]
        return '{} {}'.format(student['firstname'], student['lastname'])

    def get_team_ids(self):
        return self.df['team'].unique()

    def write_students_file():
        students = [{'id': 'aa1', 'team': '01', 'lastname': 'Kraemer', 'firstname': 'Frank Alexander', 'email': 'kraemer@ntnu.no'}]
        students = pd.DataFrame.from_dict(students)
        students = students.set_index('id')
        students.to_excel('students.xlsx')

    def generate_ids():
        assert False
        def get_unique_id(a, b, ids):
            for i in range(1,100):
                idx = (a + b + str(i)).lower()
                if idx not in ids:
                    ids.append(idx)
                    return idx
        email_to_id = {}
        # TODO get already existing ids
        # TODO only set ids on rows that do not yet have one
        ids = []
        for index, row in df.iterrows():
            id = get_unique_id(row['firstname'][0:1], row['lastname'][0:1], ids)
            email_to_id[row['email']] = id
        df['id'] = df['email'].apply(lambda x: email_to_id[x])

    def check():
        # TODO check that all emails are valid and unique
        # TODO check name characters (Latin-1 encoding?)
        # TODO check unique ID
        assert False

    def exists(self, student_id):
        return student_id in self.df.index.values


class Teams:
    def __init__(self):
        pass

    def from_excel(filename):
        teams = Teams()
        teams.df = pd.read_excel(filename)
        teams.df = teams.df.set_index('id')
        return teams

    def from_students(students):
        teams = Teams()
        ids = students.get_team_ids()
        # ids as both id and name
        data = np.transpose(np.array([ids, ids]))
        teams.df = pd.DataFrame(data=data, index=ids, columns=['id','name'])
        return teams

    def get_ids(self):
        return self.df.index.values

    def exists(self, student_id):
        return student_id in self.df.index.values


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
            lines.append('\\begin{figure}\\centering\n')
            lines.append('\includegraphics{{{}}}\n'.format(self.figure))
            lines.append('\caption{}\end{figure}\n')
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
                    return 2, 'Error in line {}: The file needs a Yaml preamble, starting with ---.'.format(linenumber)
            elif state == 'preamble':
                if line.startswith('---'): # yaml preamble end
                    preamble = yaml.load('\n'.join(preamble))
                    if 'title' not in preamble:
                        return 2, 'The preamble at the beginning must contain a line with an attribute \'title\'.'
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
        return 0, None

    def read_questionaire(filename):
        with open(filename, 'r', encoding='latin-1') as file:
            content = file.readlines()
            questionaire = Questionaire()
            questionaire._parse(content)
            return questionaire

    def write_latex(self, solution_document=None, teams=None, students=None):
        page_break = '\\cleardoublepage\n\\newpage\n\n'
        lines = []
        # add latex preamble
        # abs_file_path = os.path.join(os.path.dirname(__file__), 'resources', 'latex_preamble.tex')
        abs_file_path = os.path.join(os.path.dirname(__file__), 'latex_preamble.tex')
        with open (abs_file_path, "r", encoding='latin-1') as myfile:
            preamble = myfile.read() #.replace('\n', '')
            lines.append(preamble)

        # all question in original order, with 'a' as correct answer
        for q in self.questions:
            lines.append(q.write_latex(q.number, 'a'))

        # only print the questionaire for checking it
        if solution_document==None:
            lines.append('\\end{document}')
            return "".join(lines)

        lines.append(page_break)

        # list all solutions on the front page, for all teams
        lines.append('\\subsubsection*{{Scratchcards for Teams}}\n')
        for team_id in teams.get_ids():
            solution = solution_document.team_solutions[team_id]
            if solution.card_id is None:
                lines.append('Team {}: {}\\\\\n'.format(team_id, solution.to_string()))
            else:
                lines.append('Team {}: {} {}\\\\\n'.format(team_id, solution.card_id, solution.to_string()))

        # list all solution for all students of each team
        for team_id in teams.get_ids():
            #lines.append('\\subsubsection*\{Team {}\}\n'.format(team_id))
            lines.append('\\subsubsection*{{Team {}}}\n'.format(team_id))
            for student_id in students.get_student_ids_of_team(team_id):
                name = students.get_name(student_id)
                solution = solution_document.student_solutions[student_id].to_string()
                lines.append('{}:{}\\\\\n'.format(name, solution))
        lines.append(page_break)

        # TODO list solution for extra student

        # questionaire for each team:
        for team_id in teams.get_ids():
            lines.append('\\teamprefix{{{}}}\n\n'.format(team_id))
            solution = solution_document.team_solutions[team_id]
            for question in self.questions:
                key = solution.answers[question.number-1]
                lines.append(question.write_latex(question.number, key))
            lines.append(page_break)

        for student_id in students.get_ids(): # TODO sort by table
            name = students.get_name(student_id)
            lines.append('\\individualprefix{{{}}}{{{}}}{{{}}}\n\n'.format(name, student_id, team_id))
            solution = solution_document.student_solutions[student_id]
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

    def __init__(self, questions, answers, card_id=None):
        self.card_id = card_id
        self.questions = questions
        self.answers = answers

    def create_solution_from_questionaire(questionaire):
        questions = []
        answers = []
        # for each question, select the right answer
        for question in range(1, len(questionaire.questions)+1):
            questions.append(question)
            answers.append(random.choice(['a', 'b', 'c', 'd']))
        # shuffle the sequence of questions
        random.shuffle(questions)
        solution = Solution(questions, answers)
        return solution

    def create_solution_from_string(solution_string, card_id=None):
        """
        A solution string looks like this:
        5a 6b 4c

        Or like this:
        a b c

        Or like this:
        abc
        """
        questions = []
        answers = []
        solution_string = solution_string.strip()
        if any(char.isdigit() for char in solution_string):
            # form that also shuffles the sequence of questions
            for token in solution_string.split():
                token = token.strip()
                questions.append(token[0:-1])
                answers.append(token[-1:])
        elif ' ' in solution_string:
            # questions stay in the same sequence
            question_number = 0
            for token in solution_string.split():
                question_number += 1
                token = token.strip()
                questions.append(str(question_number))
                answers.append(token)
        else:
            question_number = 0
            for token in list(solution_string):
                question_number += 1
                questions.append(str(question_number))
                answers.append(token)
        return Solution(questions, answers, card_id=card_id)

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
        self.student_solutions = {}
        self.team_solutions = {}

    # add teams
    def create_solution_document(self, teams, students, questionaire, scratchcard_solution):
        for team_id in teams.get_ids():
            self.team_solutions[team_id] = scratchcard_solution
        for student_id in students.get_ids():
            solution = Solution.create_solution_from_questionaire(questionaire)
            self.student_solutions[student_id] = solution

    def store(self, filename):
        # create a data frame and store it
        #content = []
        #for key, solution in self.solutions.items():
        #    content.append({'id': key, 'solution': solution.to_string()})
        #df = pd.DataFrame(content)
        #df = df.set_index('id')
        #df.to_excel(filename)
        lines = []
        for key in sorted(self.team_solutions.keys()):
            lines.append('{}: {}\n'.format(key, self.team_solutions[key].to_string()))
        for key in sorted(self.student_solutions.keys()):
            lines.append('{}: {}\n'.format(key, self.student_solutions[key].to_string()))
        #for key, solution in self.solutions.items():
        #    lines.append('{}: {}\n'.format(key, solution.to_string()))
        with open(filename, 'w') as file:
            file.write("".join(lines))
            #yaml.dump(self.solutions, outfile, default_flow_style=False)

    def load(self, filename):
        df = pd.read_excel(filename)
        for index, row in df.iterrows():
            self.solutions[row['id']] = Solution.create_solution_from_string(row['id'], row['solution'])

    def printx(self):
        for key, solution in self.solutions.items():
            print('{} / {}'.format(key, solution.to_string()))


class ResultLine:

    def __init__(self, result_id, result, checksum, line_number):
        self.result_id = result_id
        self.result = result
        self.checksum = checksum
        self.line_number = line_number


class Result:

    def __init__(self):
        pass

    def _parse_result_line(self, result, line_number):
        tokens = result.split('/')
        if len(tokens) != 3:
            tell('The result string in line {} must consist of id/result/checksum.'.format(line_number), 'warn')
            return None
        return ResultLine(tokens[0].strip(),
                          tokens[1].strip(),
                          tokens[2].strip(),
                          line_number)

    def _parse_results(self, lines, teams, students):
        # initial --> preamble --> results
        state = 'initial'
        line_number = 0
        preamble = []
        result_lines = []
        unique_ids = []
        for line in lines:
            line_number = line_number + 1
            line = line.strip()
            if not line:
                # ignore empty lines
                continue
            if state == 'initial':
                if line.startswith('---'): # yaml preamble start
                    state = 'preamble'
                else:
                    return 2, 'Error in line {}: The file needs a Yaml preamble, starting with ---.'.format(linenumber)
            elif state == 'preamble':
                if line.startswith('---'): # yaml preamble end
                    preamble = yaml.load('\n'.join(preamble))
                    # assign table to object
                    state = 'results'
                else:
                    preamble.append(line)
            elif state == 'results':
                if line.startswith('#'):
                    # ignore, it's a comment
                    pass
                else:
                    result_line = self._parse_result_line(line, line_number)
                    if result_line is not None:
                        result_lines.append(result_line)
                        if result_line.result_id in unique_ids:
                             tell('Line {}: A line with the id {} already exists.'.format(result_line.line_number, result_line.result_id), 'warn')
                        else:
                            unique_ids.append(result_line.result_id)

        # finished parsing the file

        if state is not 'results':
            tell('The results file is not complete.', 'error')

        # check the preamble
        if 'name' not in preamble:
            tell('The results file should contain a name field in the preamble.', 'warn')
        else:
            self.name = preamble['name']
        if 'date' not in preamble:
            tell('The results file should contain a date field in the preamble.', 'warn')
        else:
            self.date = preamble['date']

        for result_line in result_lines:
            # check that student or team with matching id exists
            if students.exists(result_line.result_id):
                # found student
                print('found {}'.format(result_line.result_id))
            elif teams.exists(result_line.result_id):
                # found team
                print('found {}'.format(result_line.result_id))
            else:
                tell('Line {}: There exists no student or team with id {}.'.format(result_line.line_number, result_line.result_id), 'warn')
            # TODO check that result has proper length
            # TODO check that checksum is correct

    def load_results(self, file_input, teams, students):
        lines = file_input.readlines()
        file_input.close()
        self._parse_results(lines, teams, students)

class Teampy:

    def __init__(self):
        self.load_context()

    def get_teams(self):
        return self.teams

    def load_scratch_cards(self, filename):
        rawcodes = yaml.load(open(filename, 'r', encoding='latin-1'))
        codes = {}
        for key in rawcodes:
            codes[key] = Solution.create_solution_from_string(rawcodes[key], card_id=key)
        return codes

    def find_main_directory(self):
        # look in the current working directory
        dirs = [os.getcwd(), os.path.dirname(os.getcwd())]
        for directory in dirs:
            student_file = os.path.join(directory, 'students.xlsx')
            if os.path.isfile(student_file):
                return directory
        return None

    def load_context(self):
        directory = self.find_main_directory()
        if directory is None:
            tell('Could not find the students file.', level='error')
            quit()

        students_file = os.path.join(directory, 'students.xlsx')
        self.students = Students(students_file)

        teams_file = os.path.join(directory, 'teams.xlsx')
        if os.path.isfile(teams_file):
            self.teams = Teams.from_excel(teams_file)
        else:
            self.teams = Teams.from_students(self.students)

        self.scratchcards = {}
        scratchcards_file = os.path.join(directory, 'scratchcards.txt')
        if os.path.isfile(scratchcards_file):
            tell('Reading the scratchcards file.')
            self.scratchcards = self.load_scratch_cards(scratchcards_file)
