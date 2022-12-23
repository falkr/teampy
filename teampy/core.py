import os
from os.path import dirname, abspath
import yaml
import random
import numpy as np
import pandas as pd

import re

from colorama import init, Fore, Style

# colorama
# init(convert=True) # only if trouble on windows
init(autoreset=True)


def tell(message, level="info"):
    # Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
    # Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
    # Style: DIM, NORMAL, BRIGHT, RESET_ALL
    if level == "info":
        print(Fore.GREEN + Style.BRIGHT + " - " + Style.RESET_ALL + message)
    elif level == "warn":
        print(Fore.YELLOW + Style.BRIGHT + " - " + Style.RESET_ALL + message)
    else:
        print(Fore.RED + Style.BRIGHT + " - " + Style.NORMAL + message)


def tex_escape(text):
    """
    :param text: a plain text message
    :return: the message escaped to appear correctly in LaTeX
    """
    conv = {
        "æ": r"\ae{}",
        "Æ": r"\AE{}",
        "ø": r"\o{}",
        "Ø": r"\O{}",
        "å": r"\aa{}",
        "Å": r"\AA{}",
        "ä": r"\AE{}",
        "Ä": r"\AE{}",
        "ö": r"\"o{}",
        "Ö": r"\"O{}",
        "ü": r"\"u{}",
        "Ü": r"\"U{}",
        "ß": r"\ss{}",
        "ç": r"\c{c}",
        "Ç": r"\c{C}",
        "ô": r"\^{o}",
        "Ô": r"\^{O}",
        "á": r"\'{a}",
        "Á": r"\'{A}",
        "à": r"\`{a}",
        "À": r"\`{A}",
        "é": r"\'{e}",
        "É": r"\'{E}",
        "è": r"\`{e}",
        "È": r"\`{E}",
        "ó": r"\'{o}",
        "Ó": r"\'{O}",
        "ò": r"\`{o}",
        "Ò": r"\`{O}",
        # TODO add many more... like french accents,...
    }
    regex = re.compile(
        "|".join(
            re.escape(key) for key in sorted(conv.keys(), key=lambda item: -len(item))
        )
    )
    return regex.sub(lambda match: conv[match.group()], text)


class Students:
    def __init__(self, filename):
        self.df = pd.read_excel(
            filename, converters={"id": str, "team": str, "table": str}
        )
        self.df = self.df.set_index("id")
        if all(self.df.team.apply(lambda team: team.isdigit())):
            self.df["team_int"] = self.df.team.astype(int)
        if "table" in self.df.columns:
            # TODO - [ ] ERROR when we have a table that excel reads in as float, then no gigit!
            if all(self.df.table.apply(lambda table: table.isdigit())):
                self.df["table_int"] = self.df.table.astype(int)

    def assigned_to_tables(self):
        return "table" in self.df.columns

    def get_ids(self, sort_by="lastname"):
        if (sort_by == "team") & ("team_int" in self.df.columns):
            sorted_df = self.df.sort_values("team_int")
        elif (sort_by == "table") & ("table_int" in self.df.columns):
            sorted_df = self.df.sort_values("table_int")
        else:
            sorted_df = self.df.sort_values(sort_by)
        return sorted_df.index.values

    def get_student_ids_of_team(self, team_id):
        return self.df[self.df["team"] == team_id].index.values

    def get_name(self, student_id):
        student = self.df.loc[student_id]
        return "{} {}".format(student["firstname"], student["lastname"])

    def get_firstname(self, student_id):
        student = self.df.loc[student_id]
        return student["firstname"]

    def get_lastname(self, student_id):
        student = self.df.loc[student_id]
        return student["lastname"]

    def get_email(self, student_id):
        student = self.df.loc[student_id]
        return student["email"]

    def get_team(self, student_id):
        student = self.df.loc[student_id]
        return str(student["team"])

    def get_table(self, student_id):
        student = self.df.loc[student_id]
        return str(student["table"])

    def get_team_ids(self):
        return self.df["team"].unique()

    @staticmethod
    def write_students_file():
        students = [
            {
                "id": "aa1",
                "team": "01",
                "lastname": "Kraemer",
                "firstname": "Frank Alexander",
                "email": "kraemer@ntnu.no",
            }
        ]
        students = pd.DataFrame.from_dict(students)
        students = students.set_index("id")
        students.to_excel("students.xlsx")

    def generate_ids(self):
        assert False

        def get_unique_id(a, b, ids):
            for i in range(1, 100):
                idx = (a + b + str(i)).lower()
                if idx not in ids:
                    ids.append(idx)
                    return idx

        email_to_id = {}
        # TODO get already existing ids
        # TODO only set ids on rows that do not yet have one
        ids = []
        for index, row in df.iterrows():
            id = get_unique_id(row["firstname"][0:1], row["lastname"][0:1], ids)
            email_to_id[row["email"]] = id
        df["id"] = df["email"].apply(lambda x: email_to_id[x])

    def check(self):
        # TODO check that all emails are valid and unique
        # TODO check unique ID
        assert False

    def exists(self, student_id):
        return student_id in self.df.index.values


