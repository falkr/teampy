---
---

# RAT Questions


A RAT is written as a textfile with some few elements for marking questions and correct answers.
Below is an example of a quiz with a question and four answers.

    ---
    title: "RAT 1: Fruits and Vegetables"
    ---

    #

    Which of the following is a fruit?

    {1} true: A banana is a fruit.
    {2} fake: Salad is a fruit.
    {3} fake: Potatoes are fruits.
    {4} fake: Cucumbers are fruits.

    #

    Another question...


* The file contains a preamble (between the two lines starting with `---`) that
defines the title of the RAT, like here *Fruits and Vegetables*.
* Each new question is introduced with a line that starts with a `#`.
* The question can be several lines of text.
* The answer alternatives are given with the prefix `{1} true: ` resp. `{n} fake: `.
* It is important that there is only **one** true answer, and that it is declared as **first** one.
* Within each RAT, all question must have the same number of answer alternatives.

**Current constraints:**

* There must always be **four** answer alternatives.
* Text is transformed into LaTeX as it is written, i.e., markdown or other letters are not escaped.


## Filenames

The RAT files should be stored in their own folder, so that Teampy creates other files around the question file. Below is an illustration of the file structure: 

- course
    - **students.xlsx**
    - **teams.xlsx**
    - rat-01/
        - **questions.md**
        - solutions.xlsx
        - results1.txt
        - results1.xlsx
        - results2.xlsx
        - receipts
            - aa1.pdf
            - aa2.pdf
