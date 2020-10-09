#!/bin/bash

toMangle=("transport_node_bus_202006.csv" \
    "transport_node_bus_202007.csv" \
    "transport_node_bus_202008.csv" \
    "transport_node_train_202006.csv" \
    "transport_node_train_202007.csv" \
    "transport_node_train_202008.csv")

for filename in ${toMangle[@]}; do
    echo "Sorting for ${filename}"
    awk 'NR==1; NR > 1 {print $0 | "sort --field-separator=, --numeric-sort --reverse --key=6"}' $filename > mangledx/"BY_TAPIN_${filename}"
    awk 'NR==1; NR > 1 {print $0 | "sort --field-separator=, --numeric-sort --reverse --key=7"}' $filename > mangledx/"BY_TAPOUT_${filename}"
done
