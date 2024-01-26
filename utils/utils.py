import datetime
from data.Event import Event

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
