# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

"""
albopretorio-usr-lazio
~~~~~~~~~~~~~~~~~~~~~~

Scraper for the register of the "USR Lazio".

:copyright: (c) 2021 Paolo Paolo Bernardi.
:license: GNU AGPL version 3, see LICENSE for more details.
"""

import json
import os
import sys
from typing import Dict, List, Optional

from bs4.element import Tag

sys.path.append(os.path.join(os.path.dirname(__file__)))
from shared import date_ita_to_iso, download_soup  # noqa


SOURCE = "Albo Pretorio USR Lazio"
SUMMARY_URL = "https://www.usrlazio.it/"
DETAIL_URL_TEMPLATE = "https://www.usrlazio.it{}"

PUBLISHER = "USR Lazio"


def parse_row(row: Tag) -> Optional[Dict[str, str]]:
    """
    Parse a row of the table of publications.
    :param row: a row of the table of publications
    :return: a dict with the publication details or None if the parsing failed
    """
    a_title = row.find("a", {"class": "wiki4_1_ag_titolo"})
    span_date = row.find("span", {"class": "wiki4_1_ag_data"})
    pub_date = date_ita_to_iso(span_date.get_text())
    span_subtitle = row.find("span", {"class": "wiki4_1_ag_occhiello"})
    pub_num = span_subtitle.get_text()
    publisher = PUBLISHER
    span_author = row.find("span", {"class": "wiki4_1_ag_autore"})
    author = span_author.get_text()
    if author:
        publisher = f"{publisher} - {author}"
    return {
        "url": DETAIL_URL_TEMPLATE.format(a_title["href"]),
        "subject": a_title.get_text(),
        "source": SOURCE,
        "publisher": publisher,
        "date_start": pub_date,  # type: ignore
        "number": pub_num,
        "attachments": [],  # type: ignore
    }


def scrape() -> List[Dict[str, str]]:
    """
    Scrape the register.
    :return: a list of dictionaries of the current publications
    """
    soup = download_soup(SUMMARY_URL)
    rows = soup.find_all("div", {"class": "wiki4_1_ag_contenitore"})
    pubs = []
    for row in rows:
        pub = parse_row(row)
        if pub:
            pubs.append(pub)
    return pubs


if __name__ == "__main__":
    print(json.dumps(scrape(), indent=2))
