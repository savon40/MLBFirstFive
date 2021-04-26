import pandas as pd  # dataframe
from bs4 import BeautifulSoup as BS  # web scraper
import requests  # to make an HTTP request
from sys import argv
import datetime
from pitcher_utils import *
from lineup_utils import *
from matchup_utils import *
import json

import smtplib # Import smtplib for the actual sending function
from email.message import EmailMessage  # Import the email modules we'll need


def findWinners(data):
    print('matchup method')

    final_list = []
    for matchup in data:

        # print(matchup)
        if matchup['pitchers'] and len(matchup['pitchers']) == 2 and matchup['pitchers']['away'] and matchup['lineups'] and matchup['lineups']['away'] and matchup['lineups']['home']:
            match = compareMatchup(matchup)
            final_list.append(match)
        # break

    return final_list


def getTodaysGames(today):

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

        pitcher_divs = matchup_div.find_all(
            "div", {"class": "starting-lineups__pitchers"})
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
        # break
        # exit()

    return final_matchups


def main():
    print(datetime.date.today())
    today = datetime.date.today()

    # gathering
    # matchups = getTodaysGames(today)
    # with open(f"{str(today)}-raw.json", 'w') as fp:
    #     json.dump(matchups, fp)

    # reading
    f = open(f"{str(today)}-raw.json",)  # Opening JSON file
    # f = open(f"2021-04-19.json",)  # Opening JSON file
    data = json.load(f)  # returns JSON object as a dictionary
    final = findWinners(data)

    print('results done')
    # print(final)

    # with open(f"2021-04-19-final.json", 'w') as fp:
    # with open(f"{str(today)}-final.json", 'w') as fp:
    #     json.dump(final, fp)


    #email results
    with open(f"{str(today)}-final.json", 'rb') as content_file:

        msg = EmailMessage()

        content = content_file.read()
        msg.add_attachment(content, maintype='application', subtype='json', filename='results.json')

        # msg.set_content(fp.read())

        msg['Subject'] = f"Baseball Bets Script Result"
        msg['From'] = "savon40@gmail.com"
        msg['To'] = "savon40@gmail.com"

        # Send the message via our own SMTP server.
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.send_message(msg)
        s.quit()

    print('email sent')


if __name__ == '__main__':
    main()
