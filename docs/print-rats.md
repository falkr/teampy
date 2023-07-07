---
---

# Print RATs

When you print a RAT, Teampy creates a shuffled version of the questions for
each student, and provides each team with a unique solution.

    rat print questions.txt

If you want to use a specific solution for all teams, provide it using the following option:

    rat print --teamsolution abcdabcdab questions.txt

If you have defined the solutions of existing scratch cards in the [scratch cards file](setup.html), you just give the code of the scratch card:

    rat print --teamsolution D013 questions.txt

The result of this operation are two files:

* The file `questions.pdf` with the quizzes ready for printing. If you use the command line option `--nopdf`, Teampy creates a *.tex file instead that you can translate with LaTeX.
* The file `solutions.teampy`. This file contains the correct solution for each team and student. Teampy needs this file later when the RATs are evaluated, so **do not delete this file.**


## Only Printing Team RATs

In case you only need to print the RATs for teams and not the individual students, use option `--teamsonly`.