import datetime

import icalendar

from data.Event import Event
from printerio.printerConfig import output_file_path


def read_ics_file(ics_file: str) -> list[Event]:
    with open(ics_file, 'rb') as f:
        cal = icalendar.Calendar.from_ical(f.read())
        # Group events by month and week
        event_list = cal.walk(name="VEVENT")
        # Removes events with no startdate e.g. events over multiple days
        cleansed_list = clease_components(event_list)

    return [map_component_to_event(event) for event in cleansed_list]

def is_event(component):
    if component.name == 'VEVENT':
        return True
    return False


def map_component_to_event(component) -> Event:
    start_date = component.get('dtstart').dt
    end_date = component.get('dtend').dt
    return Event(
        year=start_date.year,
        month=start_date.month,
        week_of_year=start_date.strftime('%W'),
        start_date=start_date,
        end_date=end_date,
        summary=component.get('summary'),
        location=component.get('location')
    )


def filter_events_by_month_range(events: list[Event], start_month: int, end_month: int, year: int) -> list[Event]:
    return [event for event in events if start_month <= event.month <= end_month and event.year == year]


def clease_components(component_list):
    event_list = list()
    for component in component_list:
        if isinstance(component.get('dtstart').dt, datetime.datetime):
            event_list.append(component)
    return event_list