class Teams:
    def __init__(self):
        pass

    @staticmethod
    def from_excel(filename):
        teams = Teams()
        teams.df = pd.read_excel(filename, dtype={"id": str, "name": str})
        teams.df = teams.df.set_index("id")
        # TODO check that all teams referred to by students file are in here
        return teams

    @staticmethod
    def from_students(students):
        teams = Teams()
        ids = students.get_team_ids()
        # ids as both id and name
        data = np.transpose(np.array([ids, ids]))
        teams.df = pd.DataFrame(data=data, index=ids, columns=["id", "name"])
        return teams

    def get_ids(self):
        return self.df.index.values

    def exists(self, team_id):
        return team_id in self.df.index.values

    def get_rat_precentage(self, team_id):
        team = self.df.loc[team_id]
        if "pt" in team:
            return team["pt"]
        else:
            return 0


class Question:
    def __init__(self, question_lines, figure, number):
        self.question = "\n".join(question_lines)
        self.fake = []
        self.figure = figure
        self.number = number

    def set_true(self, line):
        self.true = line

    def add_fake(self, line):
        self.fake.append(line)

    def get_answers(self):
        return [self.true] + self.fake.copy()

    def get_rolled_answers(self, key):
        answers = []
        answers.append(self.true)
        answers.extend(self.fake)
        # now roll so that the true answer is at position of the key
        array = np.asarray(answers)
        hops = ord(key) - ord("a")
        return np.roll(array, hops).tolist()

    def write_latex(self, number, key, old_latex=False):
        lines = []
        if old_latex:
            lines.append("\\paragraph{{Question {}:}}\n".format(number))
        else:
            lines.append("\\vbox{{\\question{{{}}}\n".format(number))
        lines.append("{}\n".format(self.question))
        lines.append("\n")
        if self.figure is not None:
            lines.append("\\begin{figure}\\centering\n")
            lines.append("\includegraphics{{{}}}\n".format(self.figure))
            lines.append("\end{figure}\n")
        lines.append(
            "\\begin{enumerate}[label=\\textbf{{\\Alph*}},labelindent=0pt, labelsep=1.5em, parsep=0.2em]\n"
        )
        for answer in self.get_rolled_answers(key):
            lines.append("\\item {}\n".format(answer))
        lines.append("\\end{enumerate}}\n")
        return "".join(lines)

    def write_blackboard(self, key):
        line = "MC" + "\t"
        line = line + self.question + "\t"
        for i, answer in enumerate(self.get_rolled_answers(key), start=1):
            if answer == self.true:
                line = line + answer + "\t" + "correct" + "\t"
            else:
                line = line + answer + "\t" + "incorrect" + "\t"
        return line

    def write_supermark(self, key):
        line = "## Question {}\n\n".format(self.number)
        line = line + ":rat:" + self.question + "\n\n"
        for i, answer in enumerate(self.get_rolled_answers(key), start=1):
            line = line + "{}. ".format(i) + answer + "\n"
        return line


def test():
    q = Question([], None, 3)
    q.set_true("True answer.")
    q.add_fake("Fake answer (b)")
    q.add_fake("Fake answer (c)")
    q.add_fake("Fake answer (d)")
    for key in ["a", "b", "c", "d"]:
        print("---key {}".format(key))
        for answer in q.get_rolled_answers(key):
            print(answer)


class Questionaire:
    def __init__(self):
        self.questions = []

    def number_of_questions(self):
        return len(self.questions)

    def _parse(self, lines):
        def remove_answer_prefix(line):
            if line.startswith("{1} true:"):
                return line[len("{1} true:") :].strip()
            elif line.startswith("{2} fake:"):
                return line[len("{2} fake:") :].strip()
            elif line.startswith("{3} fake:"):
                return line[len("{3} fake:") :].strip()
            elif line.startswith("{4} fake:"):
                return line[len("{4} fake:") :].strip()

        state = "initial"
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
            if state == "initial":
                if line.startswith("---"):  # yaml preamble start
                    state = "preamble"
                else:
                    return (
                        2,
                        "Error in line {}: The file needs a Yaml preamble, starting with ---.".format(
                            linenumber
                        ),
                    )
            elif state == "preamble":
                if line.startswith("---"):  # yaml preamble end
                    preamble = yaml.safe_load("\n".join(preamble))
                    if "title" not in preamble:
                        return (
                            2,
                            "The preamble at the beginning must contain a line with an attribute 'title'.",
                        )
                        self.title = None
                    else:
                        self.title = preamble["title"]
                    state = "body"
                else:
                    preamble.append(line)
            elif state == "body":
                if line.startswith("#"):
                    # create a new question
                    state = "question"
            elif state == "question":
                if line.startswith("{"):
                    # finish the question, start answers
                    number = len(self.questions) + 1
                    question_under_construction = Question(question, figure, number)
                    question = []
                    self.questions.append(question_under_construction)
                    figure = None
                    if line.startswith("{1} true:"):
                        question_under_construction.set_true(remove_answer_prefix(line))
                        state = "answers"
                elif line.startswith("![]("):
                    figure = line[4:-1]
                else:
                    question.append(line)
            elif state == "answers":
                if line.startswith("{"):
                    question_under_construction.add_fake(remove_answer_prefix(line))
                elif line.startswith("#"):
                    # create a new question
                    state = "question"
        return 0, None

    @staticmethod
    def read_questionaire(filename):
        with open(filename, "r", encoding="utf-8") as file:
            content = file.readlines()
            questionaire = Questionaire()
            questionaire._parse(content)
            return questionaire

    def write_trial_latex(self):
        lines = []
        # add latex preamble
        # abs_file_path = os.path.join(os.path.dirname(__file__), 'resources', 'latex_preamble.tex')
        abs_file_path = os.path.join(os.path.dirname(__file__), "latex_preamble.tex")
        with open(abs_file_path, "r", encoding="utf-8") as myfile:
            preamble = myfile.read()  # .replace('\n', '')
            lines.append(preamble)
        lines.append("\\subsubsection*{{RAT Test Run}}\n")
