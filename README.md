# Draft Aids


## Usage


Run tiers_daddy.py to scrape rankings and create tiers  
In db/players.csv there is a my_guys column  
Add anything to the column for any player you want tracked  

Run app_daddy.py and app_draft_poll.py  
Open browser and got to http://127.0.0.1:8050/   

Copying your draft id from the sleeper draft url will live track your draft  
Selecting a position will filter just the bar graph based on that selection  
Rankings names across the top are a multiselect and will show an aggregated ranking for all sites chosen  

The value table will change color based on how close the pick is to happening  
  Green 12 or less picks away  
  Yellow 24 - 13 picks away  
  Red more than 24 picks away  
The pick column is the actual number of picks away they are  
Players that populate this table are ones that your selected rankings value at least half a round higher than Sleeper ADP  



## Set Up 


Google Chrome required  
Find your Chrome version in settings/About Chrome  
Download the matching chromedriver version from https://googlechromelabs.github.io/chrome-for-testing/  
Paste the extracted files in the draft-aids folder  

Download python  

Install required libraries from requirements.txt  
python -m pip install -r path/to/requirements.txt    


For easier start up you can make a batch script calling both apps
@echo off  
start F:\path\to\python\python.exe .\app_daddy.py  
start  F:\path\to\python\python.exe .\app_draft_poll.py  



## why selenium for picks 


Because Sleeper's draft pick API currenlty takes 5 minutes + to refresh
