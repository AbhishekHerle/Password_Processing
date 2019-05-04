Short set of APIs for processing password dumps in python using the Django framework. This project uses Grok patterns (using the PyGrok library) to search for passwords in password dumps and then retrieve user passwords as well as other well as other associated user information such as usernames, email addresses and so. 

It has two APIs, both HTTP post requests.
 1) http://127.0.0.1:8000/PP/processor/getSample/ - Requests contain the following:
    a) "N": Number of lines to fetch from the password dump.
    b) file_name": Name/path of the password dump to be processed
    c) "sampleType": "random", "last" or "first". Option to fetch N random, last or first lines.
    ![getSample](https://github.com/AbhishekHerle/Samplecode/blob/master/getSample.PNG)
    
 2) http://127.0.0.1:8000/PP/processor/doProcessing/ - Requests contain the following:
    a) "file_name": Name/path of the password dump to be processed
    b) "patterns": List of GROK patterns to be applied to the password dump
    ![doProcessing](https://github.com/AbhishekHerle/Samplecode/blob/master/doProcessing.PNG)

Primary aim is to use the getSample API to peek into the file and then determine the sort of GROK patterns that will fit the need.
