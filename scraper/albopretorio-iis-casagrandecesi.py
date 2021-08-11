# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

"""
albopretorio-iis-casagrandecesi
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Scraper for the register of the "IIS Casagrande-Cesi".

:copyright: (c) 2021 Paolo Paolo Bernardi.
:license: GNU AGPL version 3, see LICENSE for more details.
"""

import json
from typing import Dict, List, Optional

import requests

from bs4 import BeautifulSoup
from bs4.element import Tag


SOURCE = "Albo Pretorio IIS Casagrande-Cesi"
SUMMARY_URL = "https://www.casagrandecesi.edu.it/albo-online"
MEDIA_URL = "https://www.casagrandecesi.edu.it/sdg/app/default/view_documento.php?a={}&id_documento={}&sede_codice={}"

PUBLISHER = "IIS Casagrande-Cesi"


def date_ita_to_iso(ita: str) -> Optional[str]:
    """
    Convert an Italian date to the ISO format
    :param ita: date in Italian format (e.g. 31/12/2018 or 31-12-2018)
    :return: the date in ISO format (e.g. 2018-12-31)
    """
    if len(ita) != 10:
        return None
    year = int(ita[6:])
    month = int(ita[3:5])
    day = int(ita[:2])
    return "{:04d}-{:02d}-{:02d}".format(year, month, day)


def parse_row(row: Tag) -> Optional[Dict[str, str]]:
    """
    Parse a row of the table of publications.
    :param row: a row of the table of publications
    :return: a dict with the publication details or None if the parsing failed
    """
    title = row.find("h3").get_text()
    media_body = row.find("div", {"class": "media-body"})
    pub_num = media_body.get_text().strip().split("\n")[0]
    list_group_items = media_body.find_all("li", {"class": "list-group-item"})
    pub_date = date_ita_to_iso(list_group_items[0].find("strong").get_text())
    pub_type = list_group_items[1].find("strong").get_text()
    pub = {
        "url": SUMMARY_URL,
        "subject": title,
        "source": SOURCE,
        "publisher": SOURCE,
        "pub_type": pub_type,
        "date_start": pub_date,
        "number": pub_num,
        "attachments": []
    }
    media_right = row.find("div", {"class": "media-right"})
    if media_right:
        a = media_right.find("a")
        if a:
            pub["attachments"].append(
                {
                    "url": MEDIA_URL.format(a["data-dl"], a["data-doc"], a["data-cli"]),
                    "name": "Documento.pdf",
                }
            )
    medias = row.find_all("div", {"class": "media"})
    for i, media in enumerate(medias, 1):
        a = media.find("a")
        if a:
            text = media.find("span", {"class": "text"})
            name = text and text.get_text() or f"attachment-{i:02}"
            pub["attachments"].append(
                {
                    "url": MEDIA_URL.format(a["data-dl"], a["data-doc"], a["data-cli"]),
                    "name": name,
                }
            )
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
    rows = soup.find_all("div", {"class": "media at-item"})
    pubs = []
    for row in rows:
        pub = parse_row(row)
        if pub:
            pubs.append(pub)
    return pubs


if __name__ == "__main__":
    print(json.dumps(scrape(), indent=2))
