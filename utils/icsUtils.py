import icalendar
import requests


def download_ics_files(urls, save_path):
    combined_calendar = icalendar.Calendar()
    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            calendar_data = response.text.encode('utf-8')
            calendar = icalendar.Calendar.from_ical(calendar_data)
            combined_calendar.subcomponents += calendar.subcomponents
            print(f"Downloaded and combined events from {url}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading the file from {url}: {e}")
        except Exception as e:
            print(f"Error processing the file from {url}: {e}")

    try:
        with open(save_path, 'wb') as f:
            f.write(combined_calendar.to_ical())
        print(f"Combined calendar saved successfully at: {save_path}")
    except Exception as e:
        print(f"Error saving the combined calendar: {e}")


save_path = "combined_calendar.ics"
