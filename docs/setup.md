---
---

# Course Setup

Teampy expects the following file and folder structure:

    - course/
        - **students.xlsx**
        - **teams.xlsx**
        - rat-01/
            - **questions.md**
            - solutions.xlsx
            - results1.txt
            - results1.xlsx
            - results2.xlsx
            - receipts/
                - aa1.pdf
                - aa2.pdf


The top-level folder, here called *course* is a folder of your choice,
usually a unique folder for your specific course and year.
An example would be `ttm4115-2018`.

## Students File

The students file is an Excel file with the name `students.xlsx` with a table that has the following columns:

* id
* email
* lastname
* firstname
* team
* table

The id for a student should be a short, unique identifier.
It must not be the same as the identifier for a team.
We propose to use a pattern `ab1`, where the first letter is the first letter
of the student's firstname, the second letter the first letter of the students lastname.
The number is used to make the identifiers unique.

Example: A student named Kari Nordman gets the id `kn1`. Another student with the
same initials gets the id `kn2`.

The table can contain a column `table` that lists the tables where everyone sits
during the RAT. This is later useful when the RATs are printed.
They can be sorted according to the table and distributing them is fast and simple.

## Teams File

The teams file is an Excel file with the name `teams.xlsx` with the following columns:

* id
* name

The ids are the same ids that are used in the students file to assign a student to a team.
