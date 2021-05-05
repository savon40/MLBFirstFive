import re
import pandas as pd  # dataframe
from bs4 import BeautifulSoup, Comment  # web scraper
import requests  # to make an HTTP request

#be sure to change the season next year
def getFanGraphData():
    pitcher_pitch_type_url = f"https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=y&type=4&season=2021&month=0&season1=2021&ind=0&team=0&rost=0&age=0&filter=&players=0&page=1_10000"
    pitcher_pitch_value_url = f"https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=y&type=7&season=2021&month=0&season1=2021&ind=0&team=0&rost=0&age=0&filter=&players=0&page=1_10000"
    batter_pitch_value_url = f"https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=y&type=7&season=2021&month=0&season1=2021&ind=0&team=0&rost=0&age=0&filter=&players=0&page=1_10000"

    urls = [pitcher_pitch_type_url, pitcher_pitch_value_url, batter_pitch_value_url]

    #create csv daily for all 3
    index = 0
    for url in urls:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find(id="LeaderBoard1_dg1_ctl00")
        df = pd.read_html(str(table))[0]
        df.columns = df.columns.droplevel() #--> remove the multiindex
        print(index)
        print(df.columns)
        # df
        file_name = None
        if index == 0:
            file_name = 'pitcher_pitch_type'
        elif index == 1:
            file_name = 'pitcher_pitch_value'
        else:
            file_name = 'batter_pitch_value'

        df.to_csv(f"data/fangraph/{file_name}.csv", index = False)
        index = index + 1
