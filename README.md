
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

## Parsing files
#### JsonLoader
```python
from koro.dataset import JsonLoader

reader = JsonLoader()
# Root is pinned to raw_datasets/
# This means your provided path should be relative to that directory
stops = reader.load_file('static/stops.json')
```

#### CsvLoader
```python
from koro.dataset import CsvLoader

reader = CsvLoader()
# Or a list of custom headers. This affects the key you'll access the CSV
# reader = CsvLoader(['year_month']) 
entries = reader.load_file('relative-path.csv')
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

## Formatting code
- `pip install black`
- `python -m black .`
