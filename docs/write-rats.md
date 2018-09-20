---
---

# Write RATs

You write a RAT as a text file with some few elements for marking questions and correct answers.
Below is an example of a RAT showing a single question with four answers.

    ---
    title: "RAT 1: Fruits and Vegetables"
    ---

    #

    Which of the following is a fruit?

    ![](figures/fruits.pdf)

    {1} true: A banana is a fruit.
    {2} fake: Salad is a fruit.
    {3} fake: Potatoes are fruits.
    {4} fake: Cucumbers are fruits.

    #

    Another question...

As you can see, **the correct answer is always the first one.**
We will shuffle the answers once we print them.
This also means that you need to formulate the answer alternatives so that they
make sense independent of their sequence.

* The file contains a preamble (between the two lines starting with `---`) that
defines the title of the RAT, like here *Fruits and Vegetables*.
* Each new question is introduced with a line that starts with a `#`.
* The question can be several lines of text.
* The answer alternatives are given with the prefix `{1} true: ` resp. `{n} fake: `.
* Within each RAT, all question must have the same number of answer alternatives.


## Figures

A question can include a figure, using the following code:

    ![](figures/fruits.pdf)

The image should be contained in a folder `figures`, and the types can be PDF, JPG or PNG.
(With LaTeX creating the final document, PDF with vector graphics is often the best option.)

## Current Constraints

* There must always be **four** answer alternatives.
* Text is transformed into LaTeX as it is written, i.e., Markdown or other letters are not translated.
* A question can have **at most one figure**.


## Filenames

The RAT files should be stored in their own folder, so that Teampy creates other files around the question file. Below is an illustration of the file structure:

- course/
    - **students.xlsx**
    - **teams.xlsx**
    - **scratchcards.txt**
    - rat-01/
        - **questions.txt**
        - solutions.teampy
        - results-1.txt
        - receipts/
            - aa1.pdf
            - aa2.pdf
        - figures/
            - banana.pdf

## Encoding

When you store the RAT file, your editor will use an encoding for the characters.
If you write in plain English, ASCII or UTF-8 will work fine, but if you want to use other characters,
choose **ISO-Latin-1** or **ISO-Latin-9**.


## Checking RATs

At any time, you can use Teampy to check the RAT file and create LaTeX from it so you can see if all works.
To do so, run the following command in the command line:

    rat check questions.txt

We assume here that you are in the directory of the RAT, and that `questions.txt` is the name of your RAT file.
The `rat check` command does not require that your students file exists, and it does not require you to select a scratch card for the solution.
It just creates a LaTeX file with the questions in their original order and with the correct answer sorted first.


## Testing a RAT with a Colleague

Usually it is a good idea to test your RAT with a colleague, which means that they receive a copy of the RAT with 
shuffled answer alternatives so they have to think about the right answer. 
For this, use the command

    rat trial questions.txt

The resulting file prints one copy of the RAT, but shuffles the answers randomly. 
You don't need to have a `students.xlsx` file, which means you can test your RATs also before the semester has started.