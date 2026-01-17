import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

## edit station code here
station_code = "EDB"

url = "https://www.realtimetrains.co.uk/search/simple/gb-nr:" + station_code


def extract_departures(soup):

    # get all train departure entries
    departures = soup.find_all('a', class_='service')

    train_info = pd.DataFrame(columns=['Train Time', 'Destination', 'Status', 'Number of Coaches', 'Platform'])
    regex = r'^(\d{4})([A-Za-z ]+?)(At platform|Starts here|On time)([A-Za-z ]+?)\s*·\s*(\d+)\s+coaches(\d+)$'

    # clean
    for departure in departures:
        train_info_text = departure.get_text()
        match = re.match(regex, train_info_text)
        if match:
            train_time = match.group(1)[:2] + ':' + match.group(1)[2:]
            destination = match.group(2).strip()
            status = match.group(3)
            additional_info = match.group(4).strip()
            num_coaches = match.group(5)
            platform = match.group(6)

            new_row = pd.DataFrame({
                'Train Time': [train_time],
                'Destination': [destination],
                'Status': [status],
                'Additional Info': [additional_info],
                'Number of Coaches': [num_coaches],
                'Platform': [platform]
            })
            train_info = pd.concat([train_info, new_row], ignore_index=True)


    return train_info


def record_to_csv(train_info, station_code):
    filename = f"{station_code}_departures.csv"
    train_info.to_csv(filename, index=False)
    print(f"Train departure information saved to {filename}")


def main():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    train_info = extract_departures(soup)
    record_to_csv(train_info, station_code)

if __name__ == "__main__":
    main()