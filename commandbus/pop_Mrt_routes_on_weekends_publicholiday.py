from tabulate import tabulate
from koro.dataset import CsvLoader
from itertools import islice
from koro.manipulation import dataset_path
import json


def run():
    reader = CsvLoader(delimiter = ",")

    tapin = reader.load_file("large/origin_destination_train_202008.csv")


    result = {}

    mysort = filter(lambda x: x["DAY_TYPE"] == "WEEKENDS/HOLIDAY" ,tapin)
    mysort = list(islice(sorted(tapin, key=lambda x: int(x["TOTAL_TRIPS"]),reverse=True),50))

    for entry in mysort:
        day = entry["DAY_TYPE"]
        time = entry["TIME_PER_HOUR"]
        start = entry["ORIGIN_PT_CODE"]
        end = entry["DESTINATION_PT_CODE"]
        totaltrip = entry["TOTAL_TRIPS"]
        if f"{start}:{end}" not in result:
            result[f"{start}:{end}"]={
                 "weekend":[]
            }
        result[f"{start}:{end}"]["weekend"].append({"start":start,"end":end , "time":time, "totaltrip":totaltrip})

    print(result)

    with open(dataset_path("results/pop_mrt_routes_on_weekends_publicholiday.json"), "w+") as file:
        json.dump(result, file)
