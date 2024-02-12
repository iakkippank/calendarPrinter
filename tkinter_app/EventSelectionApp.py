import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from printer_io.printerConfig import calendar_urls, ics_file_path
from utils.htmlUtils import generate_html_table, pretty_save_html
from utils.icsUtils import download_ics_files, read_ics_file, filter_and_sort_events


class EventSelectionApp:
    def __init__(self, events):
        self.events = events
        self.checkboxes = []

    def _on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _save_html_table(self):
        selected_events = [self.events[i] for i, var in enumerate(self.event_vars) if var.get()]
        # Make user prompt to select events
        # selected_events = show_selection_prompt(sorted_events)
        # Group the events and generate the HTML table
        html_table = generate_html_table(selected_events)
        # Save the HTML table
        pretty_save_html(html_table)
        messagebox.showinfo("Info", "Fertsch!")

    def run(self):
        self.root = tk.Tk()
        self.root.title("Termine auswählen")
        self.root.minsize(1280, 720)
        # Import the tcl file
        self.root.tk.call('source', 'theme/forest-dark.tcl')

        # Set the theme with the theme_use method
        ttk.Style().theme_use('forest-dark')

        settings_lframe = ttk.LabelFrame(self.root, text="Einstellungen")
        selection_frame = ttk.Frame(self.root)
        event_list_lframe = ttk.LabelFrame(selection_frame, text="Eingetragene Veranstaltungen")

        settings_lframe.pack(side=tk.LEFT, fill=tk.Y, expand=False, pady=10, padx=10)
        selection_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        event_list_lframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10, padx=10)

        # Create a canvas
        self.canvas = tk.Canvas(event_list_lframe)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a frame inside the canvas to hold the list of checkboxes
        self.checkbox_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.checkbox_frame, anchor=tk.NW)

        # Configure canvas scrolling
        self.checkbox_frame.bind("<Configure>", self._on_configure)
        self.canvas.bind("<Configure>", self._on_configure)
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)  # Bind mouse wheel scroll event

        # Create variables to track checkbox states
        self.event_vars = [tk.BooleanVar(self.root, value=True) for _ in self.events]

        # Create checkboxes for each event and pack them into the frame
        for i, event in enumerate(self.events):
            checkbox = ttk.Checkbutton(self.checkbox_frame, text=event.format_event_to_readable_string(),
                                       variable=self.event_vars[i])
            checkbox.pack(anchor=tk.W)
            self.checkboxes.append(checkbox)

        # Create a scrollbar and attach it to the canvas
        scrollbar = ttk.Scrollbar(event_list_lframe, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Button to select events
        download_button = ttk.Button(settings_lframe, text="Termine herunterladen", command=self._download_events)
        remove_events_button = ttk.Button(settings_lframe, text="Termine löschen", command=self._remove_event_list)
        local_ics_button = ttk.Button(settings_lframe, text="Termine aus Calender Datei laden",
                                      command=self._get_local_events)
        select_button = ttk.Button(selection_frame, text="Erstelle HTML Tabelle", command=self._save_html_table)
        select_button.pack(side=tk.BOTTOM, pady=10, padx=10)
        download_button.pack(pady=10, padx=10)
        local_ics_button.pack(pady=10, padx=10)
        remove_events_button.pack(pady=10, padx=10)

        # Start the GUI event loop
        self.root.mainloop()

    def _download_events(self):
        downloaded_event_list = download_ics_files(calendar_urls)
        self.set_events(filter_and_sort_events(downloaded_event_list))

    def _get_local_events(self):
        collected_ics_events = read_ics_file(ics_file_path)
        self.set_events(filter_and_sort_events(collected_ics_events))

    def _remove_event_list(self):
        self.set_events([])

    def _update_checkboxes(self):
        # Clear existing checkboxes
        for checkbox in self.checkboxes:
            checkbox.destroy()

        self.checkboxes = []

        # Recreate checkboxes for each event
        self.event_vars = [tk.BooleanVar(self.root, value=True) for _ in self.events]
        for i, event in enumerate(self.events):
            checkbox = ttk.Checkbutton(self.checkbox_frame, text=event.format_event_to_readable_string(),
                                       variable=self.event_vars[i])
            checkbox.pack(anchor=tk.W)
            self.checkboxes.append(checkbox)

        # Update canvas scroll region
        self.canvas.update_idletasks()  # Ensure all widgets are updated
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def set_events(self, events):
        self.events = events
        self._update_checkboxes()
