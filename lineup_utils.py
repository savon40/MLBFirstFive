import re
import pandas as pd  # dataframe
from bs4 import BeautifulSoup, Comment  # web scraper
import requests  # to make an HTTP request
from fangraph_utils import *


def calculateWOBA(row):
    # 0.699×Unintentional BB + 0.728×HBP + 0.883×singles + 1.238×doubles + 1.558×triples + 1.979×HR) / (AB + BB – Intentional BB + SF + HBP
    # headers: Split	G	GS	PA	AB	R	H	2B	3B	HR	RBI	SB	CS	BB	SO	BA	OBP	SLG	OPS	TB	GDP	HBP	SH	SF	IBB	ROE	BAbip	tOPS+	sOPS
    # PA = AB + Walk + HBP + Sac Fly + Sac Hit?
    # I have: BB, HBP, doubles (2B), triples (3B), HR, AB, BB, IBB, SF, HBP
    # just need to calculate: Single

    if row['PA'] is not None and row['PA'] > 0:
        BB = 0 if row['BB'] is None else row['BB']
        HBP = 0 if row['HBP'] is None else row['HBP']
        Doubles = 0 if row['2B'] is None else row['2B']
        Triples = 0 if row['3B'] is None else row['3B']
        HR = 0 if row['HR'] is None else row['HR']
        PA = 0 if row['PA'] is None else row['PA']
        IBB = 0 if row['IBB'] is None else row['IBB']
        H = 0 if row['H'] is None else row['H']
        Singles = H - Doubles - Triples - HR

        WOBA = round((BB + (0.728*HBP) + (0.883*Singles) + (1.238 *
                    Doubles) + (1.558*Triples) + (1.979*HR)) / (PA - IBB), 3)
        return WOBA
    else: 
        return .310


def getSplits(player_code, year):
    split_20_url = "https://www.baseball-reference.com/players/split.fcgi?id={player_code}&year={year}&t=b"
    split_20_url = split_20_url.format(player_code=player_code, year=year)
    print(split_20_url)
    res = requests.get(split_20_url)
    data = res.text

    soup = BeautifulSoup(data, 'html5lib')
    plato_table = None
    total_table = None
    total_extra_table = None
    ha_table = None
    hagl_table = None

    for comment in soup.find_all(text=lambda text: isinstance(text, Comment)):
        if comment.find("<table ") > 0:
            comment_soup = BeautifulSoup(comment, 'html.parser')
            table = comment_soup.find("table")
            if table.get('id') == 'plato':
                plato_table = str(table)
            elif table.get('id') == 'total':
                total_table = str(table)
            elif table.get('id') == 'total_extra':
                total_extra_table = str(table)
            elif table.get('id') == 'hmvis':
                ha_table = str(table)
            elif table.get('id') == 'hmvis_extra':
                hagl_table = str(table)

    year_stats = {
        'Totals': {},
        'Last 14 Days': {},
        'vs Righty': {},
        'vs Lefty': {},
        'Home': {},
        'Away': {},
    }

    # totals table
    if total_table:
        df = pd.read_html(total_table)[0]
        for index, row in df.iterrows():
            # print(row)
            # print(row['Split'])
            if row['Split'].strip() == f"{year} Totals":
                year_stats['Totals']['Plate Appearances'] = row['PA']
                year_stats['Totals']['WOBA'] = calculateWOBA(row)
            elif row['Split'].strip() == "Last 14 days":
                year_stats['Last 14 Days']['Plate Appearances'] = row['PA']
                year_stats['Last 14 Days']['WOBA'] = calculateWOBA(row)

    # home away table
    if ha_table:
        df = pd.read_html(ha_table)[0]
        for index, row in df.iterrows():
            # print(row)
            # print(row['Split'])
            if row['Split'].strip() == 'Home':
                year_stats['Home']['Plate Appearances'] = row['PA']
                year_stats['Home']['WOBA'] = calculateWOBA(row)
            elif row['Split'].strip() == 'Away':
                year_stats['Away']['Plate Appearances'] = row['PA']
                year_stats['Away']['WOBA'] = calculateWOBA(row)

    # '#right left table'
    if plato_table:
        df = pd.read_html(plato_table)[0]
        for index, row in df.iterrows():
            # print(row)
            # print(row['Split'])
            if row['Split'].strip() == 'vs RHP':
                year_stats['vs Righty']['Plate Appearances'] = row['PA']
                year_stats['vs Righty']['WOBA'] = calculateWOBA(row)
            elif row['Split'].strip() == 'vs LHP':
                year_stats['vs Lefty']['Plate Appearances'] = row['PA']
                year_stats['vs Lefty']['WOBA'] = calculateWOBA(row)

    # print(year_stats)
    return year_stats


def getBaseballReferenceInfo(name):
    letter_url = "https://www.baseball-reference.com/players/{letter}/"

    names = name.split()
    last_name = names[1]
    letter_to_request = last_name[0].lower()
    letter_url = letter_url.format(letter=letter_to_request)
    res = requests.get(letter_url)  # make the http request
    # pass the http request content into the BeautifulSoup http parser
    soup = BeautifulSoup(res.content, 'html.parser')

    section = soup.find(id="div_players_")
    p_tags = section.find_all('p')  # find all p tags within the section
    a_tags = [p.find('a', href=True) for p in p_tags]

    splits = {}
    print(name)
    for a in a_tags:
        # within the a tags - a.contents is a list of everything within the a tags
        player_name = a.contents[0]
        player_code = a.get('href').split('/')[-1].split('.')[0]  # the url
        player_name = player_name.strip()

        if player_name == name:
            # splits['2020 Splits'] = getSplits(player_code, '2020')
            splits['2021 Splits'] = getSplits(player_code, '2021')

    return splits


def getLineups(matchup_div):

    away_lineup_ol = matchup_div.find(
        "ol", {"class": "starting-lineups__team--away"})
    away_lineup_lis = away_lineup_ol.find_all(
        "li", {"class": "starting-lineups__player"})
    away_lineup = []
    count = 1
    for li in away_lineup_lis:
        a_tag = li.find("a", {"class": "starting-lineups__player--link"})
        span = li.find("span", {"class": "starting-lineups__player--position"})

        name = a_tag.contents[0].strip()
        splits = getBaseballReferenceInfo(name)

        player = {
            '#': count,
            'name': a_tag.contents[0].strip(),
            'splits': splits
        }
        count = count + 1

        test_str = span.contents[0].strip()
        res = re.findall(r'\(.*?\)', test_str)[0]

        if len(res) == 3:
            player['bats'] = str(res)[1]

        away_lineup.append(player)

    home_lineup_ol = matchup_div.find(
        "ol", {"class": "starting-lineups__team--home"})
    home_lineup_lis = home_lineup_ol.find_all(
        "li", {"class": "starting-lineups__player"})
    home_lineup = []
    count = 1
    for li in home_lineup_lis:
        a_tag = li.find("a", {"class": "starting-lineups__player--link"})
        span = li.find("span", {"class": "starting-lineups__player--position"})

        name = a_tag.contents[0].strip()
        splits = getBaseballReferenceInfo(name)

        player = {
            '#': count,
            'name': name,
            'splits': splits
        }
        count = count + 1

        test_str = span.contents[0].strip()
        res = re.findall(r'\(.*?\)', test_str)[0]

        if len(res) == 3:
            player['bats'] = str(res)[1]

        home_lineup.append(player)

    lineups = {
        'away': away_lineup,
        'home': home_lineup
    }

    return lineups
