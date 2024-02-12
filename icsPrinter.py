from typing import List

from data.Event import Event
from tkinter_app.EventSelectionApp import EventSelectionApp

event_list: List[Event] = []

event_selector = EventSelectionApp(event_list)
event_selector.run()
