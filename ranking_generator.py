#Make a ranking
import data_retrieve
import pandas as pd
import numpy as np

data_retrieve

year=2023

ratings = pd.read_csv(f'season_rating_list/{year}_teams.txt')

ranking = ratings.rename(columns={'Unnamed: 0':'rank'})
ranking['rank'] += 1
print(ranking.head(25))