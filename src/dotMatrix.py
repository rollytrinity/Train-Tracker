import time
import pandas as pd
from rich.console import Console
from rich.live import Live
from rich.table import Table

from config import STATION_CODE, PLATFORM_NUMBER


def import_csv(path):
    return pd.read_csv(path)


def parseData(data):
    data["Platform"] = data["Platform"].astype(int)
    data = data[data["Platform"] == PLATFORM_NUMBER].head(5)

    return [
        {
            "time": row["Train Time"],
            "dest": row["Destination"],
            "stops": row["Stops"],
        }
        for _, row in data.iterrows()
    ]


def scrolling_text(text, offset, width):
    padded = text + "   "
    offset %= len(padded)
    return padded[offset : offset + width]


console = Console()
data = import_csv(f"../output/{STATION_CODE}_departures.csv")
rows = parseData(data)

scroll_offsets = [0] * len(rows)
SCROLL_WIDTH = 40

with Live(console=console, refresh_per_second=10) as live:
    while True:
        table = Table(show_header=True, header_style="bold")
        table.add_column("Time", width=6)
        table.add_column("Destination", width=18)
        table.add_column("Stops")

        for i, row in enumerate(rows):
            stops = scrolling_text(row["stops"], scroll_offsets[i], SCROLL_WIDTH)
            scroll_offsets[i] += 1

            table.add_row(
                row["time"],
                row["dest"],
                stops,
            )

        live.update(table)
        time.sleep(0.1)
