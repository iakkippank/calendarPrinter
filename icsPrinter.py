import itertools
import icalendar
from printerio.printerConfig import target_month, target_year, ics_file_path
from utils.htmlUtils import pretty_save_html
from utils.utils import map_component_to_event, filter_events, clease_components


def events_to_html_table(ics_file : str):
    with open(ics_file, 'rb') as f:
        cal = icalendar.Calendar.from_ical(f.read())

        # Group events by month and week
        event_list = cal.walk(name="VEVENT")
        # Removes events with no startdate e.g. events over multiple days
        cleansed_list = clease_components(event_list)
        event_list = map(map_component_to_event, cleansed_list)
        # Filter for month and year
        filtered_list = filter_events(event_list, target_month, target_year)
        # Sort by start date
        sorted_events = sorted(filtered_list, key=lambda x: x.start_date)
        # Group by week
        # TODO group by month as well to print multiple months
        group_events = itertools.groupby(sorted_events, lambda e: e.week_of_year)

        # Generate HTML table
        html_table = "<table border='1'><tr><th>Monat</th><th>Woche</th><th>Wann</th><th>Ort</th><th>Veranstaltung</th></tr>"
        html_table += f"<tr><td rowspan=\"{sorted_events.__len__()}\"><b>{sorted_events[0].format_german_month()}<b/></td>"

        for week_of_year, week_group in group_events:
            element_list = list(week_group)
            proxy_event = element_list[0]
            html_table += f"<td rowspan=\"{len(element_list)}\">{proxy_event.calculate_week_range()}</td>"
            for element in element_list:
                html_table += f"<td>{element.format_event()}</td>"
                html_table += f"<td>{element.location}</td>"
                html_table += f"<td>{element.summary}</td></tr>"

        html_table += "</table>"

    # Save the HTML table
    pretty_save_html(html_table)


events_to_html_table(ics_file_path)