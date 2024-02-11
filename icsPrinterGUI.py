import tkinter as tk
from tkinter import ttk
from data.Event import Event as DateEvent
from utils.htmlUtils import generate_html_table, pretty_save_html


def show_app_window(events: list[DateEvent]):
    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_configure(event):
        # Update scroll region to fit the entire canvas
        canvas.configure(scrollregion=canvas.bbox("all"))

    def show_selected_events():
        selected_events = [events[i] for i, var in enumerate(event_vars) if var.get()]
        # Make user prompt to select events
        # selected_events = show_selection_prompt(sorted_events)
        # Group the events and generate the HTML table
        html_table = generate_html_table(selected_events)
        # Save the HTML table
        pretty_save_html(html_table)
        root.destroy()

    # Create the main window
    root = tk.Tk()
    root.title("Event Selector")

    # Import the tcl file
    root.tk.call('source', 'forest-dark.tcl')

    # Set the theme with the theme_use method
    ttk.Style().theme_use('forest-dark')

    settings_lframe = ttk.LabelFrame(root, text="Einstellungen")
    selection_frame = ttk.Frame(root, height=1500)
    event_list_lframe = ttk.LabelFrame(selection_frame, height=1000, text="Eingetragene Veranstaltungen")

    settings_lframe.pack(side=tk.LEFT, fill=tk.Y, expand=False, pady=10, padx=10)
    selection_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    event_list_lframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10, padx=10)

    # Create a canvas
    canvas = tk.Canvas(event_list_lframe)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create a frame inside the canvas to hold the list of checkboxes
    checkbox_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=checkbox_frame, anchor=tk.NW)

    # Configure canvas scrolling
    checkbox_frame.bind("<Configure>", on_configure)
    canvas.bind("<Configure>", on_configure)
    canvas.bind_all("<MouseWheel>", on_mouse_wheel)  # Bind mouse wheel scroll event

    # Create variables to track checkbox states
    event_vars = [tk.BooleanVar(root, value=True) for _ in events]

    # Create checkboxes for each event and pack them into the frame
    for i, event in enumerate(events):
        checkbox = ttk.Checkbutton(checkbox_frame, text=event.format_event_to_readable_string(), variable=event_vars[i])
        checkbox.pack(anchor=tk.W)

    # Create a scrollbar and attach it to the canvas
    scrollbar = ttk.Scrollbar(event_list_lframe, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Button to select events
    download_button = ttk.Button(settings_lframe, text="Download Events", command=show_selected_events)
    select_button = ttk.Button(selection_frame, text="Select Events", command=show_selected_events )
    select_button.pack(side=tk.BOTTOM, pady=10, padx=10)
    download_button.pack(pady=10,padx=10)

    # Start the GUI event loop
    root.mainloop()
