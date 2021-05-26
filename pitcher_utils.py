import pandas as pd  # dataframe
from bs4 import BeautifulSoup, Comment  # web scraper
import requests  # to make an HTTP request
from fangraph_utils import *


def calculateWOBA(row):
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


def getSplits(player_code, year):
    split_20_url = "https://www.baseball-reference.com/players/split.fcgi?id={player_code}&year={year}&t=p"
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

                # print(row)
                year_stats['Totals']['Plate Appearances'] = row['PA']
                year_stats['Totals']['WOBA Against'] = calculateWOBA(row)
                year_stats['Totals']['Games Pitched'] = row['G']
            elif row['Split'].strip() == "Last 14 days":
                year_stats['Last 14 Days']['Plate Appearances'] = row['PA']
                year_stats['Last 14 Days']['WOBA Against'] = calculateWOBA(row)
                year_stats['Last 14 Days']['Games Pitched'] = row['G']
                year_stats['Last 14 Days']['H'] = row['H']
                year_stats['Last 14 Days']['R'] = row['R']

    # totals table
    if total_extra_table:
        df = pd.read_html(total_extra_table)[0]
        for index, row in df.iterrows():
            # print(row)
            # print(row['Split'])
            if row['Split'].strip() == f"{year} Totals":
                print('Total')
                year_stats['Totals']['W'] = row['W']
                year_stats['Totals']['L'] = row['L']
                year_stats['Totals']['ERA'] = row['ERA']
                year_stats['Totals']['IP'] = row['IP']
            elif row['Split'].strip() == "Last 14 days":
                year_stats['Last 14 Days']['W'] = row['W']
                year_stats['Last 14 Days']['L'] = row['L']
                year_stats['Last 14 Days']['ERA'] = row['ERA']
                year_stats['Last 14 Days']['IP'] = row['IP']

    # home away table
    if ha_table:
        df = pd.read_html(ha_table)[0]
        for index, row in df.iterrows():
            # print(row)
            # print(row['Split'])
            if row['Split'].strip() == 'Home':
                # print(row)
                year_stats['Home']['Plate Appearances'] = row['PA']
                year_stats['Home']['WOBA Against'] = calculateWOBA(row)
                year_stats['Home']['Games Pitched'] = row['G']
            elif row['Split'].strip() == 'Away':
                # print(row)
                year_stats['Away']['Plate Appearances'] = row['PA']
                year_stats['Away']['WOBA Against'] = calculateWOBA(row)
                year_stats['Away']['Games Pitched'] = row['G']

    # home away game level table
    if hagl_table:
        df = pd.read_html(hagl_table)[0]
        for index, row in df.iterrows():
            # print(row)
            # print(row['Split'])
            if row['Split'].strip() == 'Home':
                # print(row)
                year_stats['Home']['W'] = row['W']
                year_stats['Home']['L'] = row['L']
                year_stats['Home']['ERA'] = row['ERA']
            elif row['Split'].strip() == 'Away':
                # print(row)
                year_stats['Away']['W'] = row['W']
                year_stats['Away']['L'] = row['L']
                year_stats['Away']['ERA'] = row['ERA']

    # '#right left table'
    if plato_table:
        df = pd.read_html(plato_table)[0]
        for index, row in df.iterrows():
            # print(row)
            # print(row['Split'])
            if row['Split'].strip() == 'vs RHB':
                year_stats['vs Righty']['Plate Appearances'] = row['PA']
                year_stats['vs Righty']['WOBA Against'] = calculateWOBA(row)
                year_stats['vs Righty']['Games Pitched'] = row['G']
            elif row['Split'].strip() == 'vs LHB':
                year_stats['vs Lefty']['Plate Appearances'] = row['PA']
                year_stats['vs Lefty']['WOBA Against'] = calculateWOBA(row)
                year_stats['vs Lefty']['Games Pitched'] = row['G']

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
        # print(a.contents)
        # within the a tags - a.contents is a list of everything within the a tags
        player_name = a.contents[0]
        player_code = a.get('href').split('/')[-1].split('.')[0]  # the url
        player_name = player_name.strip()

        if player_name == name:
            # splits['2020 Splits'] = getSplits(player_code, '2020')
            splits['2021 Splits'] = getSplits(player_code, '2021')

    return splits


def getPitcher(pitcher_divs):
    pitchers = {}
    for pitcher_div in pitcher_divs:
        pitcher_summaries = pitcher_div.find_all(
            "div", {"class": "starting-lineups__pitcher-summary"})
        count = 1
        for pitcher_summary_div in pitcher_summaries:
            name_tags = pitcher_summary_div.find_all(
                "a", {"class": "starting-lineups__pitcher--link"})
            if name_tags:
                name = ''
                link = ''

                for tag in name_tags:
                    if tag.contents and tag.contents[0] and tag.contents[0].strip() != '':
                        name = tag.contents[0]
                        link = tag.get('href')

                if name and name != '':

                    throws = pitcher_summary_div.find(
                        "span", {"class": "starting-lineups__pitcher-pitch-hand"})
                    wins = pitcher_summary_div.find(
                        "span", {"class": "starting-lineups__pitcher-wins"})
                    losses = pitcher_summary_div.find(
                        "span", {"class": "starting-lineups__pitcher-losses"})
                    era = pitcher_summary_div.find(
                        "span", {"class": "starting-lineups__pitcher-era"})
                    so = pitcher_summary_div.find(
                        "span", {"class": "starting-lineups__pitcher-strikeouts"})

                    splits = getBaseballReferenceInfo(name)
                    pitch_info = getPitcherFangraphInfo(name)

                    pitcher = {
                        'name': name,
                        'link': link,
                        'throws': throws.contents[0].strip() if throws and throws.contents else '',
                        'wins': wins.contents[0].strip() if wins and wins.contents else '',
                        'losses': losses.contents[0].strip() if losses and losses.contents else '',
                        'era': era.contents[0].strip() if era and era.contents else '',
                        'so': so.contents[0].strip() if so and so.contents else '',
                        'splits': splits,
                        'pitch_info': pitch_info
                    }
                    print(pitcher)
                    # exit()

                    if count == 1:
                        pitchers['away'] = pitcher
                        count = count + 1
                    else:
                        pitchers['home'] = pitcher

    return pitchers