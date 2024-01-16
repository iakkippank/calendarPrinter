class Event:
    def __init__(self, month, week_of_year, start_date, end_date, summary):
        self.month = month
        self.week_of_year = week_of_year
        self.start_date = start_date
        self.end_date = end_date
        self.summary = summary

    def __str__(self):
        return f"Event: {self.summary}\nMonth: {self.month}\nWeek: {self.week}\nStart Date: {self.start_date}\nEnd Date: {self.end_date}"
