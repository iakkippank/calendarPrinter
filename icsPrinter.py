from typing import List
from data.Event import Event
from icsPrinterGUI import show_app_window
from printerio.printerConfig import target_year, ics_file_path, start_month, end_month, calendar_urls
from utils.icsUtils import read_ics_file, download_ics_files
from utils.userInputUtils import show_selection_prompt, shouldDownloadIcs
from utils.htmlUtils import pretty_save_html, generate_html_table
from utils.otherUtils import filter_events_by_month_range

# Get calendar.ics from file
event_list: List[Event] = []

# User selection for download or local ics file
#if shouldDownloadIcs():
event_list = download_ics_files(calendar_urls)
#else:
#    event_list = read_ics_file(ics_file_path)

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

show_app_window(sorted_events)


print("Fertsch!")
