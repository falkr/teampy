---
---

# Grade RATs

To rate the RATs, you need to prepare a file that lists all the individual and the
team results.

File `results.txt`:

    ---
    name: RAT1
    date: 2018-06-28
    ---
    va2/bbabcdacbb/2521
    am1/dacadcddca/3034
    ls1/ddabcbbabd/2413
    ...
    7/badcdadcba/10
    8/bddcdadcba/9

The individual results are listed with the student id, the results and the check
sum. The team results are listed with the id of the team, the results, and a simplified check sum that is better suited for the scratch cards.

* Empty lines are ignored, so you can use empty lines to group entries if you like.
* Capitalization is ignored, all entries (student and team ids, results) are converted into lowercase when the file is read in.
* Whitespace within a line is also removed.
* All results need to have the proper length. That means, if the RAT has 10 questions, then all result string need to be 10 letters long. If a student did not answer a question, write an `x` for that letter instead.
* If a team uses scratch cards and opens more than one scratch field, write the first wrong answer they selected in the sequence.

Run Teampy with the following command:

    rat grade results.txt

We assume here that you are in the directory of the RAT, and that `questions.md` is the name of your RAT file.
Teampy will create an Excel file with the grades for each student.


## Several RAT Sessions

Often, there is more than one instant in time when students do the RAT.
You can cover this by creating different result files, each one only including
results for a subset of students.

## Statistics

Teampy prints an overview of the questions and answers given.
It shows questions and answer alternatives in the sequence you wrote them in the
questions.txt file, so that 'A' is the best answer alternative.

    Q1: What defines a fruit?
    A: ████████████████████████████████████████████████████████████████████████████████████████████████████ 87.3
    B: ██████████ 9.5
    C:  0.0
    D: ███ 3.2

    Q2: Which of the is not a fruit?
    A: ███████████████████████████████████████████████████████████████████████ 61.9
    B: ███████ 6.3
    C: ████████████████ 14.3
    D: ████████████████████ 17.5
