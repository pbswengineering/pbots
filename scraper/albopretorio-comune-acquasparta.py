# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

"""
albopretorio-comune-acquasparta
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Scraper for the public board of the "Comune of Acquasparta".

:copyright: (c) 2025 Paolo Paolo Bernardi.
:license: GNU AGPL version 3, see LICENSE for more details.
"""

from hashlib import sha256
import os
import json
import re
import sys
from typing import Dict, List, Optional

from bs4 import BeautifulSoup
from bs4.element import Tag
import requests

sys.path.append(os.path.join(os.path.dirname(__file__)))
from shared import date_ita_text_to_iso, download_soup  # noqa


SOURCE = "Albo Pretorio del Comune di Acquasparta"
BASE_URL = "https://asp.urbi.it/urbi/progs/urp/"
SUMMARY_URL = f"{BASE_URL}ur1ME002.sto?StwEvent=910001^&DB_NAME=n1201560^&w3cbt=S"

MULTIPART_DATA_SUMMARY = {
    "idTreeView1": (None, "TreeView_Id"),
    "OggettoType": (None, "%like%"),
    "UR1ME001BT_CHIAMANTE": (None, "UR1ME002"),
    "DB_NAME": (None, "n1201560"),
    "BootstrapItalia_Home": (None, "/urbi/bootstrap-italia/2.3.8"),
    "w3cbt": (None, "S"),
    "Stepper_Idx": (None, "1"),
    "Collapse_Idx": (None, "1"),
    "Contenitore_Idx": (None, "1"),
    "TreeView_Idx": (None, "1"),
    "Form_Idx": (None, "1"),
    "Stepper_StepAttivo": (None, "1"),
    "Stepper_NextStep": (None, "2"),
    # Include other fields with empty values if needed
    "Tipologia": (None, ""),
    "EnteMittente": (None, ""),
    "DaData": (None, ""),
    "AData": (None, ""),
    "Oggetto": (None, ""),
    "RifAttoAnno": (None, ""),
    "RifAttoNumero": (None, ""),
    "OpenTree": (None, ""),
    "OpenTreeText": (None, ""),
    "Archivio": (None, ""),
    "SOLCollegamentoAtti": (None, ""),
    "catnome": (None, ""),
    "caturl": (None, ""),
    "servnome": (None, ""),
    "Stepper_StepAttivoNome": (None, ""),
    "Stepper_NextStepNome": (None, "")
}

MULTIPART_DATA_DETAIL = {
    "idTreeView1": (None, "TreeView_Id"),
    "Tipologia": (None, ""),
    "EnteMittente": (None, ""),
    "DaData": (None, ""),
    "AData": (None, ""),
    "OggettoType": (None, "%like%"),
    "Oggetto": (None, ""),
    "RifAttoAnno": (None, ""),
    "RifAttoNumero": (None, ""),
    "OpenTree": (None, ""),
    "OpenTreeText": (None, ""),
    "Archivio": (None, "S"),
    "UR1ME001BT_CHIAMANTE": (None, "UR1ME002"),
    "SOLCollegamentoAtti": (None, ""),
    "catnome": (None, ""),
    "caturl": (None, ""),
    "servnome": (None, ""),
    "DB_NAME": (None, "n1201560"),
    "BootstrapItalia_Home": (None, "/urbi/bootstrap-italia/2.3.8"),
    "w3cbt": (None, "S"),
    "Stepper_Idx": (None, "1"),
    "Collapse_Idx": (None, "2"),
    "Contenitore_Idx": (None, "1"),
    "TreeView_Idx": (None, "1"),
    "Form_Idx": (None, "2"),
    "Modale_Idx": (None, "1"),
}

HEADERS = {
    "User-Agent": "Mozilla/5.0",
}


def parse_row(row: Tag) -> Optional[Dict[str, str]]:
    """
    Parse a row of the table of publications.
    :param row: a row of the table of publications
    :return: a dict with the publication details or None if the parsing failed
    """
    url_suffix = row.attrs["data-w3cbt-button-modale-url"]
    url = f"{BASE_URL}{url_suffix}"
    response = requests.post(url, files=MULTIPART_DATA_DETAIL, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    rows = soup.find_all("tr")
    pub = {
        "url": url,
        "pub_num": "",
        "date_start": "",
        "attachments": [],
    }
    for row in rows:
        ths = row.find_all("th")
        tds = row.find_all("td")
        if not ths or not tds:
            continue
        key = ths[0].get_text().strip().upper()
        val = tds[0].get_text().strip()
        if key == "OGGETTO":
            pub["subject"] = val
        elif key == "N.REG":
            pub["pub_num"] = val
        elif key == "IN PUBBLICAZIONE":
            dates = re.findall(r"\d{2}-\d{2}-\d{4}", val)
            pub["date_start"] = dates[0]
        elif key == "TIPOLOGIA":
            pub["pub_type"] = val
        elif key == "ENTE MITTENTE":
            pub["publisher"] = val
    id_tabella_2 = soup.find("div", {"id": "idTabella2"})
    trs = id_tabella_2.find_all("tr")
    for tr in trs:
        tds = tr.find_all("td")
        if len(tds) < 2:
            continue
        att_name = tds[0].get_text().strip()
        a = tds[1].find("a", string="FILE")
        if not a:
            a = tds[1].find("a")
        att_url = a.attrs["href"]
        pub["attachments"].append({
            "name": att_name,
            "url": f"{BASE_URL}{att_url}",
        })
    return pub


def scrape() -> List[Dict[str, str]]:
    """
    Scrape the register.
    :return: a list of dictionaries of the current publications
    """
    response = requests.post(SUMMARY_URL, files=MULTIPART_DATA_SUMMARY, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    rows = soup.find_all("button", {"class": "btn-primary"})
    pubs = []
    for row in rows:
        pub = parse_row(row)
        if pub:
            pubs.append(pub)
    return pubs


if __name__ == "__main__":
    print(json.dumps(scrape(), indent=2))
