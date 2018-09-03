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
* All results need to have the proper length. That means, if the RAT has 10 questions, then all result string need to be 10 letters long. If a student did not answer a question, write an `x` for that answer instead.
* If a team uses scratch cards and opens more than one scratch field, write the first wrong answer they selected in the sequence.

Make sure you are in the folder of the rat, where also the files `questions.txt` and `solutions.teampy` are stored.
Run Teampy with the following command:

    rat grade results.txt

Teampy will create an Excel file `results.xlsx` with the grades for each student.


## Several RAT Sessions

In case you want to let students do the RATs in different sessions (for instance for students that could not attend the regular RAT), you can store results in several files, like `results-1.txt` and `results-2.txt`, and include in each file only the results of the students taking the RAT then and there.


## Team and Individual Results

The results file includes both individual and team results of the specific RAT session. 
Teampy assumes that all students in a result file also get the team results that are recorded in that file and that correspond to the team that Teampy had registered in the students.xlsx files at that time.

This also means, if you offer a RAT as a repetition to students that could not take the RAT during normal class time, and they did not participate in a team RAT, simply don't include any team result in the result file for that session.


## Manual Adjustments

In case you want to correct faulty questions or otherwise change the results manually, you can do so in the file `results.xslx`. You can change the data in any column, or add a comment in the `comment` column. The email later sent to students contains all information in the columns, including the comment. 
Note, however, that Teampy does not recalculate any scores. I.e., if you only change the result delivered by the student, for instance, the individual score and the total score are not changed. 
You have to change them accordingly.

In case you do manual adjustment, note that if you run the `rat grade` command again on the file, your adjustments will be overwritten. (Usually running that command more than once is not useful anyways.)


## Statistics

Teampy prints an overview of the questions and answers given.
It shows questions and answer alternatives in the sequence you wrote them in the
questions.txt file, so that 'A' is the best answer alternative.

    Q1: What defines a fruit?
    A: ████████████████████████████████████████████████████████████████████████████████████████████████████ 87.3
    B: ██████████ 9.5
    C:  0.0
    D: ███ 3.2

    Q2: Which of the following is not a fruit?
    A: ███████████████████████████████████████████████████████████████████████ 61.9
    B: ███████ 6.3
    C: ████████████████ 14.3
    D: ████████████████████ 17.5
