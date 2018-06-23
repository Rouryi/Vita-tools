#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Rouryi on 6/23.

import requests
from bs4 import BeautifulSoup
import pickle
import pandas as pd
import sys
import os


def get_gameid_from_PSN(target_url):
    r = requests.get(target_url, allow_redirects=False)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "lxml")
    else:
        return None

    game_list = set()
    for i in soup.find_all("a", class_="internal-app-link ember-view"):
        game_list.add(i.get('href').strip("/ja-jp/product/"))
    return game_list


def get_gameid_from_NPS():
    original_data = pd.read_table("PSV_GAMES.tsv", error_bad_lines=False)
    all_data = original_data[["Title ID", "Region", "Content ID", "Original Name"]]
    data = all_data[all_data["Region"] == "JP"]
    return data


def main():
    args = sys.argv
    target_url = "https://store.playstation.com/ja-jp/grid/PN.CH.JP-PN.CH.MIXED.JP-PSVGAMEADD/1?direction=desc&gameContentType=games&sort=release_date"
    game_list = set()

    if len(args) is 1 and os.path.isfile("obj.pickle"):
        with open('obj.pickle', 'rb') as f:
            game_list = pickle.load(f)
    elif args[1] is "update":
        while True:
            res = get_gameid_from_PSN(target_url)
            if res is None:
                print(game_list)
                with open('obj.pickle', 'wb') as f:
                    pickle.dump(game_list, f)
                break
            game_list.update(res)
            if target_url[77] is "?":
                print(target_url[76] + "ページ目")
                target_url = target_url[:76] + str(int(target_url[76]) + 1) + target_url[77:]
            elif target_url[77] is "9":
                print(target_url[76:78] + "ページ目")
                target_url = target_url[:76] + str(int(target_url[76]) + 1) + "0" + target_url[78:]
            else:
                print(target_url[76:78] + "ページ目")
                target_url = target_url[:77] + str(int(target_url[77]) + 1) + target_url[78:]
            print("PS STORE の リスト   :   " + game_list)
            print("アクセス中URL" + target_url)
    else:
        exit()
    game_list_nps = get_gameid_from_NPS()
    # print("NPSのリスト   :   " + game_list_nps)

    result = game_list_nps[game_list_nps['Content ID'].apply(lambda x: x not in game_list)]
    print(result)
    result.to_csv('result.tsv')


if __name__ == '__main__':
    with open('obj.pickle', 'rb') as f:
        game_list = pickle.load(f)
    game_list_nps = get_gameid_from_NPS()
    result = [x for x in game_list if x not in game_list_nps["Content ID"]]
    print(result)
