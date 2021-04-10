import re


def getLineups(matchup_div):

    # print('in lineup')

    away_lineup_ol = matchup_div.find(
        "ol", {"class": "starting-lineups__team--away"})
    away_lineup_lis = away_lineup_ol.find_all(
        "li", {"class": "starting-lineups__player"})
    away_lineup = []
    count = 1
    for li in away_lineup_lis:
        a_tag = li.find("a", {"class": "starting-lineups__player--link"})
        span = li.find("span", {"class": "starting-lineups__player--position"})

        player = {
            '#': count,
            'name': a_tag.contents[0].strip()
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

        player = {
            '#': count,
            'name': a_tag.contents[0].strip()
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