#        index = 0
        for q in self.questions:
#            index += 1
            key = random.choice(["a", "b", "c", "d"])
#            lines.append(q.write_latex(index, key))
            lines.append(q.write_latex(q.number, key))
        lines.append("\\end{document}")
        return "".join(lines)

    def write_pdf(self, solution):
        lines = []
        # add latex preamble
        # abs_file_path = os.path.join(os.path.dirname(__file__), 'resources', 'latex_preamble.tex')
        abs_file_path = os.path.join(os.path.dirname(__file__), "latex_preamble.tex")
        with open(abs_file_path, "r", encoding="utf-8") as myfile:
            preamble = myfile.read()  # .replace('\n', '')
            lines.append(preamble)
        # lines.append("\\subsubsection*{{RAT}}\n")
        lines.append("\\vbox{\\textbf"
                     + "{{{}}}".format(self.title)
                     + "}\n")
        if len(self.questions) > len(solution.answers):
            raise Exception("You must provide enough solutions. There are more questions than answers!")

        for q in self.questions:
            key = solution.answers[q.number - 1]
            #lines.append(q.write_latex(index, key))
            lines.append(q.write_latex(q.number, key))
        lines.append("\\end{document}")
        return "".join(lines)

    def write_blackboard(self, solution):
        lines = []
        for q in self.questions:
            key = solution.answers[q.number - 1]
            lines.append(q.write_blackboard(key))
        return "\n".join(lines)

    def write_supermark(self, solution):
        lines = []
        for q in self.questions:
            key = solution.answers[q.number - 1]
            lines.append(q.write_supermark(key))
        return "\n".join(lines)

    def write_latex(
        self,
        solution_document=None,
        teams=None,
        students=None,
        old_latex=False,
        teamonly=False,
    ):
        course, date = "", ""
        page_break = "\\cleardoublepage\n\\newpage\n\n"
        lines = []
        # add latex preamble
        # abs_file_path = os.path.join(os.path.dirname(__file__), 'resources', 'latex_preamble.tex')
        abs_file_path = os.path.join(os.path.dirname(__file__), "latex_preamble.tex")
        with open(abs_file_path, "r", encoding="utf-8") as myfile:
            preamble = myfile.read()  # .replace('\n', '')
            lines.append(preamble)

        # all question in original order, with 'a' as correct answer
        for q in self.questions:
            lines.append(q.write_latex(q.number, "a"))

        # only print the questionaire for checking it
        if solution_document is None:
            lines.append("\\end{document}")
            return "".join(lines)

        lines.append(page_break)

        # list all solutions on the front page, for all teams
        lines.append("\\subsubsection*{{Scratchcards for Teams}}\n")
        for team_id in teams.get_ids():
            solution = solution_document.team_solutions[team_id]
            if solution.card_id is None:
                lines.append("Team {}: {}\\\\\n".format(team_id, solution.to_string()))
            else:
                lines.append(
                    "Team {}: {} {}\\\\\n".format(
                        team_id, solution.card_id, solution.to_string()
                    )
                )
        if not teamonly:
            # list all solution for all students of each team
            for team_id in teams.get_ids():
                # lines.append('\\subsubsection*\{Team {}\}\n'.format(team_id))
                lines.append("\\subsubsection*{{Team {}}}\n".format(team_id))
                for student_id in students.get_student_ids_of_team(team_id):
                    name = tex_escape(students.get_name(student_id))
                    solution = solution_document.student_solutions[
                        student_id
                    ].to_string()
                    lines.append("{}:{}\\\\\n".format(name, solution))
            lines.append(page_break)

        # TODO list solution for extra students

        # questionaire for each team:
        for team_id in teams.get_ids():
            lines.append(
                "\\teamprefix"
                + "{{{}}}{{{}}}{{{}}}{{{}}}".format(team_id, course, self.title, date)
                + "\n\n"
            )
            solution = solution_document.team_solutions[team_id]
            for question in self.questions:
                key = solution.answers[question.number - 1]
                lines.append(question.write_latex(question.number, key))
            lines.append(page_break)
        # rest the thumb index
        lines.append("\\thumbnewcolumn\n")

        # questionaire for each student
        if not teamonly:
            old_thumb = None
            if students.assigned_to_tables():
                for student_id in students.get_ids(sort_by="table"):
                    name = tex_escape(students.get_name(student_id))
                    team_id = students.get_team(student_id)
                    table = students.get_table(student_id)
                    if old_thumb != table:
                        lines.append(
                            "\\addthumb{}" + "{{{}}}".format(table) + "{white}{black}\n"
                        )
                    lines.append(
                        "\\individualprefix"
                        + "{{{}}}{{{}}}{{{}}}{{{}}}{{{}}}{{{}}}{{{}}}".format(
                            name, student_id, team_id, table, course, self.title, date
                        )
                        + "\n\n"
                    )
                    solution = solution_document.student_solutions[student_id]
                    # sort question according to solution for this student
                    index = 0
                    for question_number in solution.questions:
                        index += 1
                        question = self.questions[question_number - 1]
                        key = solution.answers[index - 1]
                        lines.append(question.write_latex(index, key))
                    lines.append(page_break)
                    old_thumb = table
            else:
                for student_id in students.get_ids(sort_by="team"):
                    name = tex_escape(students.get_name(student_id))
                    team_id = students.get_team(student_id)
                    if old_thumb != team_id:
                        lines.append(
                            "\\addthumb{}"
                            + "{{{}}}".format(team_id)
                            + "{white}{black}\n"
                        )
                    lines.append(
                        "\\individualprefix"
                        + "{{{}}}{{{}}}{{{}}}{{{}}}{{{}}}{{{}}}{{{}}}".format(
                            name, student_id, team_id, "", course, self.title, date
                        )
                        + "\n\n"
                    )
                    solution = solution_document.student_solutions[student_id]
                    # sort question according to solution for this student
                    index = 0
                    for question_number in solution.questions:
                        index += 1
                        question = self.questions[question_number - 1]
                        key = solution.answers[index - 1]
                        lines.append(question.write_latex(index, key))
                    lines.append(page_break)
                    old_thumb = team_id
        lines.append("\\end{document}")

        # TODO questionaire for each extra sheet
        return "".join(lines)

    def write_latex_old(self, solution_document=None, teams=None, students=None):
        page_break = "\\cleardoublepage\n\\newpage\n\n"
        lines = []
        # add latex preamble
        # abs_file_path = os.path.join(os.path.dirname(__file__), 'resources', 'latex_preamble.tex')
        abs_file_path = os.path.join(
            os.path.dirname(__file__), "latex_preamble_old.tex"
        )
        with open(abs_file_path, "r", encoding="utf-8") as myfile:
            preamble = myfile.read()  # .replace('\n', '')
            lines.append(preamble)

        # all question in original order, with 'a' as correct answer
        for q in self.questions:
            lines.append(q.write_latex(q.number, "a", old_latex=True))

        # only print the questionaire for checking it
        if solution_document == None:
            lines.append("\\end{document}")
            return "".join(lines)

        lines.append(page_break)

        # list all solutions on the front page, for all teams
        lines.append("\\subsubsection*{{Scratchcards for Teams}}\n")
        for team_id in teams.get_ids():
            solution = solution_document.team_solutions[team_id]
            if solution.card_id is None:
                lines.append("Team {}: {}\\\\\n".format(team_id, solution.to_string()))
            else:
                lines.append(
                    "Team {}: {} {}\\\\\n".format(
                        team_id, solution.card_id, solution.to_string()
                    )
                )

        # list all solution for all students of each team
        for team_id in teams.get_ids():
            # lines.append('\\subsubsection*\{Team {}\}\n'.format(team_id))
            lines.append("\\subsubsection*{{Team {}}}\n".format(team_id))
            for student_id in students.get_student_ids_of_team(team_id):
                name = tex_escape(students.get_name(student_id))
                solution = solution_document.student_solutions[student_id].to_string()
                lines.append("{}:{}\\\\\n".format(name, solution))
        lines.append(page_break)

        # TODO list solution for extra students

        # questionaire for each team:
        for team_id in teams.get_ids():
            lines.append("\\teamprefix{{{}}}\n\n".format(team_id))
            solution = solution_document.team_solutions[team_id]
            for question in self.questions:
                key = solution.answers[question.number - 1]
                lines.append(question.write_latex(question.number, key, old_latex=True))
            lines.append(page_break)

        # questionaire for each student
        sort_by = "team"
        if students.assigned_to_tables():
            sort_by = "table"
        for student_id in students.get_ids(sort_by=sort_by):
            name = tex_escape(students.get_name(student_id))
            team_id = students.get_team(student_id)
            if students.assigned_to_tables():
                table = students.get_table(student_id)
                lines.append(
                    "\\individualprefixtable{{{}}}{{{}}}{{{}}}{{{}}}\n\n".format(
                        name, student_id, team_id, table
                    )
                )
            else:
                lines.append(
                    "\\individualprefix{{{}}}{{{}}}{{{}}}\n\n".format(
                        name, student_id, team_id
                    )
                )
            solution = solution_document.student_solutions[student_id]
            # sort question according to solution for this student
            index = 0
            for question_number in solution.questions:
                index += 1
                question = self.questions[question_number - 1]
                key = solution.answers[index - 1]
                lines.append(question.write_latex(index, key, old_latex=True))
            lines.append(page_break)

        lines.append("\\end{document}")

        # TODO questionaire for each extra sheet
        return "".join(lines)


