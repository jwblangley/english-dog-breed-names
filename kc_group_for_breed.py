from collections import namedtuple
from typing import Any
import requests
from lxml import html

Breed = namedtuple("Breed", ["name", "group"])

KC_AZ_INFO_PAGE = "https://www.thekennelclub.org.uk/search/breeds-a-to-z"

INFO_CARD_XPATH = '//div[@class="m-breed-card__body"]'
GROUP_XPATH = './/div[@class="m-breed-card__category"]'
BREED_XPATH = './/strong[@class="m-breed-card__title"]'


def _breed_from_info_card(info_card: Any) -> Breed:
    assert len(group_elems := info_card.xpath(GROUP_XPATH)) == 1
    assert len(breed_elems := info_card.xpath(BREED_XPATH)) == 1
    [breed] = breed_elems
    [group] = group_elems
    return Breed(breed.text_content(), group.text_content())


def get_groups_for_breed() -> dict[str, str]:
    page = requests.get(f"{KC_AZ_INFO_PAGE}")
    content = page.text
    tree = html.fromstring(content)
    info_cards = tree.xpath(INFO_CARD_XPATH)
    return {breed: group for (breed, group) in map(_breed_from_info_card, info_cards)}


if __name__ == "__main__":
    groups_for_breed = get_groups_for_breed()
