import icalendar
import requests
from data.Event import Event
from printerio.printerConfig import calendar_urls
from utils.utils import clease_components, map_component_to_event

def download_ics_files(urls, save_path):
    combined_calendar = icalendar.Calendar()
    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            calendar_data = response.text.encode('utf-8')
            calendar = icalendar.Calendar.from_ical(calendar_data)
            combined_calendar.subcomponents += calendar.subcomponents
            print(f"Downloaded and combined events from {url}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading the file from {url}: {e}")
        except Exception as e:
            print(f"Error processing the file from {url}: {e}")

    try:
        with open(save_path, 'wb') as f:
            f.write(combined_calendar.to_ical())
        print(f"Combined calendar saved successfully at: {save_path}")
    except Exception as e:
        print(f"Error saving the combined calendar: {e}")


def read_ics_file(ics_file: str) -> list[Event]:
    with open(ics_file, 'rb') as f:
        cal = icalendar.Calendar.from_ical(f.read())
        # Group events by month and week
        event_list = cal.walk(name="VEVENT")
        # Removes events with no startdate e.g. events over multiple days
        cleansed_list = clease_components(event_list)

    return [map_component_to_event(event) for event in cleansed_list]
