import datetime
from data.Event import Event
from io.printerConfig import output_file_path


def is_event(component):
    if component.name == 'VEVENT':
        return True
    return False


def map_component_to_event(component):
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


def filter_events(events, target_month, target_year):
    return [event for event in events if (event.month == target_month and event.year == target_year)]


def clease_components(component_list):
    event_list = list()
    for component in component_list:
        if isinstance(component.get('dtstart').dt, datetime.datetime):
            event_list.append(component)
    return event_list

def prettySaveHtml(htmlString : str):
    with open(output_file_path, 'w', encoding="utf-8") as html_file:
        html_file.write(htmlString)