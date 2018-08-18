---
---

# Grade RATs

To rate the RATs, you need to prepare a file that lists all the individual and the
team results.

rat01.results:

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




    rat rate

We assume here that you are in the directory of the RAT, and that `questions.md` is the name of your RAT file.

The `rat check` command does not require that your students file exists. The RAT is printed
