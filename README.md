
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


## Formatting code
- `pip install black`
- `python -m black .`
