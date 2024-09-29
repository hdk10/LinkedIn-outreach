#!/usr/bin/env python
# coding: utf-8

# In[158]:


import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import sys
import time
import logging

# Setup logging to file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("outreach_logs.txt"),
        logging.StreamHandler()
    ]
)

# In[154]:


data = pd.read_csv('./outreach.csv')
# Add a new column for Status to track success/failure
data['Status'] = 'Pending'
# Read URLs and messages from csv
urls = data['URL']
messages = data['Message']
emails = data['Email']
data=data.reset_index()
# In[117]:


options = webdriver.ChromeOptions()
options.add_argument("--start-fullscreen") 
driver = webdriver.Chrome(options=options)

# Open LinkedIn and wait for the user to sign in
driver.get("https://www.linkedin.com/login")
WebDriverWait(driver, 300).until(EC.url_contains("https://www.linkedin.com/feed"))

# In[156]:


logging.info(" <-- Campaign Logs -->")
logging.info("")
for index, url in enumerate(urls):
    logging.info(f"Attempting {url}")
    msg = data['Message'][index]
    email = data['Email'][index]

    try:
        driver.get(url)
        logging.info("- - Page loaded")
        time.sleep(10)  # Pause for 10 seconds (1 minute)

        # Find the name heading element (h1) and extract the person's name
        name_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[@class='text-heading-xlarge inline t-24 v-align-middle break-words']"))
        )
        person_name = name_element.text.strip()
        logging.info(f"- - Found person name: {person_name}")
        

        try:
            # Use the person's name to locate the specific "Connect" button
            connect_button = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, f"//button[contains(@aria-label, 'Invite {person_name} to connect')]"))
            )
            logging.info(f"- - Found 'Connect' button directly")
        
            # Scroll the "Connect" button into view
            driver.execute_script("arguments[0].scrollIntoView(true);", connect_button)
            logging.info(f"- - Scrolled to the 'Connect' button directly")
        
        
            # Force click the "Connect" button using JavaScript
            driver.execute_script("arguments[0].click();", connect_button)
            logging.info(f"- - Clicked 'Connect' button directly")
            time.sleep(10)  # Pause for 15 seconds

        except:
            logging.info(f"- - Connect not found directly, trying in More")
            # Locate the specific "More" button
            more_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//button[contains(@aria-label, 'More actions')]"))
            )
            logging.info(f"- - Found 'More' button")
            
            # Scroll the "More" button into view
            driver.execute_script("arguments[0].scrollIntoView(true);", more_button)
            logging.info(f"- - Scrolled to the 'More' button")
        
            # Click on the "More actions" button
            driver.execute_script("arguments[0].click();", more_button)
            logging.info(f"- - Clicked 'More' button")

            time.sleep(10) # Pause for 10 seconds

            # Wait for the dropdown to appear
            dropdown = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, "//*[contains(@class, 'artdeco-dropdown__content-inner')]"))
            )
            logging.info(f"- - Dropdown visible")

            # Use the person's name to locate the specific "Connect" button
            connect_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//div[starts-with(@id, 'ember') and @role='button' and .//span[text()='Connect']]"))
            )
            logging.info(f"- - Found 'Connect' button inside More")
            
            # Scroll the "Connect" button into view
            driver.execute_script("arguments[0].scrollIntoView(true);", connect_button)
            logging.info(f"- - Scrolled to the 'Connect' button inside More")
        
            # Force click the "Connect" button using JavaScript
            driver.execute_script("arguments[0].click();", connect_button)
            logging.info(f"- - Clicked 'Connect' button inside More using JavaScript")

            time.sleep(10) #Pause for 10 seconds

        try: 
            # Wait for the email input to appear (10 seconds timeout)
            email_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))
            )
            logging.info(f"- - Email input required")
              
            # Enter the email into the input field
            
            email_input.send_keys(email)
            logging.info(f"- - Entered email: {email}")

        except:

            logging.info(f"- - Email input not required")

            # Wait for the popup to appear and the "Add a note" button to be clickable
            add_note_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Add a note']"))
            )
            logging.info("- - Found the 'Add a note' button")
            
            # Click the "Add a note" button
            add_note_button.click()
            logging.info("- - Clicked 'Add a note' button")
            time.sleep(10)  # Pause for 10 seconds 
        
            message_input = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//textarea[@name='message' or @id='custom-message']"))
            )
            # Get the corresponding message for the current URL
            message_input.send_keys(msg)  
            logging.info(f"- - Entered the message: {msg}")
        
            send_invite_button = driver.find_element(By.XPATH, "//button[@aria-label='Send invitation']")
            send_invite_button.click()
            logging.info(f"{person_name} - Invitation sent with a note")

            # Update the status to 'Success' in the DataFrame
            data.at[index, 'Status'] = 'Success'
        
            # Add a 1-minute delay between requests
            logging.info("")
            logging.info("Waiting for 1 minute before sending the next request...")
            logging.info("")
            time.sleep(60)  # Pause for 60 seconds (1 minute)
    
    except:
        logging.info(f"Failed {url}")
        logging.info("")

        # Update the status to 'Failed' in the DataFrame
        data.at[index, 'Status'] = 'Failed'
        time.sleep(60)   # Pause for 60 seconds (1 minute)

driver.quit()
data.to_csv('outreach.csv', index=False)
logging.info("***Campaign Completed!***")