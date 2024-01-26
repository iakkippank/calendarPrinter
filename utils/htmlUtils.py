from bs4 import BeautifulSoup as bs
from printerio.printerConfig import output_file_path

def pretty_save_html(html_string : str):
    soup = bs( html_string, features= "html.parser")    #make BeautifulSoup
    pretty_html = soup.prettify()                       #prettify the html
    with open(output_file_path, 'w', encoding="utf-8") as html_file:
        html_file.write(pretty_html)