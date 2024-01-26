from printerio.printerConfig import calendar_urls
from utils.icsUtils import download_ics_files
from utils.userInputUtils import shouldDownloadIcs

if shouldDownloadIcs():
    download_ics_files(calendar_urls)
