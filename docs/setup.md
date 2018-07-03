---
---

# Course Setup

Teampy expects the following file and folder structure:

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


Type the following command:

    python teams create


Teampy will create a folder for your course and template files for the students
and the teams.

## Students File

The students file is an Excel file with a table that has the following columns:

* id
* email
* lastname
* firstname
* team
* table

## Teams File

The teams file is an Excel file with the following columns:

* id
* name
