## Summary
Our datasets are static. What we need to do is create "tasks", simple scripts that read in some data, does some computing and spits out a result as a JSON file. To fulfill a task
- Create a new file under the [`commandbus/`](https://github.com/ict1002-42/flaxen-spade/blob/master/commandbus/my_first_task.py) folder. You should define a method that will be called (e.g. run())
- Register your command with the app in [`cli.py`](https://github.com/ict1002-42/flaxen-spade/blob/master/cli.py#L43)
- Run the command with `python -m flask task {your-command-name}`

## Testing out code
You can easily test out code by running the interactive shell. Run `python -m flask konch`.

## How to write tasks

### Detailed flow

#### commandbus
You'll first need to create a new python file under `commandbus/`. Don't be afraid to pick a long name, it should be descriptive and unique (find_nearby_bus_stops_for_all_polytechnics.py).

#### Entry point
Next, you'll need an entry point to your *task*. A simple [run()](https://github.com/ict1002-42/flaxen-spade/blob/master/commandbus/my_first_task.py) will do. We will call this method from `cli.py`

#### Register command
Head to `cli.py` and something like this to the end of the file. What you'll do here is define the name of your command with the decorator (in this example, our command is testcommand). Next, we'll locally import your newly created file under commandbus and call the `run()` method we defined earlier.

You'll be able to call this command by running `python -m flask task testcommand`.

```python
@t.cli.command("testcommand")
def my_test_command():
    """Whatever you write here will show up in the CLI help menu"""
    from commandbus import my_first_task
    my_first_task.run()
```

#### Arguments and parameters
With click, you can easily accept different types of arguments. Checkout the [documentation](https://click.palletsprojects.com/en/7.x/) for what you can do. Here are some common examples.

```python
@t.cli.command("testcommand")
@click.option("--limit", help="The distance we want to limit our search", prompt="Limit")
def my_test_command(limit):
    """Whatever you write here will show up in the CLI help menu"""
    from commandbus import my_first_task
    my_first_task.run()
```

This command will now prompt you for a limit. Alternatively, you can specify it when calling the command (`python -m flask task testcommand --limit 20`). Either way, you'll receive it as a normal python parameter which you can pass on to your `run()` function.

## Reading datasets
Use the JsonLoader/CsvLoader under `koro.dataset` to load your files. The path is relative to `raw_datasets`, so you'll only need to provide a path based on that.

For example, if I want to load the stops.json which is under raw_datasets/static/stops.json, I'll specify `reader.load_file("static/stops.json")`. 

```python
from koro.dataset import CsvLoader

reader = CsvLoader()
tap_in = reader.load_file("od/mangled/BY_TAPIN_transport_node_bus_202006.csv")
for line in tap_in:
    print(line["TOTAL_TAP_OUT_VOLUME"]) # every "TOTAL_TAP_OUT_VOLUME" field
```


## Writing Files/Saving results
```python
from koro.manipulation import dataset_path
import json

# ... do some processing

with open(dataset_path("results/my-results.json", "w+")) as file:
   json.dump(my_dictionary_or_list_of_results, file)
```
