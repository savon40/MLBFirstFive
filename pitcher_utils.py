def getPitcher(pitcher_divs):
    pitchers = {}
    for pitcher_div in pitcher_divs:
        pitcher_summaries = pitcher_div.find_all(
            "div", {"class": "starting-lineups__pitcher-summary"})
        count = 1
        for pitcher_summary_div in pitcher_summaries:
            # print('SUMMARY HERE:::')
            # print(pitcher_summary_div)
            name_tags = pitcher_summary_div.find_all(
                "a", {"class": "starting-lineups__pitcher--link"})
            if name_tags:
                name = ''
                link = ''

                for tag in name_tags:
                    if tag.contents and tag.contents[0] and tag.contents[0].strip() != '':
                        #  print(f"pitcher here: {tag.contents[0]}")
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

                    # print(era)

                    pitcher = {
                        'name': name,
                        'link': link,
                        'throws': throws.contents[0].strip() if throws and throws.contents else '',
                        'wins': wins.contents[0].strip() if wins and wins.contents else '',
                        'losses': losses.contents[0].strip() if losses and losses.contents else '',
                        'era': era.contents[0].strip() if era and era.contents else '',
                        'so': so.contents[0].strip() if so and so.contents else '',
                    }
                    if count == 1:
                        pitchers['away'] = pitcher
                        count = count + 1
                    else:
                        pitchers['home'] = pitcher

    return pitchers
