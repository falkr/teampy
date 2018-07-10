---
---

# Teampy: Tools for Team-Based Learning

This is a set of Python scripts to manage readiness assurance tests for
team-based learning.

In detail, Teampy helps you with the following:

Manage *paper-based* readiness assurance tests (RATs):

* Write your RAT in a simple textual format, in any text editor of your choice.
* Convert the raw RATs into LaTeX, from which you can generate PDF.
* Teampy shuffles the questions and answers for each student, so that cheating is a bit harder.
* Collect the answers by documenting a single line of text for each student.
* Look at the results of a class to give feedback to students.
* Send individual results to each student via your own email.


## Current Project Status

The project is in an early stage, and not all features are in place yet.


## Installation

Teampy only requires that you have [Python 3.x](https://www.python.org) installed.
Make sure that you let the installer add the Python command line tools to your path,
so that you can later execute the pip command and the other commands that Teampy comes with.

After Python is installed, you can install Teampy via pip:

    pip install teampy

To upgrade, use:

    pip install --upgrade teampy

Pip will install several command line tools. If your command line does not recognize
the pip command, make sure the Python installer added them to the path.

## Usage

### At Semester Start

* [Course Setup](setup.html)
* ~~Assign Student IDs~~ (not supported yet)
* ~~Shuffle Teams~~ (not supported yet)

### During the Semester

* [Write RATs](write-rats.html)
* [Print RATs](print-rats.html)
* Evaluate RATs
* Send Feedback to students

### At the End of the Semester

* Summarize RAT results



## For Developers

* Teampy is open source. You can [browse the source code on Github](https://github.com/falkr/teampy),
fork it or contribute via pull requests.
* [Browse the API here.](./teams/index.html)
