# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

"""
albopretorio-usr-umbria
~~~~~~~~~~~~~~~~~~~~~~~

Scraper for the register of the "USR Umbria".

:copyright: (c) 2021 Paolo Paolo Bernardi.
:license: GNU AGPL version 3, see LICENSE for more details.
"""

import json
import os
import re
import sys
from typing import Any, Dict, List

from bs4.element import Tag

sys.path.append(os.path.join(os.path.dirname(__file__)))
from shared import date_ita_text_to_iso, download_soup  # noqa


SOURCE = "Albo Pretorio USR Umbria"
SUMMARY_URL = "https://istruzione.umbria.it/page/{}/"
DETAIL_URL_TEMPLATE = "https://usr.istruzione.umbria.gov.it/{}"
PUBLISHER = "USR Umbria"


def parse_detail(url_detail: str) -> Dict[str, str]:
    """
    Parse the detail page of a publication.
    :param url_detail: URL of the publication's detail page
    :return: a dict with the publication details
    """
    soup = download_soup(url_detail)
    pub: Dict[str, Any]
    pub = {
        "url": url_detail,
        "source": SOURCE,
        "publisher": PUBLISHER,
        "attachments": [],
    }
    titolo = soup.find("h1", {"class": "otw_post_content-blog-title"})
    pub["subject"] = titolo.get_text()
    date_str = None
    for a in soup.find_all("a"):
        try:
            date_str = a["data-date"]
            break
        except:
            pass
    pub["date_start"] = date_str
    return pub


def parse_row(row: Tag) -> Dict[str, str]:
    """
    Parse a row of the table of publications.
    :param row: a row of the table of publications
    :return: a dict with the publication details or None if the parsing failed
    """
    a_list = row.find_all("a")
    url_detail = a_list[0]["href"]
    if "bit.ly" in url_detail:
        return None
    return parse_detail(url_detail)


def scrape() -> List[Dict[str, str]]:
    """
    Scrape the register.
    :return: a list of dictionaries of the current publications
    """
    pubs = []
    for i in range(1, 4):
        soup = download_soup(SUMMARY_URL.format(i))
        container_rows = soup.find_all("div", {"class": "rt-content-loader"})
        for container_row in container_rows:
            rows = container_row.find_all("div", {"class": "rt-grid-item"})
            for row in rows:
                pub = parse_row(row)
                if not pub:
                    continue
                pub["number"] = row["data-id"]
                if pub:
                    pubs.append(pub)
    return pubs


if __name__ == "__main__":
    print(json.dumps(scrape(), indent=2))
