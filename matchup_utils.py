from fangraph_utils import *

def calculatePitcherSplitWOBA(pitcher, split):
    # woba_2020 = .400
    woba_2021 = .400
    if pitcher['splits']:
        # if pitcher['splits']['2020 Splits'] and pitcher['splits']['2020 Splits'][split]:
        #     woba_2020 = pitcher['splits']['2020 Splits'][split]['WOBA Against']
        if pitcher['splits']['2021 Splits'] and pitcher['splits']['2021 Splits'][split]:
            woba_2021 = pitcher['splits']['2021 Splits'][split]['WOBA Against']

    woba_total = woba_2021 #(woba_2021 * 1.5) + woba_2020
    print(woba_total)
    return woba_total


def comparePitchersNoRL(matchup):
    # print('comparePitchers method')
    # print(matchup['pitchers'])
    home_pitcher = matchup['pitchers']['home']
    away_pitcher = matchup['pitchers']['away']

    home_14_woba = .400
    away_14_woba = .400

    if home_pitcher['splits'] and home_pitcher['splits']['2021 Splits'] and home_pitcher['splits']['2021 Splits']["Last 14 Days"]:
        home_14_woba = home_pitcher['splits']['2021 Splits']["Last 14 Days"]['WOBA Against']
    
    if away_pitcher['splits'] and away_pitcher['splits']['2021 Splits'] and away_pitcher['splits']['2021 Splits']["Last 14 Days"]:
        away_14_woba = away_pitcher['splits']['2021 Splits']["Last 14 Days"]['WOBA Against']

    # print('home_14_woba ' + str(home_14_woba))
    # print('away_14_woba ' + str(away_14_woba))

    home_woba = calculatePitcherSplitWOBA(home_pitcher, 'Home')
    home_righty_woba = calculatePitcherSplitWOBA(home_pitcher, 'vs Righty')
    home_lefty_woba = calculatePitcherSplitWOBA(home_pitcher, 'vs Lefty')

    away_woba = calculatePitcherSplitWOBA(away_pitcher, 'Away')
    away_righty_woba = calculatePitcherSplitWOBA(away_pitcher, 'vs Righty')
    away_lefty_woba = calculatePitcherSplitWOBA(away_pitcher, 'vs Lefty')

    home_pitcher_done = {
        "name": home_pitcher['name'],
        "throws": home_pitcher['throws'],
        "ha_14_woba": (home_14_woba * 2) + home_woba,
        "righty_woba": home_righty_woba,
        "lefty_woba": home_lefty_woba,
        "pitch_info": home_pitcher['pitch_info']
    }

    away_pitcher_done = {
        "name": away_pitcher['name'],
        "throws": away_pitcher['throws'],
        "ha_14_woba": (away_14_woba * 2) + away_woba,
        "righty_woba": away_righty_woba,
        "lefty_woba": away_lefty_woba,
        "pitch_info": away_pitcher['pitch_info']
    }

    pitcher_totals = {
        'home': home_pitcher_done,
        'away': away_pitcher_done,
    }

    return pitcher_totals

def comparePitchersRL(pitcher, lineup):
    print('lineup num_lefities ' + str(lineup['lefties']))
    print('lineup num_righties ' + str(lineup['righties']))

    rl_woba = ((lineup['lefties'] * pitcher['lefty_woba']) + (lineup['righties'] * pitcher['righty_woba'])) / 9
    print(rl_woba)

    rba = None

    if len(pitcher['pitch_info']) != 0:
        rba = pitcher['pitch_info']['RBA']
    else:
        rba = 0

    final_pitcher = {
        "name": pitcher["name"],
        "throws": pitcher["throws"],
        "combined_woba": rl_woba + pitcher["ha_14_woba"],
        "runs_saved": rba
    }

    return final_pitcher


def calculateBatterHaWOBA(batter, home_away):
    # print(home_away)
    # print(batter)

    # woba_2020 = .310
    woba_2021 = .310
    if batter['splits']:
        # if batter['splits']['2020 Splits'] and batter['splits']['2020 Splits'][home_away]:
        #     woba_2020 = batter['splits']['2020 Splits'][home_away]['WOBA']
        if batter['splits']['2021 Splits'] and batter['splits']['2021 Splits'][home_away]:
            woba_2021 = batter['splits']['2021 Splits'][home_away]['WOBA']

    woba_total = woba_2021 #(woba_2021 * 1.5) + woba_2020
    # print(woba_total)
    return woba_total


