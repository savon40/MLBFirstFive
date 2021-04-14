import pandas as pd  # dataframe
from bs4 import BeautifulSoup as BS  # web scraper
import requests  # to make an HTTP request
from sys import argv
import datetime
from pitcher_utils import *
from lineup_utils import *


def getPlayerStats(matchup):
    print('matchup method')

def getTodaysGames():

    print(datetime.date.today())
    today = datetime.date.today()
    # letter_url = "https://www.pro-football-reference.com/players/{today}/"
    # need to change to todays date on actual script
    starting_lineups_url = "https://www.mlb.com/starting-lineups/{today}"
    res = requests.get(starting_lineups_url)
    soup = BS(res.content, 'html.parser')
    matchup_divs = soup.find_all("div", {"class": "starting-lineups__matchup"})
    final_matchups = []

    for matchup_div in matchup_divs:

        away_div = matchup_div.find(
            "span", {"class": "starting-lineups__team-name--away"})
        home_div = matchup_div.find(
            "span", {"class": "starting-lineups__team-name--home"})
        home_a_tag = home_div.find('a', href=True)
        away_a_tag = away_div.find('a', href=True)

        # time
        time_div = matchup_div.find(
            "div", {"class": "starting-lineups__game-date-time"})
        time = time_div.find("time")

        home = {
            "team": home_a_tag.contents[0].strip(),
        }
        away = {
            "team": away_a_tag.contents[0].strip(),
        }

        pitcher_divs = matchup_div.find_all( "div", {"class": "starting-lineups__pitchers"})
        pitchers = getPitcher(pitcher_divs)
        lineups = getLineups(matchup_div)

        matchup = {
            "datetime": time.get('datetime'),
            "home": home,
            "away": away,
            "pitchers": pitchers,
            "lineups": lineups
        }
        final_matchups.append(matchup)
        # exit()

    return final_matchups


def main():
    matchups = getTodaysGames()
    # for matchup in matchups:
    #     getPlayerStats(matchup)

    print(matchups)


if __name__ == '__main__':
    main()
