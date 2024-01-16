import datetime

from Event import Event


def isEvent(component):
    if component.name == 'VEVENT':
        return True
    return False


def mapComponentToEvent(component):
    start_date = component.get('dtstart').dt
    min_time = datetime.datetime.now().time()
    if type(start_date) is datetime.date:
        start_date = datetime.datetime.combine(start_date,min_time)
    end_date = component.get('dtend').dt
    print(type(start_date))
    return Event(
        year=start_date.year,
        month=start_date.month,
        week_of_year=start_date.strftime('%W'),
        start_date=start_date,
        end_date=end_date,
        summary=component.get('summary')
    )

def filter_events_by_month(events, target_month):
    return [event for event in events if event.month == target_month]

def sortEventsForMonth(event):
    if event.month == 1:
        return True
    return False
