# English Dog Breed Names
Scrapes <https://www.fci.be> and <https://www.thekennelclub.org.uk> for all internationally recognised dog breeds in their English name and group.

## Installation
* (Optional, recommended) Create a python virtual environment
    ```bash
    python3 -m venv venv
    ```
* Install requirements
    ```bash
    pip install -r requirements.txt
    ```

## Running

### Fetch FCI Breeds and Groups

```
usage: get_fci_data.py [-h] [destination]

positional arguments:
  destination  Output file to write contents to. stdout if not specified

optional arguments:
  -h, --help   show this help message and exit

```

### Get KC Groups for each Breed
