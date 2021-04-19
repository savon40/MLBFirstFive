def calculatePitcherHaWOBA(pitcher, home_away):

    print(home_away)
    woba_2020 = pitcher['splits']['2020 Splits'][home_away]['WOBA Against']
    woba_2021 = pitcher['splits']['2021 Splits'][home_away]['WOBA Against']

    woba_total = (woba_2021 * 1.5) + woba_2020
    print(woba_total)
    return woba_total

def comparePitchers(matchup):
    print('comparePitchers method')
    home_pitcher = matchup['pitchers']['home']
    away_pitcher = matchup['pitchers']['away']
    
    home_14_woba = home_pitcher['splits']['2021 Splits']["Last 14 Days"]['WOBA Against']
    away_14_woba = away_pitcher['splits']['2021 Splits']["Last 14 Days"]['WOBA Against']

    print('home_14_woba ' + str(home_14_woba))
    print('away_14_woba ' + str(away_14_woba))

    home_woba = calculatePitcherHaWOBA(home_pitcher, 'Home')
    away_woba = calculatePitcherHaWOBA(away_pitcher, 'Away')

    home_pitcher_done = {
        "name": home_pitcher['name'],
        "throws": home_pitcher['throws'],
        "combined_woba": home_14_woba + home_woba
    }

    away_pitcher_done = {
        "name": away_pitcher['name'],
        "throws": away_pitcher['throws'],
        "combined_woba": away_14_woba + away_woba
    }

    pitcher_totals = {
        'home': home_pitcher_done,
        'away': away_pitcher_done,
    }

    print('home_pitcher_done ' + str(home_pitcher_done));
    print('away_pitcher_done ' + str(away_pitcher_done));
    return pitcher_totals;

def calculateBatterHaWOBA(batter, home_away)


def compareLineups(matchup, pitchers):
    print('compare lineups')

    #away lineup:
    for batter in matchup['lineups']['away']:
        ha_woba = calculateBatterHaWOBA(batter, 'Away')
        print(batter['name'])
    
def compareMatchup(matchup):
    print('compareMatchup method')
    pitchers = comparePitchers(matchup)
    lineups = compareLineups(matchup, pitchers)

    




