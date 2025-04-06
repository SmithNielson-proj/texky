import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from twilio.rest import Client
from dotenv import load_dotenv
import schedule
import time

# Load environment variables
load_dotenv()

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_calendar_service():
    """Get Google Calendar service with proper authentication."""
    creds = None
    # The file token.json stores the user's access and refresh tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.getenv('GOOGLE_CALENDAR_CREDENTIALS_PATH'), SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)

def get_today_events():
    """Get today's events from Google Calendar."""
    service = get_calendar_service()
    
    # Get today's date range
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    end_of_day = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + 'Z'
    
    # Call the Calendar API
    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        timeMax=end_of_day,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    return events

def format_events_message(events):
    """Format calendar events into a readable SMS message."""
    if not events:
        return "You have no events scheduled for today."
    
    message = "Today's Calendar Events:\n\n"
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start_time = datetime.datetime.fromisoformat(start.replace('Z', '+00:00'))
        formatted_time = start_time.strftime('%I:%M %p')
        message += f"{formatted_time}: {event['summary']}\n"
    
    return message

def send_sms(message):
    """Send SMS using Twilio."""
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)
    
    message = client.messages.create(
        body=message,
        from_=os.getenv('TWILIO_PHONE_NUMBER'),
        to=os.getenv('YOUR_PHONE_NUMBER')
    )
    print(f"Message sent! SID: {message.sid}")

def send_daily_calendar():
    """Main function to fetch calendar events and send SMS."""
    events = get_today_events()
    message = format_events_message(events)
    send_sms(message)

def main():
    # Schedule the job to run every day at 7 AM
    schedule.every().day.at("08:00").do(send_daily_calendar)
    
    print("Calendar SMS service started. Will send updates at 7 AM daily.")
    print("Press Ctrl+C to exit.")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == '__main__':
    main() 