def calculateBatterRlWOBA(batter, pitcher_throws):
    # print('pitcher throws ' + pitcher_throws)

    throw = 'vs Righty' if pitcher_throws == 'RHP' else 'vs Lefty'

    # woba_2020 = .310
    woba_2021 = .310
    if batter['splits']:
        # if batter['splits']['2020 Splits'] and batter['splits']['2020 Splits'][throw]:
        #     woba_2020 = batter['splits']['2020 Splits'][throw]['WOBA']
        if batter['splits']['2021 Splits'] and batter['splits']['2021 Splits'][throw]:
            woba_2021 = batter['splits']['2021 Splits'][throw]['WOBA']

    woba_total = woba_2021 #(woba_2021 * 1.5) + woba_2020
    # print(woba_total)
    return woba_total


def getBatterTotalWoba(batter, pitcher_throws, home_away):
    # print('in batter woba')
    # print('pitcher_throws ' + pitcher_throws)
    # print('pitcher_throws ' + home_away)
    # wobas
    ha_woba = calculateBatterHaWOBA(batter, home_away)
    rl_woba = calculateBatterRlWOBA(batter, pitcher_throws)

    last_14_woba = .310
    if batter['splits'] and batter['splits']['2021 Splits'] and batter['splits']['2021 Splits']["Last 14 Days"]:
        last_14_woba = batter['splits']['2021 Splits']["Last 14 Days"]['WOBA']

    person_woba = {
        'name': batter['name'],
        'ha': ha_woba,
        'last_14_woba': last_14_woba * 2,
        'rl_woba': rl_woba
    }
    # print(person_woba)

    total_woba = ha_woba + rl_woba + last_14_woba
    return total_woba


def summarizeLineup(lineup, pitchers, pitcher_ha, batter_ha):
    num_lefties = 0
    num_righties = 0
    total_woba = 0
    total_raa = 0

    for batter in lineup:

        # get counts
        if batter['bats'] == 'L':
            num_lefties = num_lefties + 1
        elif batter['bats'] == 'R':
            num_righties = num_righties + 1
        else:
            if pitchers[pitcher_ha]['throws'] == 'RHP':
                num_lefties = num_lefties + 1
            else:
                num_righties = num_righties + 1

        batter_woba = getBatterTotalWoba(
            batter, pitchers[pitcher_ha]['throws'], batter_ha)

        print(batter['name'])
        print(pitchers[pitcher_ha]['name'])
        batter_raa = getBatterFangraphInfo(batter['name'], pitchers[pitcher_ha])
        print(f"batter raa: {batter_raa}")

        total_woba = total_woba + batter_woba
        total_raa = total_raa + batter_raa
        # break
        # total_rl_woba = total_rl_woba + rl_woba

    # print('lefties: ' + str(num_lefties))
    # print('num_righties: ' + str(num_righties))
    # print('total_woba: ' + str(total_woba))

    lineup_done = {
        'lefties': num_lefties,
        'righties': num_righties,
        'total_woba': total_woba,
        'total_raa': total_raa
    }
    return lineup_done


def compareLineups(matchup, pitchers):
    away_lineup_done = summarizeLineup(
        matchup['lineups']['away'], pitchers, 'home', 'Away')
    home_lineup_done = summarizeLineup(
        matchup['lineups']['home'], pitchers, 'away', 'Home')

    lineup_totals = {
        'home': home_lineup_done,
        'away': away_lineup_done
    }
    return lineup_totals


def compareMatchup(matchup):
    pitchers_almost = comparePitchersNoRL(matchup)
    lineups = compareLineups(matchup, pitchers_almost)

    home_pitcher_done = comparePitchersRL(pitchers_almost['home'], lineups['away'])
    away_pitcher_done = comparePitchersRL(pitchers_almost['away'], lineups['home'])


    pitchers = {
        "home": home_pitcher_done,
        "away": away_pitcher_done
    }

    # print(pitchers)
    # print(lineups)

    return_dict = {
        'home': matchup['home'],
        'away': matchup['away'],
        'pitchers': pitchers,
        'lineups': lineups
    }
    return return_dict