class Solution:
    def __init__(self, questions, answers, card_id=None):
        self.card_id = card_id
        self.questions = questions
        self.answers = answers

    @staticmethod
    def create_solution_from_questionaire(questionaire, shuffle_questions=True):
        # TODO we should check that the solution does not contain 10 times the same letter, because that would mess up the format of the checksum
        questions = []
        answers = []
        # for each question, select a random right answer
        for question in range(1, len(questionaire.questions) + 1):
            questions.append(question)
            answers.append(random.choice(["a", "b", "c", "d"]))
        if shuffle_questions:
            # shuffle the sequence of questions
            random.shuffle(questions)
        solution = Solution(questions, answers)
        return solution

    @staticmethod
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
        elif " " in solution_string:
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
        s = ""
        for q, a in zip(self.questions, self.answers):
            s += str(q) + a + " "
        return s.strip()

    def get_correct_answers_string(self):
        return "".join(self.answers)

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
        hops = ord("a") - ord(key)
        return np.roll(array, hops).tolist()


class SolutionDocument:
    def __init__(self):
        self.student_solutions = {}
        self.team_solutions = {}

    def get_team_solution(self, team_id):
        if team_id in self.team_solutions:
            return self.team_solutions[team_id]
        else:
            print("no team solution for {}".format(team_id))
            print(self.team_solutions)
            return None

    def get_student_solution(self, student_id):
        if student_id in self.student_solutions:
            return self.student_solutions[student_id]
        else:
            return None

    # add teams
    def create_solution_document(
        self, teams, students, questionaire, scratchcard_solution
    ):
        for team_id in teams.get_ids():
            self.team_solutions[team_id] = scratchcard_solution
        for student_id in students.get_ids():
            solution = Solution.create_solution_from_questionaire(questionaire)
            self.student_solutions[student_id] = solution

    def store(self, filename):
        # create a data frame and store it
        # content = []
        # for key, solution in self.solutions.items():
        #    content.append({'id': key, 'solution': solution.to_string()})
        # df = pd.DataFrame(content)
        # df = df.set_index('id')
        # df.to_excel(filename)
        lines = []
        for key in sorted(self.team_solutions.keys()):
            lines.append("{}: {}\n".format(key, self.team_solutions[key].to_string()))
        for key in sorted(self.student_solutions.keys()):
            lines.append(
                "{}: {}\n".format(key, self.student_solutions[key].to_string())
            )
        # for key, solution in self.solutions.items():
        #    lines.append('{}: {}\n'.format(key, solution.to_string()))
        with open(filename, "w") as file:
            file.write("".join(lines))
            # yaml.dump(self.solutions, outfile, default_flow_style=False)

    def load(self, filename, students, teams):
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
            line_number = 0
            for line in lines:
                line_number += 1
                line = line.strip()
                if not line:
                    continue
                elements = line.split(":")
                if len(elements) != 2:
                    tell(
                        "Invalid entry in line {} of the file {}.".format(
                            line_number, filename
                        ),
                        "error",
                    )
                else:
                    key = elements[0].strip()
                    rawcode = elements[1].strip()
                    if teams.exists(key):
                        self.team_solutions[key] = Solution.create_solution_from_string(
                            rawcode
                        )
                    elif students.exists(key):
                        self.student_solutions[
                            key
                        ] = Solution.create_solution_from_string(rawcode)
                    else:
                        tell(
                            "Entry for id {} in line {} does not correspond to a team or student.".format(
                                key, line_number
                            ),
                            "error",
                        )
        tell("Reading solutions file")

    def printx(self):
        for key, solution in self.solutions.items():
            print("{} / {}".format(key, solution.to_string()))


