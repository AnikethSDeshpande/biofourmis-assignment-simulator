# Biofourmis Assignment 14327

##### Backend Table Requirement
* Write a *__simulator__* to generate random values of hear_rate, resp_rate and activity every second
in increasing order of unix timestamp (epoch). It will then pass every value one by one to the
processor function.
* Then write a *__processor__* function code which would update the pandas dataframe after every
new second value comes to it. Basically seg_start and seg_end are 15 mins segments of UTC
hour. So every UTC hour, there are four 15 mins segments for which avg, min, max should be
calculated.

##### Execution Steps
* ``` pip install -r requirements.txt```
* Run the command ```python3 execute.py```
* On completion of the execution, the required report would be available in reports directory.