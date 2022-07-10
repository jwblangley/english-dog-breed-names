import argparse
import requests

from collections import namedtuple
from lxml import html
from tqdm import tqdm

from typing import Generator, Iterator, Optional

# Types
Breed = namedtuple("Breed", ["name", "group"])

# Constants
BASE_URL = "http://www.fci.be"

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

BREED_UL_LIST_PATH_X_PATH = '//*[@id="page"]/div[2]/div[1]/ul/li/a'

ENGLISH_NAME_X_PATH = '//*[@id="ContentPlaceHolder1_NomEnLabel"]'

GROUP_X_PATH = '//*[@id="ContentPlaceHolder1_GroupeHyperLink"]'


def _breeds_url_from_listing_page(page_content: str) -> list[tuple[str, str]]:
    elems = html.fromstring(page_content).xpath(BREED_UL_LIST_PATH_X_PATH)
    return [(breed.text_content(), breed.attrib["href"]) for breed in elems]


def _breed_from_page(page_content: str) -> Breed:
    tree = html.fromstring(page_content)
    eng_name = tree.xpath(ENGLISH_NAME_X_PATH)[0].text_content()

    group = tree.xpath(GROUP_X_PATH)[0].text_content()
    group = group[group.index("-") + 2 :]
    return Breed(eng_name.title(), group)


def print_results(breeds: Iterator[Breed], outfile: Optional[str]) -> None:
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


def get_dog_listings(show_pbar: bool) -> Generator[Breed, None, None]:
    alphabet_pbar = tqdm(ALPHABET)

    for init in alphabet_pbar if show_pbar else ALPHABET:
        if args.destination is not None:
            alphabet_pbar.set_description(
                f"Getting listings for dogs beginning with {init}"
            )

        page = requests.get(f"{BASE_URL}/en/nomenclature/races.aspx?init={init}")

        breeds = _breeds_url_from_listing_page(page.content.decode("utf-8"))

        breeds_pbar = tqdm(breeds)

        for breed_name, breed_path in breeds_pbar if show_pbar else breeds:
            if args.destination is not None:
                breeds_pbar.set_description(f"Getting English name for {breed_name}")
            subpage = requests.get(f"{BASE_URL}{breed_path}")

            yield _breed_from_page(subpage.content.decode("utf-8"))
        return


if __name__ == "__main__":
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "destination",
        nargs="?",
        help="Output file to write contents to. stdout if not specified",
    )

    args = parser.parse_args()

    print_results(get_dog_listings(args.destination is not None), args.destination)
