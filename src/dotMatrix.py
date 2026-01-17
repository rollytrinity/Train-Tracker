import pandas as pd
import tkinter as tk
from config import STATION_CODE
from config import PLATFORM_NUMBER


num_to_place = {1: '1st', 2: '2nd', 3: '3rd', 4: '4th', 5: '5th'}

def import_csv(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error importing CSV: {e}")
        return None

def parseData(data):
    display = []

    data['Platform'] = data['Platform'].astype(int)
    data = data[data['Platform'] == PLATFORM_NUMBER]
    data.reset_index(drop=True, inplace=True)

    for index, row in data.iterrows():
        if index == 5:
            break

        entry = {'Pos': str(index+1),
                    'Train Time': row['Train Time'],
                    'Destination': row['Destination'],
                    'Stops': row['Stops']}
        display.append(entry)

    return display


# set up
if __name__ == "__main__":
    window = tk.Tk()
    window.title("Railboard")
    window.geometry("1000x200")

    data = import_csv(f"../output/{STATION_CODE}_departures.csv")

    if data is not None:
        display_data = parseData(data)

        for i, entry in enumerate(display_data):
            info = f"{entry['Pos']}: {entry['Train Time']} to {entry['Destination']} \nStops: {entry['Stops']}\n"
            label = tk.Label(window, text=info, font=("Helvetica", 14), justify="left", anchor="w")
            label.pack(fill='x', padx=20, pady=10)

    window.mainloop()