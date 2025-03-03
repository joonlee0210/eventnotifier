# eventnotifier

This project automatically tracks the latest events posted by a specific Eventbrite organizer and notifies you when new events are posted or ticket availability changes.
Features

  Fetches the latest event from a specified Eventbrite organizer.
    Displays event details, including name, date, location, and ticket availability.
    Checks ticket availability regularly and notifies you if it changes.
    Runs automatically in the background and sends PC notifications when:
        A new event is posted.
        Ticket availability changes (Available → Sold Out or vice versa).

Setup

  1. Install Requirements
        Requires Python 3.7+
        Install dependencies using pip install -r requirements.txt

  2. Configure API Access
        Get an Eventbrite API key from Eventbrite API
        Add your API key to the script

  3. Run the Script
        The web scraper can be run manually to check event details.
        The notifier script runs automatically and sends notifications.

Automation

   - The event notifier checks for updates every 30 minutes by default.
    It can be set to run on startup for continuous tracking.
    Works on Windows, macOS, and Linux.

Customization
   -  Adjust the check interval to modify how often the script checks for updates.
    Modify notification messages to suit your preferences.
