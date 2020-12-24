# Google_Cloud_Function_Log_Extractor

### Description of Python files:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**ret.py** - contains the logic of API calls and stores whichever functions have completed, running, did not run. (Remove this logic from ret.py and instead implement it inside the index.html)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**test.py** - contains the logic of extracting the config details and host the server.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**/templates/index.html** - Front end for the user.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**temp.py** - You can try playing with the code with temp.py. It is a temporary code that makes the API calls.


<br />
<br />
<br />


  
### Few functionalities that are remaining to be implemented in the future are:



&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.  Create FILTER for tag, module_name, sm_name for extracting only specific logs. Also extract logs that have "Function execution started" and "function took x milliseconds".

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. Auto Refresh functionality - Extract logs after every "frequency" number of seconds.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3. CSV Export - I have partially implemented this functionality but facing some issues. Hope this can be resolved easily. :D

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4. Try logging_v2 API for extracting logs to check if it is fast enough to retrieve the logs.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;5. Support Multiple user - The same URL should be accessible to multiple user and should aid multiple users the same way as it supports a single one without any interference to other users.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;6. Colourise the Function_names buttons based on reading the logs present inside the textField rather than the logic written inside the API call list_entries() inside ret.py.

