# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 17:40:19 2023

@author: thoma
"""


import matplotlib.pyplot as plt
import json
import pandas as pd
import pickle 
import base64
from PIL import Image
import tweepy

with open('saved_dictionary.pkl', 'rb') as f:
    dict_m_o = pickle.load(f)
rena={'Bosnia-Herzegovina':'Bosnia and Herz.','Cambodia (Kampuchea)':'Cambodia',
                                   'Central African Republic':'Central African Rep.','DR Congo (Zaire)':'Dem. Rep. Congo',
                                   'Ivory Coast':'Côte d\'Ivoire','Kingdom of eSwatini (Swaziland)':'eSwatini',
                                   'Macedonia, FYR':'Macedonia','Madagascar (Malagasy)':'Madagascar','Myanmar (Burma)':'Myanmar',
                                   'Russia (Soviet Union)':'Russia','Serbia (Yugoslavia)':'Serbia','South Sudan':'S. Sudan',
                                   'Yemen (North Yemen)':'Yemen','Zimbabwe (Rhodesia)':'Zimbabwe','Vietnam (North Vietnam)':'Vietnam'}
dict_m = {rena[key] if key in rena else key: item for key, item in dict_m_o.items()}

df_tot_m = pd.read_csv('Conf.csv',parse_dates=True,index_col=(0))
df_tot_m = df_tot_m.rename(columns={'Bosnia-Herzegovina':'Bosnia and Herz.','Cambodia (Kampuchea)':'Cambodia',
                                    'Central African Republic':'Central African Rep.','DR Congo (Zaire)':'Dem. Rep. Congo',
                                    'Ivory Coast':'Côte d\'Ivoire','Kingdom of eSwatini (Swaziland)':'eSwatini',
                                    'Macedonia, FYR':'Macedonia','Madagascar (Malagasy)':'Madagascar','Myanmar (Burma)':'Myanmar',
                                    'Russia (Soviet Union)':'Russia','Serbia (Yugoslavia)':'Serbia','South Sudan':'S. Sudan',
                                    'Yemen (North Yemen)':'Yemen','Zimbabwe (Rhodesia)':'Zimbabwe','Vietnam (North Vietnam)':'Vietnam'})

hist_df=pd.read_csv('Hist.csv',parse_dates=True,index_col=(0))
column_means = hist_df.mean()
threshold = 0.4
df_filtered = hist_df.loc[:, (hist_df > column_means).mean() > threshold]
min_d_list=[]
for i in df_filtered.columns:
    min_d_list.append(dict_m[i][0][1])    
min_d_list = pd.Series(min_d_list,index=df_filtered.columns)
min_d_list = min_d_list.sort_values()

for i in range(3):
    plt.figure(figsize=(10, 6))
    plt.plot(hist_df.loc[:,min_d_list.index[i]], marker='o', color='black', linestyle='-', linewidth=2, markersize=8)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xlabel('Date', fontsize=20)
    plt.xticks(fontsize=16)  # Set x-axis tick font size
    plt.yticks(fontsize=16)
    plt.box(False)
    plt.xticks(rotation=45, ha='right')
    plt.title(hist_df.loc[:,min_d_list.index[i]].name,fontsize=25)
    plt.savefig(f'Images\{i}_1.png', bbox_inches='tight')
    plt.show()
    
    plt.figure(figsize=(15, 6))
    plt.plot(df_tot_m.loc[dict_m[min_d_list.index[i]][0][0].index[-1]:,dict_m[min_d_list.index[i]][0][0].name].iloc[:7], marker='o', color='#df2226', linestyle='-', linewidth=2, markersize=8)
    plt.plot(dict_m[min_d_list.index[i]][0][0], marker='o', color='gray', linestyle='-', linewidth=2, markersize=8)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xlabel('Date', fontsize=20)
    plt.xticks(fontsize=16)  # Set x-axis tick font size
    plt.yticks(fontsize=16)
    plt.box(False)
    plt.xticks(rotation=45, ha='right')
    plt.title(dict_m[min_d_list.index[i]][0][0].name,fontsize=25)
    plt.text()
    plt.savefig(f'Images\{i}_2.png', bbox_inches='tight')
    plt.show()

    plot1 = Image.open(f'Images\{i}_1.png')
    plot2 = Image.open(f'Images\{i}_2.png')
    combined_width = max(plot1.width, plot2.width)
    combined_height = plot1.height + plot2.height
    combined_image = Image.new('RGB', (combined_width, combined_height), 'white')
    combined_image.paste(plot1, ((combined_width - plot1.width) // 2, 0))
    combined_image.paste(plot2, ((combined_width - plot2.width) // 2, plot1.height))
    combined_image.save(f'Images\{i}_c.png')
    
    

# API_key ='iKE87AGJhYpj2dlZpBba57Ohf'
# key_secret ='w3RYtCA3kQJc0wImvEYWTQu5iTY9MrA0riVBceehAVT5Zomvy6'
# access_token='1618319345720909838-axd6L7hd3q9f7ISYQ4kHrb7mH2Btw1'
# secret_token='JlaVU540DRUSPbarc70SFj1EzxTpjJ2QmmAwyFK3dhRzE'

# client_id = 'TU54MnlxRG9ySV9xajRvaDRDbWI6MTpjaQ'
# client_sec='f9BlnK1v6AHAl198Ap4DYzv8NQo38G-Vd5M8wSSvUQk6xfUNgp'
# bearer_tok='AAAAAAAAAAAAAAAAAAAAAHKJrQEAAAAA16QgTBO%2B1Fq10JsVkzWFvVgTNMw%3D6s601sGIPqThS2pQMwMhvJHDcBRNL2rlbAVNUKJvxntyAae7cv'


# auth = tweepy.OAuth1UserHandler(API_key, key_secret)
# auth.set_access_token(access_token, secret_token)

# message = "Hello world!"
# api = tweepy.API(auth)
# media = api.media_upload('github-mark.png')
# media_id = media.media_id

# client = tweepy.Client(bearer_token=bearer_tok,consumer_key=API_key,consumer_secret=key_secret,access_token=access_token,access_token_secret=secret_token)
# client.create_tweet(text="bisous", media_ids=[media_id])
