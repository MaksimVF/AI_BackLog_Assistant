




import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from typing import Optional, Dict, Any, List

class GoogleCalendarConnector:
    """Agent for interacting with Google Calendar API"""

    def __init__(self, credentials: Credentials):
        self.credentials = credentials
        self.service = build('calendar', 'v3', credentials=credentials)

    def create_event(self, calendar_id: str, summary: str, description: str,
                    start_time: datetime.datetime, end_time: datetime.datetime,
                    attendees: List[str] = None) -> Optional[Dict]:
        """Create a new calendar event"""
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'UTC',
            },
            'attendees': [{'email': email} for email in attendees] if attendees else [],
            'reminders': {
                'useDefault': True,
            },
        }

        try:
            event_result = self.service.events().insert(
                calendarId=calendar_id,
                body=event
            ).execute()

            return event_result
        except Exception as e:
            print(f"Error creating event: {e}")
            return None

    def get_events(self, calendar_id: str, time_min: datetime.datetime = None,
                  time_max: datetime.datetime = None, max_results: int = 10) -> List[Dict]:
        """Get calendar events"""
        try:
            # Set default time range if not provided
            if not time_min:
                time_min = datetime.datetime.utcnow().isoformat() + 'Z'
            if not time_max:
                time_max = (datetime.datetime.utcnow() + datetime.timedelta(days=30)).isoformat() + 'Z'

            events_result = self.service.events().list(
                calendarId=calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()

            return events_result.get('items', [])
        except Exception as e:
            print(f"Error getting events: {e}")
            return []

    def update_event(self, calendar_id: str, event_id: str, updates: Dict) -> Optional[Dict]:
        """Update an existing calendar event"""
        try:
            # Get the existing event
            event = self.service.events().get(
                calendarId=calendar_id,
                eventId=event_id
            ).execute()

            # Update the event
            event.update(updates)

            updated_event = self.service.events().update(
                calendarId=calendar_id,
                eventId=event_id,
                body=event
            ).execute()

            return updated_event
        except Exception as e:
            print(f"Error updating event: {e}")
            return None

    def delete_event(self, calendar_id: str, event_id: str) -> bool:
        """Delete a calendar event"""
        try:
            self.service.events().delete(
                calendarId=calendar_id,
                eventId=event_id
            ).execute()
            return True
        except Exception as e:
            print(f"Error deleting event: {e}")
            return False

    def get_calendar_list(self) -> List[Dict]:
        """Get the list of calendars"""
        try:
            calendar_list = self.service.calendarList().list().execute()
            return calendar_list.get('items', [])
        except Exception as e:
            print(f"Error getting calendar list: {e}")
            return []

    def create_calendar(self, summary: str, description: str = '') -> Optional[Dict]:
        """Create a new calendar"""
        calendar = {
            'summary': summary,
            'description': description,
            'timeZone': 'UTC'
        }

        try:
            created_calendar = self.service.calendars().insert(
                body=calendar
            ).execute()

            return created_calendar
        except Exception as e:
            print(f"Error creating calendar: {e}")
            return None

# Example usage
if __name__ == '__main__':
    from google_auth import get_google_credentials

    # Get Google credentials
    credentials = get_google_credentials()

    if credentials:
        calendar = GoogleCalendarConnector(credentials)

        # Example: Get calendar list
        calendars = calendar.get_calendar_list()
        print("Calendars:", calendars)

        if calendars:
            # Use the primary calendar
            primary_calendar = calendars[0]['id']

            # Example: Create an event
            start_time = datetime.datetime.utcnow() + datetime.timedelta(days=1)
            end_time = start_time + datetime.timedelta(hours=1)

            event = calendar.create_event(
                primary_calendar,
                'Team Meeting',
                'Discuss project progress and next steps',
                start_time,
                end_time,
                ['team@example.com', 'manager@example.com']
            )
            print("Created event:", event)

            # Example: Get events
            events = calendar.get_events(primary_calendar)
            print("Upcoming events:", events)
    else:
        print("Please authenticate with Google first")





