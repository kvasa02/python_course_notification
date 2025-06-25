import os
import time
import requests
from bs4 import BeautifulSoup
from plyer import notification
from twilio.rest import Client
from dotenv import load_dotenv
import sys
import traceback

# Load environment variables
load_dotenv()

# Validate required environment variables
required_vars = [
    "TWILIO_ACCOUNT_SID",
    "TWILIO_AUTH_TOKEN",
    "MESSAGING_SERVICE_SID",
    "MY_NUMBER",
    "COURSE_URL",
    "COURSE_CODE"
]
missing_vars = [v for v in required_vars if not os.getenv(v)]
if missing_vars:
    print(f"Missing required environment variables: {', '.join(missing_vars)}")
    sys.exit(1)

# Get variables from .env
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
messaging_service_sid = os.getenv("MESSAGING_SERVICE_SID")
my_number = os.getenv("MY_NUMBER")
URL = os.getenv("COURSE_URL")
COURSE_CODE = os.getenv("COURSE_CODE")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "600"))  # Default is 10 minutes

HEADERS = {"User-Agent": "Mozilla/5.0"}

def send_text_notification():
    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body="Your course is now available! Go register before it's full!",
            messaging_service_sid=messaging_service_sid,
            to=my_number
        )
        print("Twilio text sent! SID:", message.sid)
    except Exception as e:
        print("Failed to send text notification:", e)

def check_course():
    try:
        response = requests.get(URL, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        page_text = soup.get_text().lower()

        course_code_lower = COURSE_CODE.lower()
        index = page_text.find(course_code_lower)
        if index != -1:
            post_code_text = page_text[index:index+200]
            if "full" not in post_code_text:
                print("Your course might be available! Sending notification...")
                notification.notify(
                    title="Your course is available!",
                    message="Go sign up before it fills up again!",
                    timeout=10
                )
                send_text_notification()
                return True
        print("Still full... checking again soon.")
        return False
    except Exception as e:
        print("Error during check:", e)
        traceback.print_exc()
        return False

if __name__ == "__main__":
    while True:
        if check_course():
            break
        time.sleep(CHECK_INTERVAL)