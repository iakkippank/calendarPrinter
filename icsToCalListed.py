import icalendar
from datetime import datetime
from collections import defaultdict
from Event import Event

# Replace 'your_file.ics' with the path to your ICS file
ics_file_path = 'calendar.ics'


def print_january_events_without_notes(ics_file_path):
    with open(ics_file_path, 'rb') as f:
        cal = icalendar.Calendar.from_ical(f.read())

        for component in cal.walk():
            if component.name == 'VEVENT':
                start_date = component.get('dtstart').dt
                end_date = component.get('dtend').dt

                # Check if the event is in January
                if start_date.month == 1 or end_date.month == 1:
                    # Print the summary (event title) without notes
                    summary = component.get('summary')
                    if summary:
                        print(
                            f"{start_date.strftime('%Y-%m-%d %H:%M')} - {end_date.strftime('%Y-%m-%d %H:%M')}: {summary}")


def events_to_html_table(ics_file_path):
    with open(ics_file_path, 'rb') as f:
        cal = icalendar.Calendar.from_ical(f.read())

        # Group events by month and week
        grouped_events = defaultdict(lambda: defaultdict(list))

        for component in cal.walk():
            if component.name == 'VEVENT':
                start_date = component.get('dtstart').dt
                end_date = component.get('dtend').dt
                event = Event(
                    month=start_date.month,
                    week_of_year=start_date.strftime('%W'),
                    start_date=start_date,
                    end_date=end_date,
                    summary=component.get('summary'),
                )

                if event.start_date.month == 1 or event.end_date.month == 1:
                    # Group by month and week
                    key = (start_date.year, event.start_date.month, event.week_of_year)
                    grouped_events[key]['events'].append({
                        'start_date': start_date,
                        'end_date': end_date,
                        'summary': event.summary
                    })

        # Sort grouped_Events
        # sorted(grouped_events, key=lambda x: x['start_date'])

        # Sort events within each week by start date
        # for month in grouped_events.values():
        #    month['events'] = sorted(month['events'], key=lambda x: x['start_date'])

        # Generate HTML table
        html_table = "<table border='1'><tr><th>Month</th><th>Week</th><th>Start Date</th><th>End Date</th><th>Summary</th></tr>"

        for (year, month, week), data in grouped_events.items():
            for event in data['events']:
                html_table += f"<tr><td>{datetime(year, month, 1).strftime('%B')}</td>"
                html_table += f"<td>{week}</td>"
                html_table += f"<td>{event['start_date'].strftime('%Y-%m-%d %H:%M')}</td>"
                html_table += f"<td>{event['end_date'].strftime('%Y-%m-%d %H:%M')}</td>"
                html_table += f"<td>{event['summary']}</td></tr>"

        html_table += "</table>"

        # Save the HTML table to a file (replace 'output_table.html' with your desired filename)
        with open('output_table.html', 'w', encoding="utf-8") as html_file:
            html_file.write(html_table)


events_to_html_table(ics_file_path)
print_january_events_without_notes(ics_file_path)
