#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Rouryi on 4/12.
import requests
from bs4 import BeautifulSoup
import re

# アクセスするURL
url = "https://store.playstation.com/ja-jp/grid/JP0507-PCSG00133_00-0000000000000000/1?relationship=add-ons"
res = requests.get(url)
soup = BeautifulSoup(res.text, 'lxml')

elems = soup.find_all(href=re.compile("/ja-jp/product/"))

DLC = []
for e in elems:
    temp = e.get('href')[15:]
    if temp not in DLC:
        print(temp)
        DLC.append(temp)
