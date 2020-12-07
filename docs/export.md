---
---


# Export


## Exporting to Blackboard

You can export a RAT so that you can [import it in Blackboard as a test](blackboard.html).

    rat export --format blackboard --solution abcdabcdab questions.txt

You need to provide the solution string to shuffle the answer alternatives. 



## Exporting to Supermark

You can export a RAT so that you can import it in [Supermark](https://falkr.github.io/supermark/) documents.

    rat export --format supermark --solution abcdabcdab questions.txt

You need to provide the solution string to shuffle the answer alternatives. 


## Exporting to PDF

You can export a RAT so that you can use it as a simple PDF file with randomized answers.

    rat export --format pdf --solution abcdabcdab questions.txt

You need to provide the solution string to shuffle the answer alternatives. 
