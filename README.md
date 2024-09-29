# LinkedIn-outreach
Auto outreach to LinkedIn members with a customised message 

Selenium based python script to automate sending connection requests to LinkedIn profiles with a customised message.

Pre-requisites:
  Google Chrome: https://www.google.com/intl/en_uk/chrome/dr/download/?brand=GBSK&ds_kid=43700079594422203
  Python: https://www.python.org/downloads/
      Check: command -v python3
  Python libraries
      Check: pip show pandas; pip show selenium;
  Chromedriver: https://developer.chrome.com/docs/chromedriver/downloads
      Check: command -v chromedriver


Inputs: 
  outreach.csv -> List of linkedin profile URLs, messages, emails (some profiles need email to send connection request)
  Terminal command "python3 outreach.py"

Outputs:
  Chrome based LinkedIn login -> Serially hitting URLs, navigating profile page, sending connection request with email/message attached
  outreach.csv -> Populated with final status for each profile
  outreach.logs -> Detailed logs on step by step execution for better debugging
