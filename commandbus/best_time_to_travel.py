

from koro.dataset import CsvLoader
from koro.manipulation import dataset_path
import json

def run():
    reader = CsvLoader(delimiter=",")

    entries = reader.load_file("od/mangled/BY_TAPIN_transport_node_train_202008.csv")

    results={}

    for entry in reversed(entries):
        station = entry["PT_CODE"]
        hour = entry["TIME_PER_HOUR"]
        tap_in = entry["TOTAL_TAP_IN_VOLUME"]
        tap_out = entry["TOTAL_TAP_OUT_VOLUME"]
        if station not in results:
            results[station] = {
                "weekend":[],
                "weekday":[]
                }
            
        if len(results[station]["weekend"]) < 5 and entry['DAY_TYPE'] == 'WEEKENDS/HOLIDAY':
            if hour not in ('22','23','0'):
                results[station]["weekend"].append({"hour": hour,"tap_in": tap_in, "tap_out": tap_out})
             
        if len(results[station]["weekday"]) < 5 and entry['DAY_TYPE'] == 'WEEKDAY':
            if hour not in ('22','23','0'):
                results[station]["weekday"].append({"hour": hour,"tap_in": tap_in, "tap_out": tap_out})

    print(results)

    with open(dataset_path("results/best_time_to_travel.json"),"w+") as file:
        json.dump(results,file)
