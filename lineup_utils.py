import re
import pandas as pd  # dataframe
from bs4 import BeautifulSoup, Comment  # web scraper
import requests  # to make an HTTP request

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
        'home': {},
        'away': {},
    }

    #totals table
    if total_table:
        df = pd.read_html(total_table)[0]
        for index, row in df.iterrows():
            # print(row)
            # print(row['Split'])
            if row['Split'].strip() == f"{year} Totals":
                year_stats['Totals']['At Bats'] = row['AB']
                year_stats['Totals']['Hits'] = row['H']
                year_stats['Totals']['Games Pitched'] = row['G']
                year_stats['Totals']['BA'] = row['BA']
                year_stats['Totals']['SLG'] = row['SLG']
                year_stats['Totals']['Home Runs'] = row['HR']
            elif row['Split'].strip() == "Last 14 days":
                year_stats['Last 14 Days']['Games Pitched'] = row['G']
                year_stats['Last 14 Days']['At Bats'] = row['AB']
                year_stats['Last 14 Days']['Hits'] = row['H']
                year_stats['Last 14 Days']['Home Runs'] = row['HR']
                year_stats['Last 14 Days']['BA'] = row['BA']
                year_stats['Last 14 Days']['SLG'] = row['SLG']

    # home away table
    if ha_table:
        df = pd.read_html(ha_table)[0]
        for index, row in df.iterrows():
            # print(row)
            # print(row['Split'])
            if row['Split'].strip() == 'Home':
                year_stats['home']['At Bats'] = row['AB']
                year_stats['home']['Hits'] = row['H']
                year_stats['home']['SO'] = row['SO']
                year_stats['home']['BA'] = row['BA']
                year_stats['home']['SLG'] = row['SLG']
                year_stats['home']['Home Runs'] = row['HR']
            elif row['Split'].strip() == 'Away':
                year_stats['away']['At Bats'] = row['AB']
                year_stats['away']['Hits'] = row['H']
                year_stats['away']['SO'] = row['SO']
                year_stats['away']['BA'] = row['BA']
                year_stats['away']['SLG'] = row['SLG']
                year_stats['away']['Home Runs'] = row['HR']

    # '#right left table'
    if plato_table:
        df = pd.read_html(plato_table)[0]
        for index, row in df.iterrows():
            # print(row)
            # print(row['Split'])
            if row['Split'].strip() == 'vs RHP':
                year_stats['vs Righty']['At Bats'] = row['AB']
                year_stats['vs Righty']['Hits'] = row['H']
                year_stats['vs Righty']['SO'] = row['SO']
                year_stats['vs Righty']['BA'] = row['BA']
                year_stats['vs Righty']['SLG'] = row['SLG']
                year_stats['vs Righty']['HR'] = row['HR']
            elif row['Split'].strip() == 'vs LHP':
                year_stats['vs Lefty']['At Bats'] = row['AB']
                year_stats['vs Lefty']['Hits'] = row['H']
                year_stats['vs Lefty']['SO'] = row['SO']
                year_stats['vs Lefty']['BA'] = row['BA']
                year_stats['vs Lefty']['SLG'] = row['SLG']
                year_stats['vs Lefty']['HR'] = row['HR']

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
            splits['2020 Splits'] = getSplits(player_code, '2020')
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
