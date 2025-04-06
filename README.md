# Calendar SMS Notifier

This application sends you a daily SMS with your Google Calendar events for the day.

## Setup Instructions

### 1. Google Calendar API Setup
1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the Google Calendar API
4. Create OAuth 2.0 credentials
5. Download the credentials and save them as `credentials.json` in the project directory

### 2. Twilio Setup
1. Sign up for a [Twilio account](https://www.twilio.com/try-twilio)
2. Get your Account SID and Auth Token
3. Get a Twilio phone number

### 3. Environment Variables
Update the `.env` file with your credentials:
```
GOOGLE_CALENDAR_CREDENTIALS_PATH=credentials.json
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
YOUR_PHONE_NUMBER=your_phone_number
```

### 4. Installation
1. Create a virtual environment:
```bash
python -m venv env
```

2. Activate the virtual environment:
```bash
# On Windows
.\env\Scripts\activate
# On macOS/Linux
source env/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
Run the application:
```bash
python calendar_sms.py
```

The application will:
1. First time: Open a browser window for Google Calendar authentication
2. Send you an SMS with today's calendar events
3. Continue running and send you daily updates at 7 AM

To stop the application, press Ctrl+C.

## Features
- Fetches all events for the current day
- Sends formatted SMS with event times and descriptions
- Runs automatically at 7 AM daily
- Secure credential storage using environment variables 