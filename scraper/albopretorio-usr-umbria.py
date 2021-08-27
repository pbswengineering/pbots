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
from shared import date_ita_to_iso, download_soup  # noqa


SOURCE = "Albo Pretorio USR Umbria"
SUMMARY_URL = "https://usr.istruzione.umbria.gov.it/id.asp?CatID=Albo"
DETAIL_URL_TEMPLATE = "https://usr.istruzione.umbria.gov.it/{}"
PUBLISHER = "USR Umbria"


def parse_detail(url_detail: str) -> Dict[str, str]:
    """
    Parse the detail page of a publication.
    :param url_detail: URL of the publication's detail page
    :return: a dict with the publication details
    """
    soup = download_soup(url_detail)
    number = url_detail[
        url_detail.rfind("=") + 1 :
    ]  # Assume the DB ID as publication number
    pub: Dict[str, Any]
    pub = {
        "url": url_detail,
        "source": SOURCE,
        "number": number,
        "publisher": PUBLISHER,
        "attachments": [],
    }
    table = soup.find("table")
    if not table:
        return {}
    table_text = table.get_text()
    table_dates = re.findall(r"\d{2}/\d{2}/\d{4}", table_text)
    if table_dates:
        pub["date_start"] = date_ita_to_iso(table_dates[0])
    tds = table.find_all("td")
    if len(tds) > 1:
        a = tds[1].find("a")
        if a:
            pub["pub_type"] = a.get_text()
    pub["subject"] = table.find("td").get_text()
    return pub


def parse_row(row: Tag) -> Dict[str, str]:
    """
    Parse a row of the table of publications.
    :param row: a row of the table of publications
    :return: a dict with the publication details or None if the parsing failed
    """
    a_list = row.find_all("a")
    for a in a_list:
        if re.match(r"id.asp\?id=\d+", a["href"]):
            url_detail = DETAIL_URL_TEMPLATE.format(a["href"])
            return parse_detail(url_detail)
    return {}


def scrape() -> List[Dict[str, str]]:
    """
    Scrape the register.
    :return: a list of dictionaries of the current publications
    """
    soup = download_soup(SUMMARY_URL)
    rows = soup.find_all("li", {"class": "li_out"})
    pubs = []
    for row in rows:
        pub = parse_row(row)
        if pub:
            pubs.append(pub)
    return pubs


if __name__ == "__main__":
    print(json.dumps(scrape(), indent=2))
