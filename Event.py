from datetime import datetime, date, timedelta


class Event:
    def __init__(self, year, month, week_of_year, start_date : date, end_date, location, summary):
        self.year = year
        self.month = month
        self.week_of_year = week_of_year
        self.start_date = start_date
        self.end_date = end_date
        self.location = location
        self.summary = summary

    def __lt__(self, other):
        # Comparison based on start_date
        return self.start_date < other.start_date

    def format_event(self):
        # Deutsche Wochentage
        german_weekdays = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]

        start_time = self.start_date.strftime("%H:%M")
        end_time = self.end_date.strftime("%H:%M")
        german_weekday = german_weekdays[self.start_date.weekday()]
        formatted_date = self.start_date.strftime(f"{german_weekday} %d.%m")

        return f"{formatted_date}\n{start_time} - {end_time}"

    def format_german_month(self):
        # Deutsche Wochentage
        german_months = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]
        return german_months[self.start_date.month]

    def calculate_week_range(self):
        # Assuming week starts from Monday
        start_of_week = self.start_date - timedelta(days=self.start_date.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        start_of_week_string = start_of_week.strftime(f"%d.%m")
        end_of_week_string = end_of_week.strftime(f"%d.%m")
        return f"Von {start_of_week_string}<BR><b>KW{self.week_of_year}</b><BR>Bis {end_of_week_string} "