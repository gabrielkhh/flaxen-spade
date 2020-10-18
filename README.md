
## Getting Started [![Build Status](https://travis-ci.com/ict1002-42/flaxen-spade.svg?token=BJzzpiVHKm2chRHcywxY&branch=master)](https://travis-ci.com/ict1002-42/flaxen-spade)
### Clone repo
`git clone https://github.com/ict1002-42/flaxen-spade`

#### Initial Dev setup
- `pip install -r requirements.txt` - Install dependencies
- `cp .env.example .env` (secrets and config goes here)
- `python -m flask run` - Run the web server
- `python -m flask` - See available commands

### Optional
- `poetry shell` - Activate virtualenv
- `flask konch` - Interactive REPL

Checkout the [workflow](FLOW.md) guide for more detail info about writing tasks. Checkout the [pull request](DEVELOP.md) guide for making changes.

## Configuration
`.env` stores your configurations. You can configure the datamall endpoint here.
- https://dmall.mkb.moe (School wifi blocks this domain)
- https://dmall.amatsuka.me 

### Formatting code
- `pip install black`
- `python -m black .`

# How-tos

## Paths
This ensures you'll always referencing the same files regardless of your current/script directory. You'll usually use it when writing results out.
```python
from koro.manipulation import dataset_path

# Returns a fully qualified path to "raw_datasets/large/origin_destination_bus_202006.csv"
full_path = dataset_path("large/origin_destination_bus_202006.csv")
full_path_too = dataset_path("large", "origin_destination_bus_202006.csv") # ditto
with open(full_path) as file:
    # ...
```

## Parsing files
### JsonLoader
```python
from koro.dataset import JsonLoader

reader = JsonLoader()
# Root is pinned to raw_datasets/ already
# This means your provided path should be relative to that directory
stops = reader.load_file("static/stops.json")
stops["10009"]["name"] # Bt Merah Int
```

### CsvLoader
```python
from koro.dataset import CsvLoader

# You can usually leave out the delimiter if you're working with comma separated values
# odd ones like some of the LTA datasets use \t for some files
reader = CsvLoader(delimiter=",")
entries = reader.load_file("merged/train-data.csv")
for entry in entries:
    print(entry["station_code"])
```

## Geo
### Haversine: Distance between two points on earth
```python
from koro.geo import haversine

# Latitude, Longitude
location1 = (25.0010, 136.9987)
location2 = (25.0, 71.0)
in_kilometers = haversine(location1, location2)
```

### Reverse geocoding
```python
from koro.geo import resolve_coordinates

resolve_coordinates('changi airport') # {'lat': 1.3384, 'lng': 103.984}
```

### Nearest
```python
from koro.geo import Nearest

train = Nearest()

# Get the closest train stations within 2km of this location
list_of_trains = train.location("changi airport").train_station(limit=2) # sorted by distance, [0] = closest, [-1] furthest

closest_train = list_of_trains[0] # Tuple of (distance_in_km, Instance of TrainStation)
closest_train[0] # Distance in km
closest_train[1].code # CG1
closest_train[1].name # Changi Airport

bus = Nearest()

# You can pass in a raw lat/long instead
list_of_buses = bus.raw_location(latitude, longitude)

list_of_buses = bus.location("changi airport").bus_stop(0.5)
closest_bus = list_of_buses[0] # Tuple of (distance_in_km, Instance of Stop)
closest_train[0] # Distance in km
closest_bus[1].name # Changi Airport PTB3
closest_bus[1].stop_code # 95109
```

## Transport
### Train Stations
```python
from koro.resolve import TrainStationFactory

# Case insensitive
station = TrainStationFactory.load_station("NS1") # an instance of TrainStation
station.code # NS1
station.name # Jurong East
station.line # North South Line
station.latitude # '1.333115'
station.longitude # '103.742297'
```

#### Combined Station codes
Most of the datasets for train data contain "combined" train codes. You should split them with `.split()` and pass either one of them to `load_station`.

```python
ne_seven = "NE7/DT12".split("/")[0] # "NE7"
dt_twelve = "NE7/DT12".split("/")[1] # "DT12"
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

### Bus Service
```python
from koro.resolve import BusServiceFactory

service = BusServiceFactory.load_service("812")
service.bus_service_code # 812
service.stops # List (1st route, 2nd route if any), each containing an instance of "Stop" (see above)
service.points # List (1st route, 2nd route if any), each containing a tuple of (lat, long) (Used for passing to charting frontend)
service.polyline # List of list of two floats [lat, long]. Used for passing to frontend rendering.
```
