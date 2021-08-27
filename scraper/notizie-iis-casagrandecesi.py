# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

"""
notizie-iis-casagrandecesi
~~~~~~~~~~~~~~~~~~~~~~~~~~

Scraper for the news of the "IIS Casagrande-Cesi".

:copyright: (c) 2021 Paolo Paolo Bernardi.
:license: GNU AGPL version 3, see LICENSE for more details.
"""

from hashlib import sha256
import json
from typing import Dict, List, Optional

import requests

from bs4 import BeautifulSoup
from bs4.element import Tag


SOURCE = "Notizie IIS Casagrande-Cesi"
SUMMARY_URL = "https://www.casagrandecesi.edu.it/"

PUBLISHER = "IIS Casagrande-Cesi"
PUB_TYPE = "News"

MONTHS_ITA = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"]

def date_ita_to_iso(ita: str) -> Optional[str]:
    """
    Convert an Italian date to the ISO format
    :param ita: date in Italian format (e.g. 31 dicembre 2018)
    :return: the date in ISO format (e.g. 2018-12-31)
    """
    v = ita.split(" ")
    if len(v) != 3:
        return None
    try:
        month = MONTHS_ITA.index(v[1]) + 1
    except ValueError:
        return None
    year = int(v[2])
    day = int(v[0])
    return "{:04d}-{:02d}-{:02d}".format(year, month, day)


def parse_row(row: Tag) -> Optional[Dict[str, str]]:
    """
    Parse a row of the table of publications.
    :param row: a row of the table of publications
    :return: a dict with the publication details or None if the parsing failed
    """
    h3_title = row.find("h3", {"class": "card-title"}) 
    try:
        a_title = h3_title.find("a")
        title = a_title.get_text().strip()
        url = (SUMMARY_URL + a_title.attrs["href"]).replace("//", "/")
    except:
        return None
    pub_num = sha256(url.encode("utf-8")).hexdigest()
    pub_date = date_ita_to_iso(row.find("div", {"class": "card-footer"}).get_text().strip())
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
    summary_page = requests.get(
        SUMMARY_URL,
        allow_redirects=True,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0"
        },
    )
    soup = BeautifulSoup(summary_page.content, "html.parser")
    all_news = soup.find_all("section", {"class": "sezione-notizie"})
    rows = []
    for news_row in all_news:
        rows.extend(news_row.find_all("div", {"class": "card"}))
    print(len(rows))
    pubs = []
    for row in rows:
        pub = parse_row(row)
        if pub:
            pubs.append(pub)
    return pubs


if __name__ == "__main__":
    print(json.dumps(scrape(), indent=2))
