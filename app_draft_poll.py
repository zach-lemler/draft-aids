
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

from flask import Flask
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)


class DraftPoll(Resource):
    def put(self, draft_id):
        drafted=[]
        
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration
        options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
        options.add_argument('--no-sandbox')  # Bypass OS security model
        options.add_argument('--disable-web-security')  # Disable web security
        options.add_argument('--allow-running-insecure-content')  # Allow running insecure content
        options.add_argument('--disable-webrtc')  # Disable WebRTC
        options.add_argument("headless")
        driver = webdriver.Chrome(options=options)
        try:
            # Open a web page
            driver.get(f"https://sleeper.com/draft/nfl/{draft_id}")
            time.sleep(2)
            drafted_elements = driver.find_elements(By.CLASS_NAME, "avatar-player")

            drafted = []
            for i in drafted_elements:
                drafted_id = str(i.accessible_name).replace('nfl Player ', '')
                try:
                    drafted_id = int(drafted_id)
                    drafted.append(drafted_id)
                except:
                    pass

            driver.close()
        except:
            driver.close()
            drafted = []
            
        with open('db/drafted.txt', 'w') as f:
            for line in drafted:
                f.write(f"{line}\n")

api.add_resource(DraftPoll, '/draft-poll/<draft_id>')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
    

