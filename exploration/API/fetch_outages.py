import csv
import json
import time
from pathlib import Path
from .http import cached_get

START_URL = "https://openenergyhub.ornl.gov//api/explore/v2.1/catalog/datasets/oe-417-annual-summaries/records?limit=40&offset="
CSV_COLUMNS = ("event_month", "date_event_began", "time_event_began",
               "date_of_restoration", "time_of_restoration", "area_affected",
               "nerc_region", "alert_criteria", "event_type", "demand_loss_mw",
               "number_of_customers_affected")

def build_outages_csv(output_filename: Path):
    """
    Create a CSV file.

    Parameters:
        output_filename: Path object representing location to write file.
    """

    #make "data" list
    data = []
    records = 0

    #record limit is 40 and there are 341 records total
    #so we want the last request page to be 320-341
    while records <= 320:
        time.sleep(1)
        outtext = cached_get(START_URL, records)
        outjson = json.loads(outtext)

        for outage in outjson["results"]:
            odt = {key: outage.get(key, None) for key in CSV_COLUMNS}
            data.append(odt)
            records += 1

    with open(output_filename, mode='w', newline="") as file:
        writer = csv.DictWriter(file, fieldnames= CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(data)

    return