import pandas as pd  # dataframe
from bs4 import BeautifulSoup as BS  # web scraper
import requests  # to make an HTTP request
from sys import argv
import datetime
import json
import dateutil.parser
import os
import shutil

from pitcher_utils import *
from lineup_utils import *
from matchup_utils import *
from csv_utils import *
from fangraph_utils import *

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

    starting_lineups_url = "https://www.mlb.com/starting-lineups/{today}"
    res = requests.get(starting_lineups_url)
    soup = BS(res.content, 'html.parser')
    matchup_divs = soup.find_all("div", {"class": "starting-lineups__matchup"})
    final_matchups = []

    i = 1
    for matchup_div in matchup_divs:

        # if i == 1 or i == 2:
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
        if time.has_attr('datetime'):
            matchup_datetime = dateutil.parser.parse(time['datetime']).replace(tzinfo=None)
            if matchup_datetime >= datetime.datetime.now():

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

    # remove the data folder to start fresh - this way we dont store too much
    shutil.rmtree('data')

    #create the folder
    os.mkdir('data')
    os.mkdir('data/fangraph')

    print(datetime.date.today())
    today = datetime.date.today()
    # today = '2021-05-11'

    #CREATE CSV FROM FANGRAPH
    getFanGraphData()

    # # # GATHER DATA FROM MLB AND BASEBALL REFERENCE, AND LOAD INTO RAW JSON
    matchups = getTodaysGames(today)
    with open(f"data/{str(today)}-raw.json", 'w') as fp:
        json.dump(matchups, fp)

    # # READ FROM RAW JSON AND FIND WINNERS, LOAD INTO FINAL JSON
    f = open(f"data/{str(today)}-raw.json",)  # Opening JSON file
    # f = open(f"2021-04-19.json",)  # Opening JSON file
    data = json.load(f)  # returns JSON object as a dictionary
    final = findWinners(data)
    # with open(f"2021-05-05-final.json", 'w') as fp:
    with open(f"data/{str(today)}-final.json", 'w') as fp:
        json.dump(final, fp)

    # # READ FROM FINAL JSON AND CREATE CSV
    # f = open(f"data/2021-05-05-final.json",)
    f = open(f"data/{str(today)}-final.json",)
    data = json.load(f)
    df = create_csv(data)
    df.to_csv(f"data/{str(today)}.csv")

    if not df.empty:

        # EMAIL RESULTS FROM CSV
        with open(f"data/{str(today)}.csv", 'rb') as content_file:

            sender_address = "seavon.sf@gmail.com"
            sender_password = "Duecourse_1"

            # receiver_address = ["savon40@gmail.com"]
            receiver_address = ["savon40@gmail.com", "jackcanaley@gmail.com"]

            msg = EmailMessage()

            content = content_file.read()
            msg.add_attachment(content, maintype='application',
                            subtype='json', filename='results.csv')

            msg['Subject'] = f"Baseball Bets Script Result"
            msg['From'] = sender_address
            msg['To'] = ', '.join(receiver_address)

            # Send the message via our own SMTP server.
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(sender_address, sender_password)
            s.send_message(msg)
            s.quit()

        print('email sent')
    else:
        print('dataframe empty')


if __name__ == '__main__':
    main()
