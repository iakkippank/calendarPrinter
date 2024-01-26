from typing import List
from data.Event import Event
from printerio.printerConfig import target_year, ics_file_path, start_month, end_month
from utils.userCheckboxSelection import show_selection_prompt
from utils.htmlUtils import pretty_save_html, generate_html_table
from utils.utils import filter_events_by_month_range, read_ics_file

# Get calendar.ics from file
event_list: List[Event] = read_ics_file(ics_file_path)

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

# Make user prompt to select events
selected_events = show_selection_prompt(sorted_events)

# Group the events and generate the HTML table
html_table = generate_html_table(selected_events)

# Save the HTML table
pretty_save_html(html_table)
print("Fertsch!")
