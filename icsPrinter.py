from typing import List

from data.Event import Event
from icsPrinterGUI import EventSelectorApp
from printerio.printerConfig import target_year, start_month, end_month
from utils.otherUtils import filter_events_by_month_range

# Get calendar.ics from file
event_list: List[Event] = []

# Filter for month and year
filtered_list = filter_events_by_month_range(
    events=event_list,
    start_month=start_month,
    end_month=end_month,
    year=target_year
)

# Sort by start date
sorted_events = sorted(filtered_list, key=lambda x: x.start_date)

event_selector = EventSelectorApp(sorted_events)
event_selector.run()
