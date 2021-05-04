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

        home_lineup_woba = round(matchup['lineups']['home']['total_woba'], 3)
        away_lineup_woba = round(matchup['lineups']['away']['total_woba'], 3)

        if home_lineup_woba > away_lineup_woba:
            lineup_difference = f"{str(round(home_lineup_woba - away_lineup_woba, 3))} Home"
        else:
            lineup_difference = f"{str(round(away_lineup_woba - home_lineup_woba, 3))} Away"

        row = {
            'Home Team': matchup['home']['team'],
            'Away Team': matchup['away']['team'],
            'HP': matchup['pitchers']['home']['name'],
            'HP Throws': matchup['pitchers']['home']['throws'],
            'HP WOBA Against': home_pitch_woba,
            'AP': matchup['pitchers']['away']['name'],
            'AP Throws': matchup['pitchers']['away']['throws'],
            'AP WOBA Against': away_pitch_woba,
            'HL WOBA': home_lineup_woba,
            'AL WOBA': away_lineup_woba,
            'WOBA Pitcher Difference': pitcher_difference,
            'WOBA Lineup Difference': lineup_difference,
        }
        # print(row)
        matchup_items.append(row)

    df = pd.DataFrame(matchup_items)
    return df
