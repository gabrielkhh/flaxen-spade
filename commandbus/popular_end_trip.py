from koro.dataset import CsvLoader, JsonLoader
from koro.manipulation import dataset_path
from tabulate import tabulate
import json

def end_trip():
     reader = CsvLoader(delimiter=",")
     format_of_file = "od/mangled/BY_TAPIN_transport_node_train_2020{}.csv"
     final = {}
     for month in ["06", "07", "08"]:
          file = format_of_file.format(month)
          
               
          tapin_entries = reader.load_file(file)
          results = {}

          for entry in tapin_entries:
               pt_code = entry['PT_CODE']
               stat_hr = entry['TIME_PER_HOUR']
               day_type = entry['DAY_TYPE']
               tap_in = entry['TOTAL_TAP_IN_VOLUME']
               tap_out = entry['TOTAL_TAP_OUT_VOLUME']

               if pt_code not in results:
                    results[pt_code] = {
                               "weekend": [],
                               "weekday": []
                               }
               if len(results[pt_code]["weekend"]) < 5 and day_type == 'WEEKENDS/HOLIDAY':
                    if stat_hr in ('21','22','23','0'):
                         results[pt_code]["weekend"].append({"hour": stat_hr, "tap_in": tap_in, "tap_out": tap_out})
                         
               if len(results[pt_code]["weekday"]) < 5 and day_type == 'WEEKDAY':
                    if stat_hr in ('21','22','23','0'):
                         results[pt_code]["weekday"].append({"hour": stat_hr, "tap_in": tap_in, "tap_out": tap_out})
                         print (tabulate([["pt_code", "day_type", "stat_hr", "tap_in", "tap_out"],[pt_code, day_type, stat_hr, tap_in, tap_out]], headers="firstrow"))
          final[month] = results
     with open(dataset_path("results/popular_end_trip.json"), "w+") as file:
          json.dump(final, file)

