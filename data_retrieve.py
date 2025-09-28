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

def get_teams(year):
    with cfbd.ApiClient(configuration) as api_client:
        api_instance = cfbd.TeamsApi(api_client)
        teams = api_instance.get_fbs_teams(year=year)
        return teams

def get_ratings(year):
    with cfbd.ApiClient(configuration) as api_client:
        api_instance = cfbd.RatingsApi(api_client)
        ratings = api_instance.get_sp(year=year)
        return ratings
    

# Gathers API data into a pandas dataframe and creates a csv .txt file for each season
def get_game_data(year, division):
    df = pd.DataFrame.from_records([dict(season=g.season, week=g.week, home_team=g.home_team, home_points=g.home_points, away_points=g.away_points, away_team=g.away_team) for g in get_games(year, division)])
    df.to_csv(f'season_game_data/{year}_{division}_game_data.txt')

def get_team_data(year):
    df = pd.DataFrame.from_records([dict(school=g.school, abbreviation=g.abbreviation, alternate_names=g.alternate_names, conference=g.conference)for g in get_teams(year)])
    df.to_csv(f'season_team_list/{year}_teams.txt')

def get_ratings_data(year):
    df = pd.DataFrame.from_records([dict(school=g.team, rating=g.rating) for g in get_ratings(year)])
    df.to_csv(f'season_rating_list/{year}_teams.txt')

# Checks if the right amount of data files exist. If some are missing, will pull the data and overwrite current file structure.
if len(os.listdir('season_game_data')) < (dt.datetime.now().year - 2005):
    for year in range(2005, 2026):
        get_game_data(year, 'fbs')
        print(f'Game data for the {year} season has been downloaded')

if len(os.listdir('season_team_list')) < (dt.datetime.now().year - 2005):
    for year in range(2005, 2026):
        get_team_data(year)
        print(f'Team data for the {year} season has been downloaded')

if len(os.listdir('season_rating_list')) < (dt.datetime.now().year - 2005):
    for year in range(2005, 2026):
        get_ratings_data(year)
        print(f'Rating data for the {year} season has been downloaded')
else:
    print("All files game data files currently exist")
