---
---

# Send RAT Feedback via Email

You can send an email to each student that shows their RAT score. 
The email is sent via SMTP from your own email account, so that students may also respond.

Use the following command:

    rat email results.xlsx

The results file is the one Teampy created when grading the RAT. 
This also means it only sends an email to the students that participated in that specific RAT.




## About Sending Email

The connection to the server is protected via TLS, and Teampy prompts each time for your password, but does not store it.

Depending on the email system you use, you will not see the mail in your folder with sent items.

Teampy will modify the results file, and write in the column `feedback` if it succeeded to send the email to the specific student. 
The field will then say `ok'. 
In case some emails could not be sent, Teampy will try to tell you the reason. 
You can then run the command again:

    rat email results.xlsx

Teampy will then try to send the email to all students that have not yet an `ok` in the `feedback` column. 