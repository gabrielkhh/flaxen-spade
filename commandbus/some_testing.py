from koro.manipulation import dataset_path
from koro.dataset import JsonLoader
from koro.dataset import CsvLoader

# dataset_path("large/transport_node_train_202008.csv")

def run_test():
    reader = CsvLoader()
    entries = reader.load_file("large/transport_node_train_202008.csv")

    count = 0

    for entry in entries:
        count += 1
        print(f"All taps: {entry['TOTAL_TAP_OUT_VOLUME']} and count is %d" % count)
