# Python Course Notification

A Python project to send notifications related to a course. This project sends reminders or updates for course participants, leveraging the Twilio API for SMS notifications and BeautifulSoup for web scraping.

## Features

- Send custom SMS notifications using the Twilio API.
- Scrape course information or updates using BeautifulSoup.
- Uses environment variables for sensitive configuration.
- Easily configurable and extendable.

## Getting Started

### Prerequisites

- Python 3.8 or newer
- [pip](https://pip.pypa.io/en/stable/installation/)
- Twilio account (for sending SMS)
- Twilio credentials (Account SID, Auth Token)
- A valid phone number (for sending/receiving SMS)

### Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/kvasa02/python_course_notification.git
   cd python_course_notification
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Copy `.env.example` to `.env` (if `.env.example` exists) or create a `.env` file.
   - Add your Twilio credentials and any other required environment variables:
     ```
     TWILIO_ACCOUNT_SID=your_account_sid
     TWILIO_AUTH_TOKEN=your_auth_token
     TWILIO_PHONE_NUMBER=your_twilio_number
     ```

### Usage

Run the notification script:
```sh
python notification.py
```

The script will use BeautifulSoup to scrape course information and Twilio to send SMS notifications as configured.

## File Structure

- `notification.py` - Main script to scrape data and send notifications.
- `requirements.txt` - Python dependencies (including `twilio` and `beautifulsoup4`).
- `.env` - Environment variables file (not included in version control for security).


*Created by [kvasa02](https://github.com/kvasa02)*