class ResultLine:
    def __init__(
        self, result_id, result, checksum, line_number, questionaire, filename, students
    ):
        self.result_id = result_id
        self.result = result
        self.checksum = checksum
        self.line_number = line_number
        self.questionaire = questionaire
        self.filename = filename
        self.students = students
        # will be set later:
        self.solution = None
        self.type = None  # 'student' or 'team'
        self.valid = False

    def check(self):
        team = ""
        if self.type == "student":
            team = self.students.get_team(self.result_id)
            if team is None:
                team = ""
            else:
                team = " (team {})".format(team)
        # check that result has proper length
        # TODO also print which filename, like 'results.txt'
        # TODO also print which team a student belongs to, for easier finding it
        if len(self.result) != self.questionaire.number_of_questions():
            tell(
                "File {}, line {}: The result entry for id {}{} has {} letters, but the RAT has {} questions.".format(
                    self.filename,
                    self.line_number,
                    self.result_id,
                    team,
                    len(self.result),
                    self.questionaire.number_of_questions(),
                ),
                "error",
            )
            return False
        # check that the answer alternatives are proper letters within the range (+x)
        valid_letters = ["a", "b", "c", "d", "x"]
        for letter in self.result:
            if letter not in valid_letters:
                tell(
                    'File {}, line {}: The result entry for id {}{} contains letter "{}", which is not valid. Only answer alternative letters ("a", "b",...) and "x" are allowed.'.format(
                        self.filename, self.line_number, self.result_id, team, letter
                    ),
                    "error",
                )
                return False
        # check that checksum is correct, and that it corresponds with result string
        # if self.type is "student":
        if self.type == "student":
            if len(self.checksum) != 4:
                tell(
                    "File {}, line {}: The checksum for student with id {}{} is wrong.".format(
                        self.filename, self.line_number, self.result_id, team
                    ),
                    "error",
                )
                return False
            for number in self.checksum:
                if number not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    tell(
                        "File {}, line {}: The checksum for student with id {}{} is wrong.".format(
                            self.filename, self.line_number, self.result_id, team
                        ),
                        "error",
                    )
                    return False
            for index, letter in enumerate(["a", "b", "c", "d"]):
                if self.result.count(letter) != int(self.checksum[index]):
                    tell(
                        "File {}, line {}: The checksum for student with id {}{} is inconsistent.".format(
                            self.filename, self.line_number, self.result_id, team
                        ),
                        "error",
                    )
                    return False
        elif self.type == "team":
            pass
            # count correct results

        if self.solution is None:
            return
        self.valid = True

        # unshuffle the questions, bring back into original question sequence
        self.normalized_results = (
            {}
        )  # = np.arange(self.questionaire.number_of_questions())
        for index, question in enumerate(self.solution.questions):
            if index < len(self.result):
                answer_given = self.result[index]
                if answer_given == "x":
                    self.normalized_results[int(question)] = "x"
                else:
                    answer_given_ord = ord(answer_given) - ord("a")  # 0, 1, 2,...
                    # now also transform back the answer given, based on the solution letter
                    answer_key = self.solution.answers[index]
                    array = np.asarray(["a", "b", "c", "d"])
                    hops = ord("a") - ord(answer_key)
                    answer_given = np.roll(array, -hops)[answer_given_ord]
                    self.normalized_results[int(question)] = answer_given

        correct_answers = 0
        for c in self.normalized_results.values():
            if c == "a":
                correct_answers += 1
