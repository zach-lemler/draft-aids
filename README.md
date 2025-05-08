# Draft Aids

--- usage ---

run tiers_daddy.py to scrape rankings and create tiers  
in db/players.csv there is a my_guys column  
Adding anything to the column for any player you want tracked  

run app_daddy.py and app_draft_poll.py  
open browser and got to http://127.0.0.1:8050/   

copying your draft id from the sleeper draft url will live track your draft  
selecting a position will filter just the bar graph based on that selection  
rankings names across the top are a multiselect and will show an aggregated ranking for all sites chosen  



example of batch file to start both app_daddy.py and app_draft_poll.py  

@echo off  
start /B F:\path\to\python\python.exe .\app_daddy.py  
start /B F:\path\to\python\python.exe .\app_draft_poll.py  



--- set up ---

Google Chrome required  
Find your Chrome version in settings/About Chrome  
Download the matching chromedriver version from https://googlechromelabs.github.io/chrome-for-testing/  
paste the extracted files in the draft-aids folder  

Download python  

Install required libraries from requirements.txt  
python -m pip install -r path/to/requirements.txt  
