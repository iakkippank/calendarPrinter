from datetime import datetime, date


class Event:
    def __init__(self, year, month, week_of_year, start_date : date, end_date, summary):
        self.week_of_year = year
        self.month = month
        self.week_of_year = week_of_year
        self.start_date = start_date
        self.end_date = end_date
        self.summary = summary

    def __lt__(self, other):
        # Comparison based on start_date
        return self.start_date < other.start_date
