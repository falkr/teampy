---
---

# Course Setup

Teampy expects the following file and folder structure:

- course/
    - **students.xlsx**
    - **teams.xlsx**
    - **scratchcards.txt**
    - **smtp.txt**
    - rat-01/
        - **questions.txt**
        - solutions.teampy
        - **results-1.txt**
        - **results-1.xlsx**
        - receipts/
            - aa1.pdf
            - aa2.pdf


The top-level folder, here called *course* is a folder of your choice,
usually a unique folder for your specific course and year.
An example would be `ttm4115-2018`.

## Students File

The students file is an Excel file with the name `students.xlsx` with a table that has the following columns:

|  id | email | lastname | firstname | team | table |
| --- | ----- | -------- | --------- | ---- | ----- |
| ab1 | a@example.org | Berg | Anna  | 14   |     7 |
| ... | ...   | ...      | ...       | ...  | ...   |

The id for a student should be a short, unique identifier.
It must not be the same as the identifier for a team.
We propose to use a pattern `ab1`, where the first letter is the first letter
of the student's first name, the second letter the first letter of the students last name.
The number is used to make the identifiers unique.

Example: A student named Kari Nordman gets the id `kn1`. Another student with the
same initials gets the id `kn2`.

The table can contain a column `table` that lists the tables where everyone sits
during the RAT. This is later useful when the RATs are printed.
They can be sorted according to the table and distributing them is fast and simple.

## Teams File

The teams file is an Excel file with the name `teams.xlsx` with the following columns:

|  id | name   |  pt | 
| --- | ------ | --- | 
|  14 | A-Team |  30 | 
| ... |  ...   | ... | 

- The **ids** are the same ids that are used in the students file to assign a student to a team.
- The **names** can be the team names that students selected for their team. They have no technical significance, but Teampy can show them for instance in emails. 
- The **pt** column determines for each team how much the team RAT should count to the total score. You can decide on your own if you give teams the choice for this, or if you assign the same percentage to each team. In the example above, the team rat counts 30% to the total RAT score, the remaining 70% are the individual RAT score. In case you assign the same percentage to all teams, just write 
the same value into the rows for all teams.

The teams file is optional.

## Scratch Cards File

The scratch cards file is optional. In this file, you can store solution patterns
of scratch cards that you have on stock and that you use throughout the semester.
Often, these cards have a short code (like *F017*) that identifies a specific solution pattern.
When you store these codes in the file, you can simply select the code when you print
RATs, instead of writing the entire solution.

The file simply contains one code in each line, separated with a colon.

    F017: a b d c d b c a d d
    F018: a d c b a d b b d c
    ...

The name of the file must be `scratchcards.txt'.

## Readiness Assurance Tests (RATs)

Each RAT is stored in a separate folder, containing several files for each of them. 


## SMTP Settings

If you want to send the results of each RAT to your students, you need to configure 
a file with the SMTP settings of your email server. 
You can check the settings of your local email client (if it uses SMTP), or contact your IT support.

The file should look like this, obviously with the values changed to your settings:

    from: kraemer@ntnu.no
    smtp: smtp.ansatt.ntnu.no
    port: 587


## Backups

Teampy is written to be careful with your data. It distinguishes between files that are written by you, and files it generates. Still, backing up data is good practice anyway. 
Please always keep regular backups of your data. The files Teampy uses are relatively small even for large courses, so that you also can keep several backups over time.