# original        self.score = 100 * correct_answers / len(self.normalized_results)
        if self.type == "student":
            self.score = 100 * correct_answers / len(self.normalized_results)
        elif self.type == "team":
            total_qs = len(self.normalized_results)
            # using the checksum as the number of attempts
            attempts = int(self.checksum)
            # we assume each team got all the correct answers
            # and count the "extra" attempts to penalise the score
            # instead of counting only the ones right on the first attempt
            # NOTE: this assumes 4 possible options 
            total_choices = 4
            self.score = 100 - (attempts - total_qs) * (100/total_qs) / (total_choices - 1)

        # print('--Results for {}'.format(self.result_id))
        # print('              {}'.format(self.result))
        # print('              {}'.format(self.solution.to_string()))
        # print('              {}'.format(normalized_results))
        # print('       score: {}'.format(self.score))


class Result:
    def __init__(self, students, teams, questionaire, solution_document):
        self.students = students
        self.teams = teams
        self.questionaire = questionaire
        self.solution_document = solution_document
        self.student_results = {}
        self.team_results = {}

    def _parse_result_line(self, result, line_number, questionaire, filename, students):
        tokens = result.split("/")
        if len(tokens) != 3:
            tell(
                "The result string in line {} must consist of id/result/checksum.".format(
                    line_number
                ),
                "warn",
            )
            return None
        return ResultLine(
            tokens[0].strip(),
            tokens[1].strip(),
            tokens[2].strip(),
            line_number,
            questionaire,
            filename,
            students,
        )

    def load_results(self, file_input):
        lines = file_input.readlines()
        filename = file_input.name
        file_input.close()
        tell("Reading results file.")

        # initial --> preamble --> results
        state = "initial"
        line_number = 0
        preamble = []
        result_lines = []
        unique_ids = []
        for line in lines:
            line_number = line_number + 1
            if state == "initial":
                if line.startswith("---"):  # yaml preamble start
                    state = "preamble"
                else:
                    tell(
                        "Error in line {}: The results file needs a preamble, starting with ---.\nExample:\n---\nname: RAT1\ndate: 2018-06-28\n---".format(
                            line_number
                        )
                    )
                    return 0, 0
            elif state == "preamble":
                if line.startswith("---"):  # yaml preamble end
                    preamble = yaml.safe_load("\n".join(preamble))
                    # assign table to object
                    state = "results"
                else:
                    preamble.append(line)
            elif state == "results":
                # remove all whitespace and transform to lower case
                line = line.strip().lower().replace(" ", "")
                if not line:
                    # ignore empty lines
                    continue
                if line.startswith("#"):
                    # ignore, it's a comment
                    pass
                else:
                    result_line = self._parse_result_line(
                        line, line_number, self.questionaire, filename, self.students
                    )
                    if result_line is not None:
                        result_lines.append(result_line)
                        if result_line.result_id in unique_ids:
                            tell(
                                "Line {}: A line with the id {} already exists.".format(
                                    result_line.line_number, result_line.result_id
                                ),
                                "warn",
                            )
                        else:
                            unique_ids.append(result_line.result_id)
        # finished parsing the file

        if state != "results":
            tell("The results file is not complete.", "error")

        # check the preamble
        if "name" not in preamble:
            tell(
                "The results file should contain a name field in the preamble.", "warn"
            )
        else:
            self.name = preamble["name"]
        if "date" not in preamble:
            tell(
                "The results file should contain a date field in the preamble.", "warn"
            )
        else:
            self.date = preamble["date"]

        for result_line in result_lines:
            # check that student or team with matching id exists
            if self.students.exists(result_line.result_id):  # found student
                self.student_results[result_line.result_id] = result_line
                result_line.type = "student"
                solution = self.solution_document.get_student_solution(
                    result_line.result_id
                )
                if solution is None:
                    tell(
                        "Line {}: There exists no solution for student with id {}.".format(
                            result_line.line_number, result_line.result_id
                        ),
                        "error",
                    )
                else:
                    result_line.solution = solution
            elif self.teams.exists(result_line.result_id):  # found team
                self.team_results[result_line.result_id] = result_line
                result_line.type = "team"
                solution = self.solution_document.get_team_solution(
                    result_line.result_id
                )
                if solution is None:
                    tell(
                        "Line {}: There exists no solution for team with id {}.".format(
                            result_line.line_number, result_line.result_id
                        ),
                        "error",
                    )
                else:
                    result_line.solution = solution
            else:
                tell(
                    "Line {}: There exists no student or team with id {}.".format(
                        result_line.line_number, result_line.result_id
                    ),
                    "warn",
                )
            result_line.check()
        return len(self.student_results), len(self.team_results)

    def store_results(self, filename):
        result_table = []
        for student_id, result_line in self.student_results.items():
            if result_line.valid:
                team_id = self.students.get_team(student_id)
                team_percent = self.teams.get_rat_precentage(team_id)
                if team_id in self.team_results:
                    team_result = self.team_results[team_id]
                    team_score = team_result.score
                    answer_t = team_result.result
                    correct_t = self.solution_document.get_team_solution(
                        team_id
                    ).get_correct_answers_string()
                    total_score = (
                        team_percent * team_result.score
                        + (100 - team_percent) * result_line.score
                    ) / 100
                else:
                    team_score = None
                    answer_t = None
                    correct_t = None
                    total_score = result_line.score
                result_table.append(
                    {
                        "id": student_id,
                        "firstname": self.students.get_firstname(student_id),
                        "lastname": self.students.get_lastname(student_id),
                        "email": self.students.get_email(student_id),
                        "team": team_id,
                        "answer_i": result_line.result,
                        "correct_i": result_line.solution.get_correct_answers_string(),
                        "answer_t": answer_t,
                        "correct_t": correct_t,
                        "irat": result_line.score,
                        "pi": 100 - team_percent,
                        "trat": team_score,
                        "pt": team_percent,
                        "score": total_score,
                        "feedback": "",
                        "comment": "",
                    }
                )
        columns = [
            "id",
            "email",
            "lastname",
            "firstname",
            "team",
            "answer_i",
            "correct_i",
            "answer_t",
            "correct_t",
            "irat",
            "pi",
            "trat",
            "pt",
            "score",
            "feedback",
            "comment",
        ]
        result_table = pd.DataFrame(result_table)
        # TODO this can go wrong in case we have no entries?
        result_table = result_table[columns]
        result_table = result_table.set_index("id")
        result_table.to_excel(filename)
        tell("Stored results in file {}".format(filename))

    def store_results_html(self, filename):
        lines = []
        lines.append("<html><head>\n")
        lines.append(
            '<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">\n'
        )
        lines.append(
            '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-table/1.12.1/bootstrap-table.min.css">\n'
        )
        lines.append("</head><body>\n")

        lines.append(
            '<table class="table table-hover table-sm table-condensed" data-toggle="table">\n'
        )
        lines.append(
            '<thead class="thead-dark">\n<tr><th data-field="id" data-sortable="true">ID</th><th data-field="firstname" data-sortable="true">Firstname</th>'
        )
        lines.append(
            '<th data-field="lastname" data-sortable="true">Lastname</th><th data-field="email" data-sortable="true">Email</th><th data-field="team" data-sortable="true">Team</th><th data-field="score" data-sortable="true">Score</th>'
        )
        for question in range(1, 11):
            lines.append(
                '<th data-field="q{}" data-sortable="true">{}</th>'.format(
                    question, question
                )
            )
        lines.append("</thead>\n")
        for student_id, result_line in self.student_results.items():
            if not result_line.valid:
                continue
            team_id = self.students.get_team(student_id)
            team_percent = self.teams.get_rat_precentage(team_id)
            if team_id in self.team_results:
                team_result = self.team_results[team_id]
                team_score = team_result.score
                answer_t = team_result.result
                correct_t = self.solution_document.get_team_solution(
                    team_id
                ).get_correct_answers_string()
                total_score = (
                    team_percent * team_result.score
                    + (100 - team_percent) * result_line.score
                ) / 100
            else:
                team_score = None
                answer_t = None
                correct_t = None
                total_score = result_line.score
            lines.append(
                "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{:.1f}</td>".format(
                    student_id,
                    self.students.get_firstname(student_id),
                    self.students.get_lastname(student_id),
                    self.students.get_email(student_id),
                    team_id,
                    result_line.score,
                )
            )
            for question_number in range(1, len(result_line.normalized_results) + 1):
                # TODO allow flexible number of questions
                answer = result_line.normalized_results[question_number]
                lines.append("<td>{}</td>".format(answer))
            lines.append("</tr>\n")
        lines.append("</table>")
        lines.append("</body>")
        lines.append(
            '<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>'
        )
        lines.append(
            '<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>'
        )
        lines.append(
            '<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>'
        )
        lines.append(
            '<script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-table/1.12.1/bootstrap-table.min.js"></script>'
        )
        lines.append("</html>")
        with open(filename, "w", encoding="utf-8") as file:
            file.write("".join(lines))

    def stats(self, filename):
        def aggregate_results(results):

            df = pd.DataFrame(
                index=range(1, len(self.questionaire.questions) + 1),
                columns=["a", "b", "c", "d"],
            )
            df = df.fillna(0)
            for result in results:
                if result.valid:
                    for question in range(1, len(result.normalized_results) + 1):
                        answer = result.normalized_results[question]
                        if answer != "x":
                            df.loc[question, answer] += 1
            return df

        def truncate(data, max):
            return data[:max] + (data[max:] and "...")

        def print_question(number, text, scores, terminal_width):
            bar_width = terminal_width - 10
            fill = "█"
            print("")
            print(
                Style.BRIGHT
                + "     Q{}:".format(number)
                + Style.BRIGHT
                + " {}".format(truncate(text, bar_width - 10))
            )
            print(
                "  "
                + Style.NORMAL
                + "A: "
                + fill * int(scores[0] * bar_width / 100)
                + " {0:.1f}".format(scores[0])
            )
            for i in range(1, len(scores)):
                print(
                    "  "
                    + Style.DIM
                    + "{}: ".format(chr(65 + i))
                    + fill * int(scores[i] * bar_width / 100)
                    + " {0:.1f}".format(scores[i])
                )

        def print_in_console(df_i):
            # TODO get terminal width
            terminal_width = 125
            for index, row in df_i.iterrows():
                # row is a Series
                scores = row.copy() * 100 / row.sum()
                preview = self.questionaire.questions[int(index) - 1].question
                print_question(index, preview, scores, terminal_width)

        def print_question_html(number, question, scores):
            lines = []
            lines.append('<div class="card mt-5">')
            lines.append('    <div class="card-header">')
            lines.append("    <b>Question {}:</b> {}".format(number, question.question))
            lines.append("    </div>")
            lines.append('<ol class="list-group list-group-flush">')
            answers = question.get_answers()
            for i in range(0, len(scores)):
                if i == 0:
                    lines.append(
                        '<li class="list-group-item"><div>{} <small class="text-muted">(This is the best answer.)</small></div>'.format(
                            answers[i]
                        )
                    )
                    bar = "bg-success"
                else:
                    lines.append(
                        '<li class="list-group-item"><div>{}</div>'.format(answers[i])
                    )
                    bar = "bg-danger"
                lines.append('    <div class="progress">')
                lines.append(
                    '    <div class="progress-bar {}" role="progressbar" style="width: {:.1f}%">{:.1f}%</div>'.format(
                        bar, scores[i], scores[i]
                    )
                )
                lines.append("    </div>")
                lines.append("</li>")
            lines.append("</div>")
            return "\n".join(lines)

        def print_html(df_i):
            lines = []
            lines.append("<html><head>")
            lines.append(
                '<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">'
            )
            lines.append(
                '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-table/1.12.1/bootstrap-table.min.css">'
            )
            lines.append("</head><body>")
            lines.append('<div class="container" role="main">')
            for index, row in df_i.iterrows():
                # row is a Series
                scores = row.copy() * 100 / row.sum()
                question = self.questionaire.questions[int(index) - 1]
                lines.append(print_question_html(index, question, scores))
            lines.append("</div>")
            lines.append("</body>")
            lines.append(
                '<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>'
            )
            lines.append(
                '<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>'
            )
            lines.append(
                '<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>'
            )
            lines.append(
                '<script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-table/1.12.1/bootstrap-table.min.js"></script>'
            )
            lines.append("</html>")
            with open(filename, "w", encoding="utf-8") as file:
                file.write("\n".join(lines))

        df_i = aggregate_results(self.student_results.values())
        df_t = aggregate_results(self.team_results.values())

        print_in_console(df_i)
        print_html(df_i)


