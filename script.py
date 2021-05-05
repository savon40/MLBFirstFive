import pandas as pd  # dataframe
from bs4 import BeautifulSoup as BS  # web scraper
import requests  # to make an HTTP request
from sys import argv
import datetime
from pitcher_utils import *
from lineup_utils import *
from matchup_utils import *
from csv_utils import *
from fangraph_utils import *
import json

import smtplib  # Import smtplib for the actual sending function
from email.message import EmailMessage  # Import the email modules we'll need
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText


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

    # i = 1
    for matchup_div in matchup_divs:

        # if i == 10 or i == 11:
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
        # i = i + 1
        # exit()

    return final_matchups


def main():
    print(datetime.date.today())
    today = datetime.date.today()
    # today = '2021-04-30'

    #CREATE CSV FROM FANGRAPH
    getFanGraphData()

    # GATHER DATA FROM MLB AND BASEBALL REFERENCE, AND LOAD INTO RAW JSON
    # matchups = getTodaysGames(today)
    # with open(f"data/{str(today)}-raw.json", 'w') as fp:
    #     json.dump(matchups, fp)

    # # READ FROM RAW JSON AND FIND WINNERS, LOAD INTO FINAL JSON
    # f = open(f"data/{str(today)}-raw.json",)  # Opening JSON file
    # # f = open(f"2021-04-19.json",)  # Opening JSON file
    # data = json.load(f)  # returns JSON object as a dictionary
    # final = findWinners(data)
    # # # with open(f"2021-04-19-final.json", 'w') as fp:
    # with open(f"data/{str(today)}-final.json", 'w') as fp:
    #     json.dump(final, fp)

    # # READ FROM FINAL JSON AND CREATE CSV
    # f = open(f"data/{str(today)}-final.json",)
    # data = json.load(f)
    # df = create_csv(data)
    # df.to_csv(f"data/{str(today)}.csv")

    # # EMAIL RESULTS FROM CSV
    # with open(f"data/{str(today)}.csv", 'rb') as content_file:

    #     sender_address = "seavon.sf@gmail.com"
    #     sender_password = "Duecourse_1"

    #     receiver_address = ["savon40@gmail.com", "jackcanaley@gmail.com"]

    #     msg = EmailMessage()

    #     content = content_file.read()
    #     msg.add_attachment(content, maintype='application',
    #                        subtype='json', filename='results.csv')

    #     msg['Subject'] = f"Baseball Bets Script Result"
    #     msg['From'] = sender_address
    #     msg['To'] = ', '.join(receiver_address)

    #     # Send the message via our own SMTP server.
    #     s = smtplib.SMTP('smtp.gmail.com', 587)
    #     s.starttls()
    #     s.login(sender_address, sender_password)
    #     s.send_message(msg)
    #     s.quit()

    print('email sent')


if __name__ == '__main__':
    main()
