# Draft Aids

## Usage

run tiers_daddy.py to scrape rankings and create tiers  
in db/players.csv there is a my_guys column  
Add anything to the column for any player you want tracked  

run app_daddy.py and app_draft_poll.py  
open browser and got to http://127.0.0.1:8050/   

copying your draft id from the sleeper draft url will live track your draft  
selecting a position will filter just the bar graph based on that selection  
rankings names across the top are a multiselect and will show an aggregated ranking for all sites chosen  

the value table will change color based on how close the pick is to happening  
green 12 or less picks away  
yellow 24 - 13 picks away  
red more than 24 picks away  
the pick column is the actual number of picks away they are  
players that populate this table are ones that your selected rankings value at least half a round higher than Sleeper ADP  


example batch file to start both apps  

@echo off  

start F:\path\to\python\python.exe .\app_daddy.py  
start  F:\path\to\python\python.exe .\app_draft_poll.py  


## Set Up 

Google Chrome required  
Find your Chrome version in settings/About Chrome  
Download the matching chromedriver version from https://googlechromelabs.github.io/chrome-for-testing/  
paste the extracted files in the draft-aids folder  

Download python  

Install required libraries from requirements.txt  
python -m pip install -r path/to/requirements.txt    



## why selenium for picks 

because Sleeper's draft pick API currenlty takes 5 minutes + to refresh
