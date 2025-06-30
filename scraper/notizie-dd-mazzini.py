# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

"""
notizie-dd-mazzini
~~~~~~~~~~~~~~~~~~

Scraper for the news of the "DD Mazzini".

:copyright: (c) 2021 Paolo Paolo Bernardi.
:license: GNU AGPL version 3, see LICENSE for more details.
"""

from hashlib import sha256
import os
import json
import sys
from typing import Dict, List, Optional

from bs4.element import Tag

sys.path.append(os.path.join(os.path.dirname(__file__)))
from shared import date_ita_text_to_iso, download_soup  # noqa


SOURCE = "Notizie DD Mazzini"
SUMMARY_URL = "https://ddmazziniterni.edu.it/tipologia-articolo/notizie/"

PUBLISHER = "DD Mazzini"
PUB_TYPE = "News"


def parse_row(row: Tag) -> Optional[Dict[str, str]]:
    """
    Parse a row of the table of publications.
    :param row: a row of the table of publications
    :return: a dict with the publication details or None if the parsing failed
    """
    title = row.find("h2").get_text().strip()
    url = row.attrs["href"]  # Here "row" is an "a"
    pub_num = sha256(url.encode("utf-8")).hexdigest()
    year = row.find("span", {"class": "year"}).get_text().strip()
    month_str = row.find("span", {"class": "month"}).get_text().strip()
    day = row.find("span", {"class": "day"}).get_text().strip()
    pub_date = date_ita_text_to_iso(f"{day} {month_str} {year}")
    pub = {
        "url": url,
        "subject": title,
        "source": SOURCE,
        "publisher": SOURCE,
        "pub_type": PUB_TYPE,
        "date_start": pub_date,
        "number": pub_num,
        "attachments": [],
    }
    return pub


def scrape() -> List[Dict[str, str]]:
    """
    Scrape the register.
    :return: a list of dictionaries of the current publications
    """
    soup = download_soup(SUMMARY_URL)
    rows = soup.find_all("a", {"class": "presentation-card-link"})
    pubs = []
    for row in rows:
        pub = parse_row(row)
        if pub:
            pubs.append(pub)
    return pubs


if __name__ == "__main__":
    print(json.dumps(scrape(), indent=2))
