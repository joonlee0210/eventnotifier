import time
import requests
import schedule
from datetime import datetime
from plyer import notification  # Sends PC notifications

HEADERS = {"Authorization": "Bearer YOUR_ACCESS_TOKEN"}  # Replace with your API token
API_URL = "https://www.eventbriteapi.com/v3/users/me/owned_events/"
LAST_EVENT_ID = None  # Store the last seen event ID
LAST_AVAILABILITY = None  # Track last known availability


def get_ticket_availability(event_id):
    """Fetch ticket availability for the given event."""
    ticket_url = f"https://www.eventbriteapi.com/v3/events/{event_id}/ticket_classes/"
    response = requests.get(ticket_url, headers=HEADERS)

    if response.status_code == 200:
        tickets = response.json().get("ticket_classes", [])
        return "Available" if any(ticket.get("on_sale_status") == "AVAILABLE" for ticket in tickets) else "Sold Out"
    else:
        return "Unknown"


def check_event_updates():
    """Fetch latest event and notify if there's an update."""
    global LAST_EVENT_ID, LAST_AVAILABILITY

    response = requests.get(API_URL, headers=HEADERS)

    if response.status_code == 200:
        events = response.json().get("events", [])

        if events:
            latest_event = events[0]  # Most recent event
            event_id = latest_event["id"]
            event_name = latest_event["name"]["text"]
            event_date = latest_event["start"]["local"]
            event_url = latest_event["url"]

            # Check availability
            availability = get_ticket_availability(event_id)

            # Notify if there's a new event or availability changes
            if event_id != LAST_EVENT_ID:
                notification_title = "New Event Posted!"
                notification_message = f"{event_name}\n📅 {event_date}\n🎫 {availability}\n🔗 Click to view"
                LAST_EVENT_ID = event_id  # Update last event ID

            elif availability != LAST_AVAILABILITY:
                notification_title = "Ticket Availability Updated!"
                notification_message = f"{event_name}\n🎫 Now: {availability}"

            else:
                return  # No changes, so no notification needed

            # Send notification
            notification.notify(
                title=notification_title,
                message=notification_message,
                app_name="Event Notifier",
                timeout=10
            )

            LAST_AVAILABILITY = availability  # Update last availability

        else:
            print("No events found.")
    else:
        print("Error fetching events:", response.status_code)


# Schedule to run every 30 minutes
schedule.every(30).minutes.do(check_event_updates)

if __name__ == "__main__":
    print("✅ Event notifier is running...")
    check_event_updates()  # Run once immediately

    while True:
        schedule.run_pending()
        time.sleep(60)  # Wait 1 minute before checking again
