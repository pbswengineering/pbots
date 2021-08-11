# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

"""
albopretorio-usr-terni
~~~~~~~~~~~~~~~~~~~~~~

Scraper for the register of the "USR Terni".

:copyright: (c) 2020 Paolo Paolo Bernardi.
:license: GNU AGPL version 3, see LICENSE for more details.
"""

import json
import re
from typing import Any, Dict, List, Optional

import requests

from bs4 import BeautifulSoup
from bs4.element import Tag


SOURCE = "Albo Pretorio UST Terni"
SUMMARY_URL = "https://terni.istruzione.umbria.gov.it/id.asp?CatID=Albo"
DETAIL_URL_TEMPLATE = "https://terni.istruzione.umbria.gov.it/{}"
PUBLISHER = "UST Terni"


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


def parse_detail(url_detail: str) -> Dict[str, str]:
    """
    Parse the detail page of a publication.
    :param url_detail: URL of the publication's detail page
    :return: a dict with the publication details
    """
    detail_page = requests.get(url_detail, allow_redirects=True)
    soup = BeautifulSoup(detail_page.content, "html.parser")
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
    summary_page = requests.get(SUMMARY_URL, allow_redirects=True)
    soup = BeautifulSoup(summary_page.content, "html.parser")
    rows = soup.find_all("li", {"class": "li_out"})
    pubs = []
    for row in rows:
        pub = parse_row(row)
        if pub:
            pubs.append(pub)
    return pubs


if __name__ == "__main__":
    print(json.dumps(scrape(), indent=2))
