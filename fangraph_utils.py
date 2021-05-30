import re
import pandas as pd  # dataframe
from bs4 import BeautifulSoup, Comment  # web scraper
import requests  # to make an HTTP request

# be sure to change the season next year


def getFanGraphData():
    pitcher_pitch_type_url = f"https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=4&season=2021&month=1000&season1=2021&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate=2021-01-01&enddate=2021-12-31&page=1_10000"
    pitcher_pitch_value_url = f"https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=7&season=2021&month=0&season1=2021&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate=&enddate=&page=1_10000"
    batter_pitch_value_url = f"https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=7&season=2021&month=0&season1=2021&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate=2021-01-01&enddate=2021-12-31&page=1_10000"

    urls = [pitcher_pitch_type_url,
            pitcher_pitch_value_url, batter_pitch_value_url]

    # create csv daily for all 3
    index = 0
    for url in urls:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find(id="LeaderBoard1_dg1_ctl00")
        df = pd.read_html(str(table))[0]
        df.columns = df.columns.droplevel()  # --> remove the multiindex
        df = df.fillna(0)  # make these all 0s so we can do math easier
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

        df.to_csv(f"data/fangraph/{file_name}.csv", index=False)
        index = index + 1


def getPitcherFangraphInfo(pitcher):
    print('fangraph pitcher')

    pitch_type_df = pd.read_csv("data/fangraph/pitcher_pitch_type.csv")
    pitch_value_df = pd.read_csv("data/fangraph/pitcher_pitch_value.csv")

    # pitch_type_row = pitch_type_row.iloc[:, 1:]

    # FB – fastball
    # SL – slider
    # CT – cutter
    # CB – curveball
    # CH – changeup
    # SF – split-fingered
    # KN – knuckleball
    # XX – unidentified
    # PO – pitch out

    if pitcher in pitch_type_df.values and pitcher in pitch_value_df.values:

        pitch_type_row = pitch_type_df.loc[pitch_type_df['Name'] == pitcher]
        pitch_value_row = pitch_value_df.loc[pitch_value_df['Name'] == pitcher]

        FB = pitch_type_row.loc[pitch_type_row['Name']
                                == pitcher, 'FB%'].item().strip('%')
        wFB = pitch_value_row.loc[pitch_value_row['Name']
                                  == pitcher, 'wFB/C'].item()

        SL = pitch_type_row.loc[pitch_type_row['Name']
                                == pitcher, 'SL%'].item().strip('%')
        wSL = pitch_value_row.loc[pitch_value_row['Name']
                                  == pitcher, 'wSL/C'].item().strip('%')

        CT = pitch_type_row.loc[pitch_type_row['Name']
                                == pitcher, 'CT%'].item().strip('%')
        wCT = pitch_value_row.loc[pitch_value_row['Name']
                                  == pitcher, 'wCT/C'].item()

        CB = pitch_type_row.loc[pitch_type_row['Name']
                                == pitcher, 'CB%'].item().strip('%')
        wCB = pitch_value_row.loc[pitch_value_row['Name']
                                  == pitcher, 'wCB/C'].item().strip('%')

        CH = pitch_type_row.loc[pitch_type_row['Name']
                                == pitcher, 'CH%'].item().strip('%')
        wCH = pitch_value_row.loc[pitch_value_row['Name']
                                  == pitcher, 'wCH/C'].item()

        SF = pitch_type_row.loc[pitch_type_row['Name']
                                == pitcher, 'SF%'].item().strip('%')
        wSF = pitch_value_row.loc[pitch_value_row['Name']
                                  == pitcher, 'wSF/C'].item()

        KN = pitch_type_row.loc[pitch_type_row['Name']
                                == pitcher, 'KN%'].item().strip('%')
        wKN = pitch_value_row.loc[pitch_value_row['Name']
                                  == pitcher, 'wKN/C'].item()

        rba = (float(FB) / 100 * float(wFB)) + (float(SL) / 100 * float(wSL)) + \
            (float(CT) / 100 * float(wCT)) + (float(CB) / 100 * float(wCB)) + (float(CH) /
                                                                               100 * float(wCH)) + (float(SF) / 100 * float(wSF)) + (float(KN) / 100 * float(wKN))

        # pitch types:: ,Name,Team,wFB,wSL,wCT,wCB,wCH,wSF,wKN,wFB/C,wSL/C,wCT/C,wCB/C,wCH/C,wSF/C,wKN/C
        # pitch values: #,Name,Team,wFB,wSL,wCT,wCB,wCH,wSF,wKN,wFB/C,wSL/C,wCT/C,wCB/C,wCH/C,wSF/C,wKN/C

        print('rba:: ')
        print(rba)

        pitcher_info = {
            'RBA': rba,
            'FB%': pitch_type_row.loc[pitch_type_row['Name']
                                      == pitcher, 'FB%'].item().strip('%'),
            'SL%': pitch_type_row.loc[pitch_type_row['Name']
                                      == pitcher, 'SL%'].item().strip('%'),
            'CT%': pitch_type_row.loc[pitch_type_row['Name']
                                      == pitcher, 'CT%'].item().strip('%'),
            'CB%': pitch_type_row.loc[pitch_type_row['Name']
                                      == pitcher, 'CB%'].item().strip('%'),
            'CH%': pitch_type_row.loc[pitch_type_row['Name']
                                      == pitcher, 'CH%'].item().strip('%'),
            'SF%': pitch_type_row.loc[pitch_type_row['Name']
                                      == pitcher, 'SF%'].item().strip('%'),
            'KN%': pitch_type_row.loc[pitch_type_row['Name']
                                      == pitcher, 'KN%'].item().strip('%')
        }
        # print('pitcher info here')
        # print(pitcher_info)
        # exit()
        return pitcher_info
    else:
        return {}


