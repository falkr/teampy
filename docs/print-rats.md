---
---

# Print RATs

When you print a RAT, Teampy creates a shuffled version of the questions for
each student, and shuffles the answers for the teams so that they match any
scratch cards that you may want to use.

    rat print -teamsolution abcdabcdab rat01.md

If you have defined the solutions of existing scratch cards in the [scratch cards file](setup.html), you just give the code of the scratch card:

    rat print -teamsolution D013 rat01.md
