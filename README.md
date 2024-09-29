# LinkedIn-outreach
Auto outreach to LinkedIn members with a customised message 

Selenium based python script to automate sending connection requests to LinkedIn profiles with a customised message.

**Pre-requisites:** <br/>
  &emsp;• Google Chrome: <br/> &emsp;&emsp;https://www.google.com/intl/en_uk/chrome/dr/download/?brand=GBSK&ds_kid=43700079594422203<br/>
  &emsp;• Python: <br/> &emsp;&emsp;https://www.python.org/downloads/<br/>
      &emsp;&emsp; Check: command -v python3<br/>
  &emsp;• Python libraries<br/>
      &emsp;&emsp;Check: pip show pandas; pip show selenium;<br/>
  &emsp;• Chromedriver: <br/> &emsp;&emsp;https://developer.chrome.com/docs/chromedriver/downloads<br/>
      &emsp;&emsp;Check: command -v chromedriver<br/>


**Inputs:** <br/>
  &nbsp;&nbsp;• outreach.csv -> List of linkedin profile URLs, messages, emails (some profiles need email to send connection request) <br/>
  &nbsp;&nbsp;• Terminal command "python3 outreach.py"

**Outputs:** <br/>
  &nbsp;&nbsp;• Chrome based LinkedIn login -> Serially hitting URLs, navigating profile page, sending connection request with email/message attached<br/>
  &nbsp;&nbsp;• outreach.csv -> Populated with final status for each profile<br/>
  &nbsp;&nbsp;• outreach.logs -> Detailed logs on step by step execution for better debugging
