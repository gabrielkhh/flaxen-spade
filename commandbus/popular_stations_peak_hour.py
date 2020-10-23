from koro.dataset import CsvLoader, JsonLoader
from koro.resolve import TrainStationFactory
import csv

results = {}
six_list = []
seven_list = []
eight_list = []

def run():
    reader = CsvLoader()
    entries = reader.load_file("od/mangled/BY_TAPOUT_transport_node_train_202008.csv")

    for entry in entries:
        station = entry["PT_CODE"]
        hour = entry["TIME_PER_HOUR"]
        tap_out = entry["TOTAL_TAP_OUT_VOLUME"]

        # AM peak --> 6am - 9am
        if entry["DAY_TYPE"] == "WEEKDAY":
            if hour in ['6', '7', '8']:
                station_obj = TrainStationFactory.load_station(station)
                station_name = station_obj.name
                # results.append({"hour": hour, "station": station, "station_name": station_name, "tap_out": tap_out})
                if hour == '6':
                    six_list.append({"hour": hour, "station": station, "station_name": station_name, "tap_out": tap_out})
                elif hour == '7':
                    seven_list.append({"hour": hour, "station": station, "station_name": station_name, "tap_out": tap_out})
                elif hour == '8':
                    eight_list.append({"hour": hour, "station": station, "station_name": station_name, "tap_out": tap_out})

    results["6"] = six_list[:3]
    results["7"] = seven_list[:3]
    results["8"] = eight_list[:3]

    hour_dict = {}
    outer_list = []
    # result_list = []
    # print(results["7"])

    for index in range(6,9):
        result_list = []
        for data in results[str(index)]:
            result_dict = {"code": data["station"], "tap_out": data["tap_out"], "name": data["station_name"]}
            result_list.append(result_dict)

        # hour_dict[index] = result_list

        outer_list.append({"hour": index, "stations": result_list})

    print(outer_list)
    # print('\n'.join(map(str, results[:9])))

"""          
        elif entry['TIME_PER_HOUR'] == '7':
            results.append({"hour": hour, "station": station, "tap_out": tap_out})
        elif entry['TIME_PER_HOUR'] == '8':
            results.append({"hour": hour, "station": station, "tap_out": tap_out})
        # PM peak --> 5pm - 7pm
        elif entry['TIME_PER_HOUR'] == '17':
            results.append({"hour": hour, "station": station, "tap_out": tap_out})
        elif entry['TIME_PER_HOUR'] == '18':
            results.append({"hour": hour, "station": station, "tap_out": tap_out})
"""













"""
        if station in results:
            results[station] = {
                "weekday:[]",
                "weekend:[]"
                }
        if len(results[station]["weekend"]) < 3 and entry['DAY_TYPE'] == 'WEEKENDS/HOLIDAY':
            results[station]["weekend"].append({"hour": hour, "tap_out": tap_out})
        print(results[station]["weekend"])
        if row['TIME_PER_HOUR'] == '6':
            print(row['TOTAL_TAP_OUT_VOLUME'])
                #print(row['TOTAL_TAP_OUT_VOLUME'])
    # row YEAR_MONTH, DAY_TYPE, TIME_PER_HOUR, PT_TYPE, PT_CODE, TOTAL_TAP_IN_VOLUME, TOTAL_TAP_OUT_VOLUME
        year_month = str(row[0])
        day_type = str(row[1])
        time_hour = str(row[2])
        pt_type = str(row[3]) #train
        pt_code = str(row[4]) #ew21/ns1
        total_tapin = str(row[5])
        total_tapout = str(row[6])
        data.append([year_month,day_type, time_hour,pt_type,pt_code,total_tapin,total_tapout])
"""
