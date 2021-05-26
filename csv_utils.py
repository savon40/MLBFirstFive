import pandas as pd  # dataframe


def create_csv(data):
    matchup_items = []

    for matchup in data:

        pitcher_difference = None
        lineup_difference = None

        home_pitch_woba = round(
            matchup['pitchers']['home']['combined_woba'], 3)
        away_pitch_woba = round(
            matchup['pitchers']['away']['combined_woba'], 3)
        if home_pitch_woba < away_pitch_woba:
            pitcher_difference = f"{str(round(away_pitch_woba - home_pitch_woba, 3))} Home"
        else:
            pitcher_difference = f"{str(round(home_pitch_woba - away_pitch_woba, 3))} Away"

        home_pitch_rs = matchup['pitchers']['home']['runs_saved']
        away_pitch_rs = matchup['pitchers']['away']['runs_saved']

        print('rs things')
        print(home_pitch_rs)
        print(away_pitch_rs)

        home_lineup_woba = round(matchup['lineups']['home']['total_woba'], 3)
        away_lineup_woba = round(matchup['lineups']['away']['total_woba'], 3)

        if home_lineup_woba > away_lineup_woba:
            lineup_difference = f"{str(round(home_lineup_woba - away_lineup_woba, 3))} Home"
        else:
            lineup_difference = f"{str(round(away_lineup_woba - home_lineup_woba, 3))} Away"

        home_lineup_raa = round(matchup['lineups']['home']['total_raa'] / 9, 3)
        away_lineup_raa = round(matchup['lineups']['away']['total_raa'] / 9, 3)

        row = {
            'Home Team': f"{matchup['home']['team']} - {matchup['pitchers']['home']['name']} - {matchup['pitchers']['home']['throws']} - {matchup['pitchers']['home']['stats']}",
            'Away Team': f"{matchup['away']['team']} - {matchup['pitchers']['away']['name']} - {matchup['pitchers']['away']['throws']} - {matchup['pitchers']['away']['stats']}",
            'Home Last 14': f"{matchup['pitchers']['home']['last 14 stats']}",
            'Away Last 14': f"{matchup['pitchers']['away']['last 14 stats']}",
            # 'Away Team': f"{matchup['away']['team']}",
            # 'HP': matchup['pitchers']['home']['name'],
            # 'HP Throws': matchup['pitchers']['home']['throws'],
            'HP WOBA Against': home_pitch_woba,
            'HP Runs Saved': round(home_pitch_rs, 3),
            # 'AP': matchup['pitchers']['away']['name'],
            # 'AP Throws': matchup['pitchers']['away']['throws'],
            'AP WOBA Against': away_pitch_woba,
            'AP Runs Saved': round(away_pitch_rs, 3),
            'HL WOBA': home_lineup_woba,
            'HL RAA': home_lineup_raa,
            'AL WOBA': away_lineup_woba,
            'AL RAA': away_lineup_raa,
            'WOBA Pitcher Diff': pitcher_difference,
            'WOBA Lineup Diff': lineup_difference,
            'Home RAA vs AP': home_lineup_raa - away_pitch_rs,
            'Away RAA vs HP': away_lineup_raa - home_pitch_rs 
        }
        # print(row)
        matchup_items.append(row)

    df = pd.DataFrame(matchup_items)
    return df
