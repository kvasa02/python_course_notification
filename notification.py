import os
import time
import requests
from bs4 import BeautifulSoup
from plyer import notification
from twilio.rest import Client
from dotenv import load_dotenv
import sys
import traceback
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('course_notifier.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

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
    logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
    logger.error("Please copy env.example to .env and fill in your credentials")
    sys.exit(1)

# Get variables from .env
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
messaging_service_sid = os.getenv("MESSAGING_SERVICE_SID")
my_number = os.getenv("MY_NUMBER")
URL = os.getenv("COURSE_URL")
COURSE_CODE = os.getenv("COURSE_CODE")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "600"))  # Default is 10 minutes

# Additional validation for required variables
if not all([account_sid, auth_token, messaging_service_sid, my_number, URL, COURSE_CODE]):
    logger.error("One or more required environment variables are empty")
    sys.exit(1)

# Type casting after validation
account_sid = str(account_sid)
auth_token = str(auth_token)
messaging_service_sid = str(messaging_service_sid)
my_number = str(my_number)
URL = str(URL)
COURSE_CODE = str(COURSE_CODE)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def send_text_notification():
    """Send SMS notification via Twilio"""
    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f"🎓 Course Alert: {COURSE_CODE} is now available! Go register before it's full!",
            messaging_service_sid=messaging_service_sid,
            to=my_number
        )
        logger.info(f"Twilio SMS sent successfully! SID: {message.sid}")
        return True
    except Exception as e:
        logger.error(f"Failed to send SMS notification: {e}")
        return False

def send_desktop_notification():
    """Send desktop notification"""
    try:
        notification.notify(
            title=f"Course Available: {COURSE_CODE}",
            message="A spot has opened up! Go register before it fills up again!",
            timeout=10,
            app_icon=None  # e.g. 'C:\\icon_32x32.ico'
        )
        logger.info("Desktop notification sent successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to send desktop notification: {e}")
        return False

def check_course_availability():
    """Check if the course is available by scraping the webpage"""
    try:
        logger.info(f"Checking availability for {COURSE_CODE} at {URL}")
        
        response = requests.get(URL, headers=HEADERS, timeout=15)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        soup = BeautifulSoup(response.text, 'html.parser')
        page_text = soup.get_text().lower()
        
        course_code_lower = COURSE_CODE.lower()
        index = page_text.find(course_code_lower)
        
        if index == -1:
            logger.warning(f"Course code '{COURSE_CODE}' not found on the page")
            return False
        
        # Check the text around the course code for availability indicators
        start_index = max(0, index - 100)
        end_index = min(len(page_text), index + 300)
        context_text = page_text[start_index:end_index]
        
        # Look for indicators that the course is full
        full_indicators = ['full', 'closed', 'no seats', 'waitlist', 'enrollment closed']
        is_full = any(indicator in context_text for indicator in full_indicators)
        
        if not is_full:
            logger.info(f"🎉 Course {COURSE_CODE} appears to be available!")
            return True
        else:
            logger.info(f"Course {COURSE_CODE} is still full. Checking again in {CHECK_INTERVAL} seconds...")
            return False
            
    except requests.exceptions.Timeout:
        logger.error("Request timed out. The website may be slow or unavailable.")
        return False
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error occurred: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during course check: {e}")
        logger.error(traceback.format_exc())
        return False

def main():
    """Main function to run the course monitoring loop"""
    logger.info("🚀 Starting Course Availability Notifier")
    logger.info(f"Monitoring course: {COURSE_CODE}")
    logger.info(f"Target URL: {URL}")
    logger.info(f"Check interval: {CHECK_INTERVAL} seconds ({CHECK_INTERVAL/60:.1f} minutes)")
    logger.info(f"Phone number: {my_number}")
    
    check_count = 0
    
    while True:
        try:
            check_count += 1
            logger.info(f"Check #{check_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            if check_course_availability():
                logger.info("🎊 COURSE IS AVAILABLE! Sending notifications...")
                
                # Send both types of notifications
                sms_sent = send_text_notification()
                desktop_sent = send_desktop_notification()
                
                if sms_sent or desktop_sent:
                    logger.info("✅ Notifications sent successfully!")
                    logger.info("Stopping monitoring as course is now available.")
                    break
                else:
                    logger.error("❌ Failed to send notifications, continuing to monitor...")
            
            # Wait before next check
            logger.info(f"Waiting {CHECK_INTERVAL} seconds before next check...")
            time.sleep(CHECK_INTERVAL)
            
        except KeyboardInterrupt:
            logger.info("🛑 Monitoring stopped by user")
            break
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {e}")
            logger.error(traceback.format_exc())
            logger.info("Waiting 60 seconds before retrying...")
            time.sleep(60)

if __name__ == "__main__":
    main()