# if __name__ == '__main__':
#    test()


class Teampy:
    def __init__(self):
        self.load_context()

    def get_teams(self):
        return self.teams

    def load_scratch_cards(self, filename):
        rawcodes = yaml.safe_load(open(filename, "r", encoding="utf-8"))
        codes = {}
        for key in rawcodes:
            codes[key] = Solution.create_solution_from_string(
                rawcodes[key], card_id=key
            )
        return codes

    def load_smtp_settings(self, filename):
        settings = yaml.safe_load(open(filename, "r", encoding="utf-8"))
        if "from" not in settings:
            tell(
                'The smtp settings need to include attribute "from" with your email.',
                "error",
            )
            # TODO check if 'from' is a valid email, at least syntactically
            return None
        if "smtp" not in settings:
            tell(
                'The smtp settings need to include attribute "smtp" with the address of your SMTP server.',
                "error",
            )
            return None
        if "port" not in settings:
            tell(
                'The smtp settings need to include attribute "port" with the port number of your SMTP server.',
                "error",
            )
            return None
        return settings

    def find_main_directory(self):
        # look in the current working directory
        dirs = [os.getcwd(), os.path.dirname(os.getcwd())]
        for directory in dirs:
            student_file = os.path.join(directory, "students.xlsx")
            if os.path.isfile(student_file):
                return directory
        return None

    def load_context(self):
        directory = self.find_main_directory()
        if directory is None:
            tell("Could not find the students file.", level="error")
            quit()

        students_file = os.path.join(directory, "students.xlsx")
        self.students = Students(students_file)
        # check if student ids are unique
        s = set()
        duplicates = set(
            x for x in list(self.students.df.index.values) if x in s or s.add(x)
        )
        if len(duplicates) > 0:
            tell(
                "The ids of some students are not unique. Check {}".format(duplicates),
                level="error",
            )
            quit()

        teams_file = os.path.join(directory, "teams.xlsx")
        if os.path.isfile(teams_file):
            self.teams = Teams.from_excel(teams_file)
        else:
            self.teams = Teams.from_students(self.students)

        self.scratchcards = {}
        scratchcards_file = os.path.join(directory, "scratchcards.txt")
        if os.path.isfile(scratchcards_file):
            tell("Reading the scratchcards file.")
            self.scratchcards = self.load_scratch_cards(scratchcards_file)

        self.smtp_settings = None
        smtp_settings_file = os.path.join(directory, "smtp.txt")
        if os.path.isfile(smtp_settings_file):
            tell("Reading the smtp settings file.")
            self.smtp_settings = self.load_smtp_settings(smtp_settings_file)


class RATContext:
    def __init__(self, teampy):
        self.teampy = teampy
        directory = os.getcwd()
        self.questionaire_file = os.path.join(directory, "questions.txt")
        self.solutions_file = os.path.join(directory, "solutions.teampy")
