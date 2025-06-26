# Course Availability Notifier

A Python-based course availability notifier that automatically monitors course registration websites and sends real-time alerts when spots become available.

## Features

- **Automated Web Scraping**: Continuously monitors course registration pages for availability
- **Real-time Notifications**: Sends SMS alerts via Twilio and desktop notifications
- **Secure Configuration**: Uses environment variables for credential management
- **Configurable Monitoring**: Customizable check intervals (default: 10 minutes)
- **Error Handling**: Robust error handling with detailed logging

## Prerequisites

- Python 3.7+
- Twilio account (for SMS notifications)
- Course registration website URL

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd python_course_notification
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` with your actual credentials:
   - `TWILIO_ACCOUNT_SID`: Your Twilio Account SID
   - `TWILIO_AUTH_TOKEN`: Your Twilio Auth Token
   - `MESSAGING_SERVICE_SID`: Your Twilio Messaging Service SID
   - `MY_NUMBER`: Your phone number (include country code)
   - `COURSE_URL`: The course registration page URL
   - `COURSE_CODE`: The course code to monitor (e.g., "CS101")
   - `CHECK_INTERVAL`: Check interval in seconds (default: 600)

## Usage

Run the notification script:
```bash
python notification.py
```

The script will:
1. Check the course availability every 10 minutes (or your specified interval)
2. Send desktop notification when course becomes available
3. Send SMS notification via Twilio
4. Continue monitoring until course is found available

## How It Works

1. **Web Scraping**: Uses BeautifulSoup to parse the course registration page
2. **Course Detection**: Searches for the specified course code and checks for "full" status
3. **Notification System**: Triggers both desktop and SMS notifications when availability is detected
4. **Continuous Monitoring**: Runs indefinitely with configurable intervals

## Security Features

- Environment variables for sensitive credentials
- `.gitignore` configured to exclude `.env` files
- No hardcoded credentials in source code

## Error Handling

- Network timeout handling (15 seconds)
- Twilio API error handling
- Detailed error logging with traceback
- Graceful failure recovery

## Platform Compatibility

- **Desktop Notifications**: 
  - ✅ Windows and Linux: Fully supported
  - ⚠️ macOS: May require additional setup for Python 3.13+ due to pyobjus compatibility issues
  - SMS notifications work on all platforms

## Customization

You can modify the script to:
- Add different notification methods
- Implement more sophisticated course detection logic
- Add multiple course monitoring
- Customize notification messages

## Testing

Run the test script to verify functionality:
```bash
python test_notification.py
```

## Troubleshooting

- Ensure all environment variables are set correctly
- Verify your Twilio credentials are valid
- Check that the course URL is accessible
- Ensure your phone number includes country code
- For macOS desktop notifications: Consider using Python 3.11 or 3.12 if experiencing issues


=======
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
python3 notification.py
```

The script will use BeautifulSoup to scrape course information and Twilio to send SMS notifications as configured.

## File Structure

- `notification.py` - Main script to scrape data and send notifications.
- `requirements.txt` - Python dependencies (including `twilio` and `beautifulsoup4`).
- `.env` - Environment variables file (not included in version control for security).


*Created by [kvasa02](https://github.com/kvasa02)*
>>>>>>> d9e32eff9f6fd902e4de04b0c89b1213781d985a
