from collections import defaultdict
from data.Event import Event, format_german_month
from bs4 import BeautifulSoup as bs
from printerio.printerConfig import output_file_path
from utils.constants import HTML_TABLE_HEAD


def pretty_save_html(html_string : str):
    soup = bs( html_string, features= "html.parser")    #make BeautifulSoup
    pretty_html = soup.prettify()                       #prettify the html
    with open(output_file_path, 'w', encoding="utf-8") as html_file:
        html_file.write(pretty_html)


def generate_html_table(selected_events: list[Event]) -> str:
    # Dictionary to hold events grouped by month and week_of_year
    grouped_events = defaultdict(lambda: defaultdict(list[Event]))

    # Group events by month and week_of_year
    for event in selected_events:
        grouped_events[event.start_date.month][event.week_of_year].append(event)

    # Generate HTML table
    html_table = HTML_TABLE_HEAD
    for month, weeks in grouped_events.items():
        total_events_in_month = sum(
            len(events_in_week) for events_in_week in weeks.values()) + 1  # No Idea why this is needed
        html_table += f"<tr><th rowspan=\"{total_events_in_month}\"><b>{format_german_month(month)}</b></th>"
        for week, events_in_week in weeks.items():
            proxy_event = events_in_week[0]
            if week == next(iter(weeks.values())):
                html_table += f"<th rowspan=\"{len(events_in_week)}\">{proxy_event.calculate_week_range()}</th>"
            else:
                html_table += f"<tr><th rowspan=\"{len(events_in_week)}\">{proxy_event.calculate_week_range()}</th>"
            for event in events_in_week:
                if event == events_in_week[0]:
                    html_table += f"<td>{event.format_event_time_for_table()}</td>"
                else:
                    html_table += f"<tr><td>{event.format_event_time_for_table()}</td>"
                html_table += f"<td>{event.location}</td>"
                html_table += f"<td>{event.summary}</td></tr>"
    html_table += "</table>"
    return html_table
