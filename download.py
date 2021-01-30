#!/usr/bin/python3
# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, line-too-long

import json
import locale
import datetime
import xml.etree.ElementTree as ET
import os.path
import re
import argparse
import time

import requests
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
    'Content-Type': 'application/json;charset=utf-8',
    'Origin': 'https://www.smard.de',
    'Connection': 'keep-alive',
    'Referer': 'https://www.smard.de/home/downloadcenter/download-marktdaten',
    'DNT': '1',
    'Sec-GPC': '1',
}

data = {
    "request_form": [{
        "format": "XML",
        "moduleIds": [
            1001224,
            1004066,
            1004067,
            1004068,
            1001223,
            1004069,
            1004071,
            1004070,
            1001226,
            1001228,
            1001227,
            1001225,
            5000410,
            5004359
        ],
        "region":"DE",
        "timestamp_from": 1611010800000,
        "timestamp_to": 1611961199999,
        "type":"discrete",
        "language":"de"
    }]
}

'''
Module-Ids:

1001224: Realisierte Erzeugung > Kernenergie
1004066: Realisierte Erzeugung > Biomasse
1004067: Realisierte Erzeugung > Wind Onshore
1004068: Realisierte Erzeugung > Photovoltaik
1001223: Realisierte Erzeugung > Braunkohle
1004069: Realisierte Erzeugung > Steinkohle
1004071: Realisierte Erzeugung > Erdgas
1004070: Realisierte Erzeugung > Pumpspeicher
1001226: Realisierte Erzeugung > Wasserkraft
1001228: Realisierte Erzeugung > Sonstige Erneuerbare
1001227: Realisierte Erzeugung > Sonstige Konventionelle
1001225: Realisierte Erzeugung > Wind Offshore
5000410: Realisierter Stromverbrauch > Gesamt
5004359: Realisierter Stromverbrauch > Residuallast
'''


def round_time(dt=None, round_to=60):
    """Round a datetime object to any time lapse in seconds
    dt : datetime.datetime object, default now.
    round_to : Closest number of seconds to round to, default 1 minute.
    Author: Thierry Husson 2012 - Use it as you want but don't blame me.
    """
    if dt is None:
        dt = datetime.datetime.now()
    if isinstance(dt, int):
        dt = datetime.datetime.fromtimestamp(round(dt / 1000))
    seconds = (dt.replace(tzinfo=None) - dt.min).seconds
    rounding = (seconds+round_to/2) // round_to * round_to
    return dt + datetime.timedelta(0, rounding-seconds, -dt.microsecond)

locale.setlocale(locale.LC_NUMERIC, "de_DE.UTF-8")
for category in root.findall('kategorie'):
    cat_name = category.find('kategorie_name').text
    modules = category.find('bausteine')
    for module in modules.findall('baustein'):
        module_name = module.find('baustein_name').text
        unit_name = module.find('einheit').text
        values = module.find('werte')
        SUM_VALUES = 0
        for single_value in values.findall('wert_detail'):
            myval = single_value.find('wert')
            SUM_VALUES += locale.atof(myval.text)
        print(cat_name + ' > ' + module_name + ': ' + str(SUM_VALUES) + ' ' + unit_name)
CACHE_FILE = ''
