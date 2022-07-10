import argparse
import requests

from collections import namedtuple
from lxml import html
from tqdm import tqdm

from typing import Optional

# Types
Breed = namedtuple("Breed", ["name", "group"])

# Constants
BASE_URL = "http://www.fci.be"

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

BREED_UL_LIST_PATH_X_PATH = '//*[@id="page"]/div[2]/div[1]/ul/li/a'

ENGLISH_NAME_X_PATH = '//*[@id="ContentPlaceHolder1_NomEnLabel"]'

GROUP_X_PATH = '//*[@id="ContentPlaceHolder1_GroupeHyperLink"]'


def print_results(breeds: list[Breed], outfile: Optional[str]):
    # Report results
    header = "Name, Group\n"
    format_gen = (f"{b.name}, {b.group}\n" for b in sorted(breeds))

    if outfile is None:
        print(header, end="")
        for l in format_gen:
            print(l, end="")
    else:
        with open(outfile, "w") as f:
            f.write(header)
            f.writelines(format_gen)
            print(f"Results written to {outfile}")


if __name__ == "__main__":
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "destination",
        nargs="?",
        help="Output file to write contents to. stdout if not specified",
    )

    args = parser.parse_args()

    res = []

    alphabet_pbar = ALPHABET if args.destination is None else tqdm(ALPHABET)

    for init in alphabet_pbar:
        if args.destination is not None:
            alphabet_pbar.set_description(
                f"Getting listings for dogs beginning with {init}"
            )

        page = requests.get(f"{BASE_URL}/en/nomenclature/races.aspx?init={init}")

        breeds = html.fromstring(page.content).xpath(BREED_UL_LIST_PATH_X_PATH)

        breeds_pbar = breeds if args.destination is None else tqdm(breeds)

        for breed in breeds_pbar:
            if args.destination is not None:
                breeds_pbar.set_description(
                    f"Getting English name for {breed.text_content()}"
                )
            subpage = requests.get(f"{BASE_URL}{breed.attrib['href']}")

            tree = html.fromstring(subpage.content)
            eng_name = tree.xpath(ENGLISH_NAME_X_PATH)[0].text_content()

            group = tree.xpath(GROUP_X_PATH)[0].text_content()
            group = group[group.index("-") + 2 :]

            res.append(Breed(eng_name.title(), group))

    print_results(res, args.desination)
