# Import Teampy RAT into Blackboard



## Exporting from Teampy

You can export a RAT so that you can [import it in Blackboard as a test](blackboard.html).

    rat export --format blackboard --solution abcdabcdab questions.txt

You need to provide the solution string to shuffle the answer alternatives. 
The result is a file called **blackboard.txt**

## Creating a Test on Blackboard

1. Create a new Assessment and select Test
2. Create a new Test
3. Give a name for the Test
4. Select **Upload Questions**, and select the file you created above. Click **Submit**.
5. Check the imported questions. Check also if the correct answer alternative is marked as the correct one. Click **OK**.
6. Back in Test page, confirm with **Submit**.
7. Edit the test availability and due date if you want to restrict the timeslot to prepare the test. 
8. **Remove any feedback after the submission**, since students should go into the team RAT without knowing their score.
9. In Test Presentation, select **All at once**, and **Randomize Questions**
10. Click **Submit** to confirm. 