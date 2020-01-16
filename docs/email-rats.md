---
---

# Send RAT Feedback via Email

You can send an email to each student that shows their RAT score. 
The email is sent via SMTP from your own email account, so that students may also respond.

Use the following command:

    rat email results.xlsx

The results file is the one Teampy created when grading the RAT. 
This also means it only sends an email to the students that participated in that specific RAT.

You can specify with the flag `--testonly` that Teampy is just storing HTML files that contain the email contents in a folder called *emails*. 

    rat email results.xlsx --testonly

In this way you can have a look at the email before anything is sent out.


## About Sending Email

The connection to the server is protected via TLS, and Teampy prompts each time for your password, but does not store it.

Depending on the email system you use, you will not see the mail in your folder with sent items.

Teampy will modify the results file, and write in the column `feedback` if it succeeded to send the email to the specific student. 
The field will then say `sent`. 
In case some emails could not be sent, Teampy will try to tell you the reason. 
You can then run the command again:

    rat email results.xlsx

Teampy will then try to send the email to all students that have not yet an `sent` in the `feedback` column. 