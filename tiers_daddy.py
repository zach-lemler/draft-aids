import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import math
import requests
import time
from itertools import combinations
import shutil
import os


import warnings
warnings.filterwarnings('ignore')

try:
    shutil.rmtree('tiers')
except:
    pass
try:
    shutil.rmtree('db')
except:
    pass

os.mkdir('tiers')
os.mkdir('db')

ranking_urls = {
                'rankings_adpdaddy' : 'https://dynasty-daddy.com/api/v1/player/all/market/6',
                'rankings_dynastyprocess' : 'https://dynasty-daddy.com/api/v1/player/all/market/2',
                'rankings_fantasynavigator' : 'https://dynasty-daddy.com/api/v1/player/all/market/3',
                'rankings_profootballnetwork' : 'https://dynasty-daddy.com/api/v1/player/all/market/9',
                'rankings_draftsharks' : 'https://dynasty-daddy.com/api/v1/player/all/market/12',
                'rankings_keeptradecut' : 'https://dynasty-daddy.com/api/v1/player/all/market/0'
                }

all_players_url = 'https://dynasty-daddy.com/api/v1/player/all/today'

sleeper_adp_url = "https://api.sleeper.com/projections/nfl/2025?season_type=regular&position[]=DEF&position[]=K&position[]=QB&position[]=RB&position[]=TE&position[]=WR&order_by=adp_std"
sleeper_adp = requests.get(sleeper_adp_url)
sleeper_adp = sleeper_adp.json()
sleeper_df = pd.DataFrame(sleeper_adp)
sleeper_adp_df = pd.DataFrame(sleeper_df['stats'].to_list())
sleeper_adp_df = pd.concat([sleeper_df[['player_id']], sleeper_adp_df[['adp_dynasty_2qb']]], axis=1)
sleeper_adp_df.columns = ['player_id', 'adp']

players = requests.get(all_players_url)
players_df = pd.DataFrame(players.json())

players_df = players_df[[
                        'name_id', 'sleeper_id', 'mfl_id', 'ff_id', 'espn_id', 'yahoo_id',
                        'ffpc_id', 'fantrax_id', 'full_name', 'first_name', 'last_name', 'team',
                        'position', 'age', 'experience', 'injury_status', 'depth_chart'
                        ]]

for ranking_url in ranking_urls.keys():
    time.sleep(5)
    rankings = requests.get(ranking_urls[ranking_url])

    rankings = rankings.json()
    rankings = pd.DataFrame(rankings)
    rankings = rankings[['name_id', 'sf_trade_value']]
    scaler = MinMaxScaler()
    rankings[ranking_url] = scaler.fit_transform(rankings['sf_trade_value'].values.reshape(-1,1))

    players_df = pd.merge(players_df, rankings[['name_id', ranking_url]], how='left', on='name_id')

players_df = players_df[players_df['position'] != 'PI']

players_df.to_csv('ranking_review.csv')

k_value=50
colors=['indianred', 'mediumseagreen', 'orchid', 'cornflowerblue', 'palevioletred', 'mediumpurple']
colors_unique = k_value
color_len = len(colors)
color_mult = int(math.ceil(colors_unique / color_len))
colors_tiered = colors * color_mult
colors_tiered = colors_tiered[:colors_unique]

tiers_columns = list(ranking_urls.keys()) 

all_combinations = []
for i in range(1,len(tiers_columns)+1):
    all_combinations += list(combinations(tiers_columns,i))

start = time.time()
for combination in all_combinations:
    
    
    combination = list(combination)
    combination_id = ''
    for i in tiers_columns:
        if i in combination:
            combination_id +='1' 
        else:
            combination_id +='0'
    
    tiers_df_concat = players_df[['sleeper_id'] + combination]
    
    if len(combination) > 1:
        tiers_df_concat['worst'] = tiers_df_concat.apply(lambda x : x[combination].min(), axis=1)
        tiers_df_concat['best'] = tiers_df_concat.apply(lambda x : x[combination].max(), axis=1)
        tiers_df_concat['avg'] = tiers_df_concat.apply(lambda x : x[combination].mean(), axis=1)    
    else:
        tiers_df_concat['worst'] = 0
        tiers_df_concat['best'] = tiers_df_concat[combination] + .005
        tiers_df_concat['avg'] = tiers_df_concat[combination]
        
    tiers_df_concat = tiers_df_concat.sort_values('avg', ascending = False)
    kmeans = KMeans(n_clusters=k_value, max_iter=600, algorithm = 'lloyd') 
    kmeans.fit(tiers_df_concat['avg'].values.reshape(-1, 1))    
    
    tiers_df_concat['tier'] = kmeans.labels_ 

    tiers_and_colors = pd.DataFrame(tiers_df_concat['tier'].drop_duplicates())
    tiers_and_colors = tiers_and_colors.reset_index(drop=True)
    tiers_and_colors = tiers_and_colors.reset_index()
    tiers_and_colors['colors'] = colors_tiered

    tiers_df_concat = pd.merge(tiers_df_concat, tiers_and_colors, how='left', on='tier')
    tiers_df_concat = tiers_df_concat.drop(columns=['tier'])
    tiers_df_concat =tiers_df_concat.rename(columns={'index':'tier'})
    tiers_df_concat = tiers_df_concat.sort_values(['avg'], ascending=False)
    
    if len(combination) > 1:
        tiers_df_concat['rank_diff'] = tiers_df_concat['worst'] - tiers_df_concat['best']
    else: 
        tiers_df_concat['rank_diff'] = - .01
        
    tiers_df_concat['avg_plot'] = tiers_df_concat['avg'] 
    tiers_df_concat = tiers_df_concat.reset_index(drop=True)
    tiers_df_concat = tiers_df_concat.reset_index()
    tiers_df_concat = tiers_df_concat.rename(columns={'index':'pick'})
    tiers_df_concat['player_id'] = tiers_df_concat['sleeper_id']
    tiers_df_concat = pd.merge(tiers_df_concat, sleeper_adp_df, how='left', on='player_id')
    tiers_df_concat['value'] = tiers_df_concat['pick'] - tiers_df_concat['adp'] + 1
    tiers_df_concat['value'] = tiers_df_concat['value'].round(2)
    
    tiers_df_concat = tiers_df_concat[['pick', 'sleeper_id', 'value', 'tier', 'colors', 'avg_plot', 'best', 'rank_diff', 'adp']]
    
    tiers_df_concat.to_csv(f'tiers/{combination_id}.csv', index=False)
    
    
stop = time.time()
print(stop-start)



players_df = players_df.rename(columns={'full_name':'player'})
players_df['my_guys'] = np.nan

players_df = players_df[['player', 'sleeper_id', 'my_guys', 'position']]

players_df.to_csv('db/players.csv', index=False)

with open('db/rankings.txt', 'w') as f:
    for line in tiers_columns:
        f.write(f"{line}\n")

with open('db/colors.txt', 'w') as f:
    for line in colors_tiered:
        f.write(f"{line}\n")