def getBatterFangraphInfo(batter, pitcher):
    # gets the pitch_info from the pitcher and the name from the batter - from there we do calculation per fangraphs.txt
    batter_value_df = pd.read_csv("data/fangraph/batter_pitch_value.csv")

    print(pitcher['pitch_info'])
    print(len(pitcher['pitch_info']))

    if batter in batter_value_df.values and len(pitcher['pitch_info']) != 0:
        batter_value_row = batter_value_df.loc[batter_value_df['Name'] == batter]
        if len(batter_value_row) == 1:
            # ,Name,Team,wFB,wSL,wCT,wCB,wCH,wSF,wKN,wFB/C,wSL/C,wCT/C,wCB/C,wCH/C,wSF/C,/C
            wFB = batter_value_row.loc[batter_value_row['Name']
                                    == batter, 'wFB/C'].item()
            wSL = batter_value_row.loc[batter_value_row['Name']
                                    == batter, 'wSL/C'].item()
            wCT = batter_value_row.loc[batter_value_row['Name']
                                    == batter, 'wCT/C'].item()
            wCB = batter_value_row.loc[batter_value_row['Name']
                                    == batter, 'wCB/C'].item()
            wCH = batter_value_row.loc[batter_value_row['Name']
                                    == batter, 'wCH/C'].item()
            wSF = batter_value_row.loc[batter_value_row['Name']
                                    == batter, 'wSF/C'].item()
            wKN = batter_value_row.loc[batter_value_row['Name']
                                    == batter, 'wKN/C'].item()

            # 'pitch_info': {'RAA': -0.45162, 'FB%': '32.5', 'SL%': '0', 'CT%': '33.7', 'CB%': '11.2', 'CH%': '22.6', 'SF%': '0', 'KN%': '0'}}
            # print(pitcher)
            # fb = 
            raa = (float(pitcher['pitch_info']['FB%']) / 100 * float(wFB)) + (float(pitcher['pitch_info']['SL%']) / 100 * float(wSL)) + (float(pitcher['pitch_info']['CT%']) / 100 * float(wCT)) + (float(pitcher['pitch_info']
                                                                                                                                                                                                ['CB%']) / 100 * float(wCB)) + (float(pitcher['pitch_info']['CH%']) / 100 * float(wCH)) + (float(pitcher['pitch_info']['SF%']) / 100 * float(wSF)) + (float(pitcher['pitch_info']['KN%']) / 100 * float(wKN))
            # raa = fb
            return raa
        else:
            return 0
    else:
        return 0
