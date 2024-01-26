import pprint
from collections import defaultdict
from typing import List
from data.Event import Event, format_german_month
import icalendar
from printerio.printerConfig import target_year, ics_file_path, start_month, end_month
from utils.constants import HTML_TABLE_HEAD
from utils.htmlUtils import pretty_save_html
from utils.utils import map_component_to_event, clease_components, filter_events_by_month_range


def events_to_html_table(ics_file : str):
    with open(ics_file, 'rb') as f:
        cal = icalendar.Calendar.from_ical(f.read())

        # Group events by month and week
        event_list = cal.walk(name="VEVENT")
        # Removes events with no startdate e.g. events over multiple days
        cleansed_list = clease_components(event_list)
        event_list: List[Event] = [map_component_to_event(event) for event in cleansed_list]

        # Handle the case where element_list is empty
        if not event_list:
            raise ValueError(
                "Oops! Looks like there are no events for this period. Time to relax and enjoy some downtime!")

        # Filter for month and year
        filtered_list = filter_events_by_month_range(
            events=event_list,
            start_month=start_month,
            end_month=end_month,
            year=target_year
        )

        # Sort by start date
        sorted_events = sorted(filtered_list, key=lambda x: x.start_date)

        # Dictionary to hold events grouped by month and week_of_year
        grouped_events = defaultdict(lambda: defaultdict(list[Event]))

        # Group events by month and week_of_year
        for event in sorted_events:
            grouped_events[event.start_date.month][event.week_of_year].append(event)

        # Generate HTML table
        html_table = HTML_TABLE_HEAD

        for month, weeks in grouped_events.items():
            total_events_in_month = sum(len(events_in_week) for events_in_week in weeks.values())
            html_table += f"<tr><th rowspan=\"{total_events_in_month}\"><b>{format_german_month(month)}</b></th>"
            for week, events_in_week in weeks.items():
                proxy_event = events_in_week[0]
                html_table += f"<th rowspan=\"{len(events_in_week)}\">{proxy_event.calculate_week_range()}</th>"
                for event in events_in_week:
                    if event == events_in_week[0]:
                        html_table += f"<td>{event.format_event()}</td>"
                    else:
                        html_table += f"<tr><td>{event.format_event()}</td>"
                    html_table += f"<td>{event.location}</td>"
                    html_table += f"<td>{event.summary}</td></tr>"

        # for week_of_year, week_group in group_events:
        #     element_list = list(week_group)
        #     proxy_event = element_list[0]
        #     html_table += f"<td rowspan=\"{len(element_list)}\">{proxy_event.calculate_week_range()}</td>"
        #     for element in element_list:
        #         html_table += f"<td>{element.format_event()}</td>"
        #         html_table += f"<td>{element.location}</td>"
        #         html_table += f"<td>{element.summary}</td></tr>"

        html_table += "</table>"

    # Save the HTML table
    pretty_save_html(html_table)


events_to_html_table(ics_file_path)