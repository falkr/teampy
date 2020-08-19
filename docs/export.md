---
---


# Export


## Exporting to Blackboard

You can export a RAT so that you can [import it in Blackboard as a test](blackboard.html).

    rat export --format blackboard questions.txt

In this format, the correct answer is always listed first since Blackboard shuffles answer alternatives on its own.

## Exporting to Supermark

You can export a RAT so that you can import it in [Supermark](https://falkr.github.io/supermark/) documents.

    rat export --format supermark --teamsolution abcdabcdab questions.txt

For this export, you need to provide the solution string to shuffle the answer alternatives. 