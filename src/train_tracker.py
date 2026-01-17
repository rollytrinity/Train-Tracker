import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from config import STATION_CODE

url = "https://www.realtimetrains.co.uk/"

def extract_stops(train_url):
    response = requests.get(url + train_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    stops = soup.find_all('a',  class_='name')

    stop_names = [stop.get_text().strip()[3:] for stop in stops]
    stops = ", ".join(stop_names)

    return stops


def extract_departures(soup):

    # get all train departure entries
    departures = soup.find_all('a', class_='service', href=True)

    train_info = pd.DataFrame(columns=['Train Time', 'Destination', 'Provider', 'Status', 'Number of Coaches', 'Platform', 'Stops'])
    regex = r'^(\d{4})([A-Za-z ]+?)(At platform|Starts here|On time)([A-Za-z ]+?)\s*·\s*(\d+)\s+coaches(\d+)$'

    # clean
    for departure in departures:
        stops =extract_stops(departure['href'])

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
                'Provider': [additional_info],
                'Number of Coaches': [num_coaches],
                'Platform': [platform],
                'Stops': [stops]
            })
            train_info = pd.concat([train_info, new_row], ignore_index=True)

    return train_info


def record_to_csv(train_info):
    filename = f"./output/{STATION_CODE}_departures.csv"
    train_info.to_csv(filename, index=False)
    print(f"Train departure information saved to {filename}")


def main():
    response = requests.get(url + 'search/simple/gb-nr:' + STATION_CODE)
    soup = BeautifulSoup(response.text, 'html.parser')

    train_info = extract_departures(soup)
    record_to_csv(train_info)

if __name__ == "__main__":
    main()