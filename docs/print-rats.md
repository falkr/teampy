---
---

# Print RATs

When you print a RAT, Teampy creates a shuffled version of the questions for
each student, and shuffles the answers for the teams so that they match any
scratch cards that you may want to use.

    rat print -teamsolution abcdabcdab rat01.md

If you have defined the solutions of existing scratch cards in the [scratch cards file](setup.html), you just give the code of the scratch card:

    rat print -teamsolution D013 rat01.md

The result of this operation are two files:

* The file `rat01.tex`. This is a LaTeX file that you should translate into PDF with your LaTeX tools.
* The file 'rat01.solutions'. This file contains the correct solution for each team and student. Teampy needs this file later when the RATs are evaluated, so do not delete this file.
