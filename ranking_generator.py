import cfbd
import pandas as pd
import numpy as np
import os
import datetime as dt

# Gets API Key from text file
with open('collegefootballdata api key.txt', 'r') as file:
    for line in file:
        key=line

configuration = cfbd.Configuration(
    access_token = key
)

# Requests game data from the API and returns the result
def get_games(year, division):
    with cfbd.ApiClient(configuration) as api_client:
        api_instance = cfbd.GamesApi(api_client)
        games = api_instance.get_games(year=year, classification=division)
        return games

# Gathers API data into a pandas dataframe and creates a csv .txt file for each season
def get_data(year, division):
    df = pd.DataFrame.from_records([dict(season=g.season, week=g.week, home_team=g.home_team, home_points=g.home_points, away_points=g.away_points, away_team=g.away_team) for g in get_games(year, division)])
    df.to_csv(f'season_game_data/{year}_{division}_game_data.txt')

# Checks if the right amount of data files exist. If some are missing, will pull the data and overwrite current file structure.
if len(os.listdir('season_game_data')) < (dt.datetime.now().year - 2005):
    for year in range(2005, 2026):
        get_data(year, 'fbs')
        print(f'Game data for the {year} season has been downloaded')
else:
    print("All files game data files currently exist")
