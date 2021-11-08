from lxml import html
from tqdm import tqdm

import argparse
import requests

# Constants
BASE_URL = "http://www.fci.be"

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

BREED_UL_LIST_PATH_X_PATH = "//*[@id=\"page\"]/div[2]/div[1]/ul/li/a"

ENGLISH_NAME_X_PATH = "//*[@id=\"ContentPlaceHolder1_NomEnLabel\"]"

OUT_FILE = "all_dogs.txt"

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("destination", nargs="?", help="Output file to write contents to. stdout if not specified")

args = parser.parse_args()

if __name__ == "__main__":

    res = []

    alphabet_pbar = tqdm(ALPHABET)

    for init in alphabet_pbar:
        alphabet_pbar.set_description(f"Getting listings for dogs beginning with {init}")

        page = requests.get(f"{BASE_URL}/en/nomenclature/races.aspx?init={init}")

        breeds = html.fromstring(page.content).xpath(BREED_UL_LIST_PATH_X_PATH)

        breeds_pbar = tqdm(breeds)

        for breed in breeds_pbar:
            breeds_pbar.set_description(f"Getting English name for {breed.text_content()}")
            subpage = requests.get(f"{BASE_URL}{breed.attrib['href']}")

            eng_name = html.fromstring(subpage.content).xpath(ENGLISH_NAME_X_PATH)[0].text_content()

            res.append(eng_name.title())

    # Report results
    if args.destination is None:
        print("\n".join(sorted(res)))

    else:
        with open(args.destination, "w") as f:
            f.write("\n".join(sorted(res)))
            print(f"Results written to {OUT_FILE}")
