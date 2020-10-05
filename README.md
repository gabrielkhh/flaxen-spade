
## Getting Started [![Build Status](https://travis-ci.com/ict1002-42/flaxen-spade.svg?token=BJzzpiVHKm2chRHcywxY&branch=master)](https://travis-ci.com/ict1002-42/flaxen-spade)
`git clone https://github.com/ict1002-42/flaxen-spade`


### Installing dependencies
#### With Poetry
`poetry install`

#### or pip
`pip install -r requirements.txt`

### Dev
- `poetry shell` (If you aren't in an venv  already.)
- `cp .env.example .env` (secrets and config goes here)
- `flask run`

## How-tos

# Parsing files
#### JsonLoader
```python
from koro.dataset import JsonLoader

reader = JsonLoader()
# Root is pinned to raw_datasets/
# This means your provided path should be relative to that directory
stops = reader.load_file("static/stops.json")
```

#### CsvLoader
```python
from koro.dataset import CsvLoader

reader = CsvLoader()
# Or a list of custom headers. This affects the key you'll access the CSV
# reader = CsvLoader(['year_month']) 
entries = reader.load_file("relative-path.csv")
for entry in entries:
    print(f"All taps: {entry['TAP_OUT_VOLUME']}")
```

#### Haversine: Distance between two points on earth
```python
from koro.geo import haversine

location1 = (25.0010, 136.9987)
location2 = (25.0, 71.0)
in_kilometers = haversine(location1, location2)
```

### Geocoding
```python
from koro.geo import resolve_coordinates

resolve_coordinates('changi airport') # {'lat': 1.3384, 'lng': 103.984}
```

### Bus Arrivals
```python
from koro.datamall import Datamall, Seat

arrivals = Datamall().bus_arrivals("10018")
print(arrivals.bus_stop_code) # "10018"
onetwofour = arrivals.get_service('124')

onetwofour.origin # instance of Stop, see below
onetwofour.origin.name # 'HarbourFront Int'
onetwofour.destination # ditto
onetwofour.destination.name # "St. Michael's Ter"

onetwofour.arriving # instance of pendulum, see https://pendulum.eustace.io/docs/
onetwofour.arriving_at # 'in 2 minutes'
onetwofour.is_wheelchair_accessible() # True

if onetwofour.get_seating(0) == Seat.AVAILABLE: # Seat.AVAILABLE
    # Seating available
    pass

onetwofour.get_location(1) # (1.279004, 103.8386425)

# Raw json
onetwofour.payload

# These methods accept an index, all defaults to 0 (the next bus)
onetwofour.get_bus_by_key(1) # access NextBus, NextBus2, NextBus3 by normal int indexes
onetwofour.get_next_bus() # same as get_bus_by_key(0)
onetwofour.get_arrival(1) # same as arriving
onetwofour.get_friendly_arrival(1) # same as arriving_at
```

### Stops
```python
from koro.resolve import StopFactory

stop = StopFactory.load_stop("10018")
stop.name # 'Outram Pk Stn Exit F/SGH'
stop.latitude # 1.27900819665099
stop.longitude # 103.83860360621959
stop.stop_code # 10018
stop.stop_data # raw data from json file
```

## Formatting code
- `pip install black`
- `python -m black .`
