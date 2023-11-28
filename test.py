# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 13:31:17 2023

@author: thoma
"""

import pandas as pd
from shape import Shape,finder
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
import seaborn as sns
import pickle
from datetime import datetime,date,timedelta
import os 

df = pd.read_csv("https://ucdp.uu.se/downloads/ged/ged231-csv.zip",
                  parse_dates=['date_start','date_end'],low_memory=False)
df= pd.concat([df,pd.read_csv('https://ucdp.uu.se/downloads/candidateged/GEDEvent_v23_01_23_09.csv',parse_dates=['date_start','date_end'],low_memory=False)],axis=0)
month = datetime.now().strftime("%m")
for i in range(10,int(month)):
    df= pd.concat([df,pd.read_csv(f'https://ucdp.uu.se/downloads/candidateged/GEDEvent_v23_0_{i}.csv',parse_dates=['date_start','date_end'],low_memory=False)],axis=0)

df_tot = pd.DataFrame(columns=df.country.unique(),index=pd.date_range(df.date_start.min(),
                                          df.date_end.max()))
df_tot=df_tot.fillna(0)
for i in df.country.unique():
    df_sub=df[df.country==i]
    for j in range(len(df_sub)):
        if df_sub.date_start.iloc[j] == df_sub.date_end.iloc[j]:
            df_tot.loc[df_sub.date_start.iloc[j],i]=df_tot.loc[df_sub.date_start.iloc[j],i]+df_sub.best.iloc[j]
        else:
            df_tot.loc[df_sub.date_start.iloc[j]:
            df_sub.date_end.iloc[j],i]=df_tot.loc[df_sub.date_start.iloc[j]: \
                                                  df_sub.date_end.iloc[j],i]+ \
                                                  df_sub.best.iloc[j]/ \
                                                  (df_sub.date_end.iloc[j]- \
                                                  df_sub.date_start.iloc[j]).days 
df_tot_m=df_tot.resample('M').sum()
last_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
df_tot_m= df_tot_m.loc[:last_month,:]
df_tot_m.to_csv('Conf.csv')
del df
del df_tot
#df_tot_m = pd.read_csv('Conf.csv',parse_dates=True,index_col=(0))

h_train=10
h=6
pred_tot=[]
pred_raw=[]
dict_m={i :[] for i in df_tot_m.columns}
for i in range(len(df_tot_m.columns)):
    if not (df_tot_m.iloc[-h_train:,i]==0).all():
        shape = Shape()
        shape.set_shape(df_tot_m.iloc[-h_train:,i]) 
        find = finder(df_tot_m.iloc[:-h,:],shape)
        find.find_patterns(min_d=0.1,select=True,metric='dtw',dtw_sel=2)
        min_d_d=0.1
        while len(find.sequences)<3:
            min_d_d += 0.05
            find.find_patterns(min_d=min_d_d,select=True,metric='dtw',dtw_sel=2)
        pred_ori = find.predict(horizon=h,plot=False,mode='mean')
        pred_raw.append(pred_ori)
        pred_ori = pred_ori*(df_tot_m.iloc[-h_train:,i].max()-df_tot_m.iloc[-h_train:,i].min())+df_tot_m.iloc[-h_train:,i].min()
        pred_tot.append(pred_ori)
        dict_m[df_tot_m.columns[i]]=find.sequences
    else :
        pred_tot.append(pd.DataFrame(np.zeros((h,3))))
        pred_raw.append(pd.DataFrame(np.zeros((h,3))))
        
with open('saved_dictionary.pkl', 'wb') as f:
    pickle.dump(dict_m, f)
    
pred_df = [df.iloc[:, 0] for df in pred_raw]
pred_df = pd.concat(pred_df, axis=1)
pred_df.columns = df_tot_m.columns
pred_df = pred_df.rename(columns={'Bosnia-Herzegovina':'Bosnia and Herz.','Cambodia (Kampuchea)':'Cambodia',
                                    'Central African Republic':'Central African Rep.','DR Congo (Zaire)':'Dem. Rep. Congo',
                                    'Ivory Coast':'Côte d\'Ivoire','Kingdom of eSwatini (Swaziland)':'eSwatini',
                                    'Macedonia, FYR':'Macedonia','Madagascar (Malagasy)':'Madagascar','Myanmar (Burma)':'Myanmar',
                                    'Russia (Soviet Union)':'Russia','Serbia (Yugoslavia)':'Serbia','South Sudan':'S. Sudan',
                                    'Yemen (North Yemen)':'Yemen','Zimbabwe (Rhodesia)':'Zimbabwe','Vietnam (North Vietnam)':'Vietnam'})

pred_df.to_csv('Pred_df.csv')
pred_df_m = [df.iloc[:, 1] for df in pred_raw]
pred_df_m = pd.concat(pred_df_m, axis=1)
pred_df_m.columns = df_tot_m.columns
pred_df_m = pred_df_m.rename(columns={'Bosnia-Herzegovina':'Bosnia and Herz.','Cambodia (Kampuchea)':'Cambodia',
                                    'Central African Republic':'Central African Rep.','DR Congo (Zaire)':'Dem. Rep. Congo',
                                    'Ivory Coast':'Côte d\'Ivoire','Kingdom of eSwatini (Swaziland)':'eSwatini',
                                    'Macedonia, FYR':'Macedonia','Madagascar (Malagasy)':'Madagascar','Myanmar (Burma)':'Myanmar',
                                    'Russia (Soviet Union)':'Russia','Serbia (Yugoslavia)':'Serbia','South Sudan':'S. Sudan',
                                    'Yemen (North Yemen)':'Yemen','Zimbabwe (Rhodesia)':'Zimbabwe','Vietnam (North Vietnam)':'Vietnam'})

pred_df_m.to_csv('Pred_df_min.csv')
pred_df_m = [df.iloc[:, 2] for df in pred_raw]
pred_df_m = pd.concat(pred_df_m, axis=1)
pred_df_m.columns = df_tot_m.columns
pred_df_m = pred_df_m.rename(columns={'Bosnia-Herzegovina':'Bosnia and Herz.','Cambodia (Kampuchea)':'Cambodia',
                                    'Central African Republic':'Central African Rep.','DR Congo (Zaire)':'Dem. Rep. Congo',
                                    'Ivory Coast':'Côte d\'Ivoire','Kingdom of eSwatini (Swaziland)':'eSwatini',
                                    'Macedonia, FYR':'Macedonia','Madagascar (Malagasy)':'Madagascar','Myanmar (Burma)':'Myanmar',
                                    'Russia (Soviet Union)':'Russia','Serbia (Yugoslavia)':'Serbia','South Sudan':'S. Sudan',
                                    'Yemen (North Yemen)':'Yemen','Zimbabwe (Rhodesia)':'Zimbabwe','Vietnam (North Vietnam)':'Vietnam'})

pred_df_m.to_csv('Pred_df_max.csv')


#pred_df=pd.read_csv('Pred_df.csv',parse_dates=True,index_col=(0))
pred_df = [df.iloc[:, 0] for df in pred_tot]
pred_df = pd.concat(pred_df, axis=1)
pred_df.columns = df_tot_m.columns
pred_df = pred_df.rename(columns={'Bosnia-Herzegovina':'Bosnia and Herz.','Cambodia (Kampuchea)':'Cambodia',
                                    'Central African Republic':'Central African Rep.','DR Congo (Zaire)':'Dem. Rep. Congo',
                                    'Ivory Coast':'Côte d\'Ivoire','Kingdom of eSwatini (Swaziland)':'eSwatini',
                                    'Macedonia, FYR':'Macedonia','Madagascar (Malagasy)':'Madagascar','Myanmar (Burma)':'Myanmar',
                                    'Russia (Soviet Union)':'Russia','Serbia (Yugoslavia)':'Serbia','South Sudan':'S. Sudan',
                                    'Yemen (North Yemen)':'Yemen','Zimbabwe (Rhodesia)':'Zimbabwe','Vietnam (North Vietnam)':'Vietnam'})

value_pred = pred_df.sum().reset_index()
value_pred.columns=['name','value']

histo = df_tot_m.iloc[-h:,:]
histo = histo.rename(columns={'Bosnia-Herzegovina':'Bosnia and Herz.','Cambodia (Kampuchea)':'Cambodia',
                                   'Central African Republic':'Central African Rep.','DR Congo (Zaire)':'Dem. Rep. Congo',
                                   'Ivory Coast':'Côte d\'Ivoire','Kingdom of eSwatini (Swaziland)':'eSwatini',
                                   'Macedonia, FYR':'Macedonia','Madagascar (Malagasy)':'Madagascar','Myanmar (Burma)':'Myanmar',
                                   'Russia (Soviet Union)':'Russia','Serbia (Yugoslavia)':'Serbia','South Sudan':'S. Sudan',
                                   'Yemen (North Yemen)':'Yemen','Zimbabwe (Rhodesia)':'Zimbabwe','Vietnam (North Vietnam)':'Vietnam'})
histo = histo.sum().reset_index()
histo.columns=['name','hist']


world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world = world.merge(value_pred, how='left',on='name')
world = world.merge(histo, how='left',on='name')
world = world[world.name != 'Antarctica']
world = world.fillna(0)
world['per_pred']=world['value']/world['pop_est']
world['log_per_pred']=np.log10(world['value']+1)
world.to_file('world_plot.shp') 
#world.to_file('world_plot.geojson', driver='GeoJSON') 
df_tot_m_plot=df_tot_m.iloc[-h_train:,:]
df_tot_m_plot = df_tot_m_plot.rename(columns={'Bosnia-Herzegovina':'Bosnia and Herz.','Cambodia (Kampuchea)':'Cambodia',
                                   'Central African Republic':'Central African Rep.','DR Congo (Zaire)':'Dem. Rep. Congo',
                                   'Ivory Coast':'Côte d\'Ivoire','Kingdom of eSwatini (Swaziland)':'eSwatini',
                                   'Macedonia, FYR':'Macedonia','Madagascar (Malagasy)':'Madagascar','Myanmar (Burma)':'Myanmar',
                                   'Russia (Soviet Union)':'Russia','Serbia (Yugoslavia)':'Serbia','South Sudan':'S. Sudan',
                                   'Yemen (North Yemen)':'Yemen','Zimbabwe (Rhodesia)':'Zimbabwe','Vietnam (North Vietnam)':'Vietnam'})
df_tot_m_plot.to_csv('Hist.csv')

# =============================================================================
# Global Map
# =============================================================================

fig, ax = plt.subplots(1, 1, figsize=(30, 15))
world.boundary.plot(ax=ax, color='black')
world.plot(column='log_per_pred', cmap='Reds', ax=ax)
plt.xlim(-180,180)
plt.box(False)
ax.spines['left'].set_visible(False)
ax.set_yticklabels([])
ax.set_yticks([])
ax.set_xticklabels([])
ax.set_xticks([])
plt.savefig('Images/map.png', bbox_inches='tight')
plt.show()

# =============================================================================
# Historical Plot
# =============================================================================
pred_df.index = pd.date_range(start=df_tot_m.index[-1],periods=h+1,freq='M')[1:]
historical_series = pd.concat([df_tot_m.sum(axis=1).iloc[-60:],pred_df.sum(axis=1)],axis=0)
date_rng = historical_series.index

plt.figure(figsize=(25, 6))
plt.plot(date_rng[:-h+1], historical_series[:-h+1], marker='o', color='grey', linestyle='-', linewidth=2, markersize=8)
plt.plot(date_rng[-h:], historical_series[-h:], marker='o', color='red', linestyle='-', linewidth=2, markersize=8)
plt.scatter(date_rng[-h:], historical_series[-h:], color='red', s=100, zorder=5)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xlabel('Date', fontsize=20)
plt.xticks(fontsize=16)  # Set x-axis tick font size
plt.yticks(fontsize=16)
plt.box(False)
plt.xticks(rotation=45, ha='right')
plt.savefig('Images/sub1_1.png', bbox_inches='tight')
plt.show()

# =============================================================================
# Per continent
# =============================================================================

pred_cont = world.groupby('continent').sum()['value']
hist_cont = world.groupby('continent').sum()['hist'] 

df_plot = pd.DataFrame({'pred_cont': pred_cont, 'hist_cont': hist_cont})
df_plot = df_plot[df_plot.index!='Seven seas (open ocean)']
df_plot = df_plot.sort_values('pred_cont')
df_plot['color'] = np.where(df_plot['pred_cont'] > df_plot['hist_cont'], 'red', 'black')
def calculate_alpha(row):
    diff_ratio = (row['pred_cont'] - row['hist_cont']) / row['hist_cont']
    return np.clip(diff_ratio / 2 +0.5 , 0, 1)
df_plot['alpha'] = df_plot.apply(calculate_alpha, axis=1)
plt.figure(figsize=(10, 6))
ax=sns.barplot(x=df_plot.index, y='pred_cont', data=df_plot, palette=df_plot['color'])
for i, bar in enumerate(ax.patches):
    bar.set_alpha(df_plot['alpha'].iloc[i])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.set_yticklabels([])
ax.set_yticks([])
ax.spines['bottom'].set_color('#DDDDDD')
ax.tick_params(bottom=False, left=False)
ax.set_axisbelow(True)
ax.yaxis.grid(True, color='#EEEEEE')
ax.xaxis.grid(False)
#plt.xlabel('Continent', fontsize=20)
plt.xlabel('')
#plt.ylabel('Sum of Values', fontsize=12)
#plt.title('Predicted values by Continent', fontsize=16)
plt.yscale('log')
plt.ylabel('')
plt.xticks(fontsize=16)  # Set x-axis tick font size
plt.yticks(fontsize=16)
# ax.spines['left'].set_visible(False)
# ax.set_yticklabels([])
# ax.set_yticks([])
plt.xticks(rotation=45, ha='right')
ax.spines['left'].set_visible(False)
ax.set_yticklabels([])
ax.set_yticks([])
plt.savefig('Images/sub3.png', bbox_inches='tight')
plt.show()

# =============================================================================
# Risk Countries
# =============================================================================

pred_risk = world.sort_values('value',ascending=False)[['name','value','hist']][:10]
df_plot =pred_risk.set_index('name').sort_values('value',ascending=True)
df_plot['color'] = np.where(df_plot['value'] > df_plot['hist'], 'red', 'black')
def calculate_alpha(row):
    diff_ratio = (row['value'] - row['hist']) / (row['hist']+1)
    return np.clip(diff_ratio / 2 +0.5 , 0, 1)
df_plot['alpha'] = df_plot.apply(calculate_alpha, axis=1)
plt.figure(figsize=(10, 6))
ax = sns.barplot(x=df_plot.index, y='value', data=df_plot, palette=df_plot['color'])
for i, bar in enumerate(ax.patches):
    bar.set_alpha(df_plot['alpha'].iloc[i])
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_color('#DDDDDD')
ax.tick_params(bottom=False, left=False)
ax.set_axisbelow(True)
ax.yaxis.grid(True, color='#EEEEEE')
ax.xaxis.grid(False)
#plt.xlabel('Country', fontsize=20)
plt.xlabel('')
plt.ylabel('')
#plt.title('Most risky countries (log scale)', fontsize=16)
plt.yscale('log')
plt.xticks(fontsize=16)  # Set x-axis tick font size
plt.yticks(fontsize=16)
ax.spines['left'].set_visible(False)
ax.set_yticklabels([])
ax.set_yticks([])
plt.savefig('Images/sub2.png', bbox_inches='tight')
plt.show()


# =============================================================================
# Specific
# =============================================================================

h_train=10
h=6
pred_tot=[]
i = df_tot_m.columns.tolist().index(df_plot.index[-1])
shape = Shape()
shape.set_shape(df_tot_m.iloc[-h_train:,i]) 
find = finder(df_tot_m.iloc[:-h,:],shape)
find.find_patterns(min_d=0.1,select=True,metric='dtw',dtw_sel=2)
min_d_d=0.1
while len(find.sequences)<3:
    min_d_d += 0.05
    find.find_patterns(min_d=min_d_d,select=True,metric='dtw',dtw_sel=2)

pred_ori = find.predict(horizon=h,plot=False,mode='mean')
#pred_ori = pred_ori*(df_tot_m.iloc[-h_train:,i].max()-df_tot_m.iloc[-h_train:,i].min())+df_tot_m.iloc[-h_train:,i].min()
seq_pred =find.predict(horizon=h,plot=False,mode='mean',seq_out=True)


plt.figure(figsize=(10, 6))
ax = plt.gca()
plt.plot(pred_ori.index, pred_ori.iloc[:, 0], marker='o', color='red', linestyle='-', linewidth=2, markersize=8)
upper_bound = pred_ori.iloc[:, 2]
lower_bound = pred_ori.iloc[:, 1]
plt.fill_between(pred_ori.index, lower_bound, upper_bound, color='red', alpha=0.2)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.yticks(fontsize=16)
plt.box(False)
plt.xticks([*range(6)],['t+1','t+2','t+3','t+4','t+5','t+6'])
plt.xticks(fontsize=16)
plt.savefig('Images/ex1_m4.png', bbox_inches='tight')
plt.show()


plt.figure(figsize=(10, 6))
plt.plot(df_tot_m.iloc[-h_train:,i], marker='o', color='black', linestyle='-', linewidth=2, markersize=8)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xlabel('Date', fontsize=20)
plt.xticks(fontsize=16)  # Set x-axis tick font size
plt.yticks(fontsize=16)
plt.box(False)
plt.xticks(rotation=45, ha='right')
plt.savefig('Images/ex1.png', bbox_inches='tight')
plt.show()

# for k in range(3):
#     pred_ori= seq_pred.iloc[k,:]*(find.sequences[k][0].max()-find.sequences[k][0].min())+find.sequences[k][0].min()
#     pred_ori =pred_ori.T
#     pred_ori.index = pd.date_range(start=find.sequences[k][0].index[-1],periods=h+1,freq='M')[1:]
#     historical_series = pd.concat([find.sequences[k][0],pred_ori],axis=0)
#     date_rng = historical_series.index
#     plt.figure(figsize=(10, 6))
#     plt.plot(date_rng[:-h+1], historical_series[:-h+1], marker='o', color='grey', linestyle='-', linewidth=2, markersize=8)
#     plt.plot(date_rng[-h:], historical_series[-h:], marker='o', color='red', linestyle='-', linewidth=2, markersize=8)
#     plt.scatter(date_rng[-h:], historical_series[-h:], color='red', s=100, zorder=5)
#     plt.grid(axis='y', linestyle='--', alpha=0.7)
#     plt.xlabel('Date', fontsize=20)
#     plt.xticks(fontsize=16)  # Set x-axis tick font size
#     plt.yticks(fontsize=16)
#     plt.box(False)
#     plt.xticks(rotation=45, ha='right')
#     plt.title(f"{find.sequences[k][0].name}\nd = {find.sequences[k][1]}", style='italic', color='grey',fontsize=20)
#     plt.show()

for k in range(3):
    pred_ori= seq_pred.iloc[k,:]*(find.sequences[k][0].max()-find.sequences[k][0].min())+find.sequences[k][0].min()
    pred_ori =pred_ori.T
    pred_ori.index = pd.date_range(start=find.sequences[k][0].index[-1],periods=h+1,freq='M')[1:]
    historical_series = pd.concat([find.sequences[k][0],pred_ori],axis=0)
    date_rng = historical_series.index
    plt.figure(figsize=(10, 6))
    plt.plot(date_rng[:-h], historical_series[:-h], marker='o', color='grey', linestyle='-', linewidth=2, markersize=8)
    #plt.plot(date_rng[-h:], historical_series[-h:], marker='o', color='red', linestyle='-', linewidth=2, markersize=8)
    #plt.scatter(date_rng[-h:], historical_series[-h:], color='red', s=100, zorder=5)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xlabel('Date', fontsize=20)
    plt.xticks(fontsize=16)  # Set x-axis tick font size
    plt.yticks(fontsize=16)
    plt.box(False)
    plt.xticks(rotation=45, ha='right')
    plt.title(f"{find.sequences[k][0].name}\nd = {find.sequences[k][1]}", style='italic', color='grey',fontsize=20)
    plt.savefig(f'Images/ex1_m{k}.png', bbox_inches='tight')
    plt.show()
    

series_names, values = zip(*find.sequences)
name_barh=[]
for i in find.sequences:
    name_barh.append(str(i[0].name)+': '+str(i[0].index[0].month)+'-'+str(i[0].index[0].year))
values=values[:10]
name_barh=name_barh[:10]
fig, ax = plt.subplots()
bars = ax.barh(name_barh, values, color='gray', edgecolor='none')
ax.set_frame_on(False)
ax.grid(False)
for bar, value in zip(bars, values):
    ax.text(value+0.1*value, bar.get_y() + bar.get_height() / 2, f'{value:.2f}',
            va='center', ha='center', color='gray', fontsize=15)
ax.set_xlabel('Distance',fontsize=16)
ax.xaxis.set_visible(False)
ax.tick_params(axis='y', which='major', labelsize=15)
plt.savefig('Images/ex1_barh.png', bbox_inches='tight')
plt.show()













h_train=10
h=6
pred_tot=[]
i = df_tot_m.columns.tolist().index(df_plot.index[-2])
shape = Shape()
shape.set_shape(df_tot_m.iloc[-h_train:,i]) 
find = finder(df_tot_m.iloc[:-h,:],shape)
find.find_patterns(min_d=0.1,select=True,metric='dtw',dtw_sel=2)
min_d_d=0.1
while len(find.sequences)<3:
    min_d_d += 0.05
    find.find_patterns(min_d=min_d_d,select=True,metric='dtw',dtw_sel=2)
pred_ori = find.predict(horizon=h,plot=False,mode='mean')
#pred_ori = pred_ori*(df_tot_m.iloc[-h_train:,i].max()-df_tot_m.iloc[-h_train:,i].min())+df_tot_m.iloc[-h_train:,i].min()
seq_pred =find.predict(horizon=h,plot=False,mode='mean',seq_out=True)

plt.figure(figsize=(10, 6))
ax = plt.gca()
plt.plot(pred_ori.index, pred_ori.iloc[:, 0], marker='o', color='red', linestyle='-', linewidth=2, markersize=8)
upper_bound = pred_ori.iloc[:, 2]
lower_bound = pred_ori.iloc[:, 1]
plt.fill_between(pred_ori.index, lower_bound, upper_bound, color='red', alpha=0.2)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.yticks(fontsize=16)
plt.box(False)
plt.xticks([*range(6)],['t+1','t+2','t+3','t+4','t+5','t+6'])
plt.xticks(fontsize=16)
plt.savefig('Images/ex2_m4.png', bbox_inches='tight')
plt.show()


plt.figure(figsize=(10, 6))
plt.plot(df_tot_m.iloc[-h_train:,i], marker='o', color='black', linestyle='-', linewidth=2, markersize=8)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xlabel('Date', fontsize=20)
plt.xticks(fontsize=16)  # Set x-axis tick font size
plt.yticks(fontsize=16)
plt.box(False)
plt.xticks(rotation=45, ha='right')
plt.savefig('Images/ex2.png', bbox_inches='tight')
plt.show()
    
for k in range(3):
    pred_ori= seq_pred.iloc[k,:]*(find.sequences[k][0].max()-find.sequences[k][0].min())+find.sequences[k][0].min()
    pred_ori =pred_ori.T
    pred_ori.index = pd.date_range(start=find.sequences[k][0].index[-1],periods=h+1,freq='M')[1:]
    historical_series = pd.concat([find.sequences[k][0],pred_ori],axis=0)
    date_rng = historical_series.index
    plt.figure(figsize=(10, 6))
    plt.plot(date_rng[:-h], historical_series[:-h], marker='o', color='grey', linestyle='-', linewidth=2, markersize=8)
    #plt.plot(date_rng[-h:], historical_series[-h:], marker='o', color='red', linestyle='-', linewidth=2, markersize=8)
    #plt.scatter(date_rng[-h:], historical_series[-h:], color='red', s=100, zorder=5)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xlabel('Date', fontsize=20)
    plt.xticks(fontsize=16)  # Set x-axis tick font size
    plt.yticks(fontsize=16)
    plt.box(False)
    plt.xticks(rotation=45, ha='right')
    plt.title(f"{find.sequences[k][0].name}\nd = {find.sequences[k][1]}", style='italic', color='grey',fontsize=20)
    plt.savefig(f'Images/ex2_m{k}.png', bbox_inches='tight')
    plt.show()

series_names, values = zip(*find.sequences)
name_barh=[]
for i in find.sequences:
    name_barh.append(str(i[0].name)+': '+str(i[0].index[0].month)+'-'+str(i[0].index[0].year))

values=values[:10]
name_barh=name_barh[:10]

fig, ax = plt.subplots()
bars = ax.barh(name_barh, values, color='gray', edgecolor='none')
ax.set_frame_on(False)
ax.grid(False)
for bar, value in zip(bars, values):
    ax.text(value+0.1*value, bar.get_y() + bar.get_height() / 2, f'{value:.2f}',
            va='center', ha='center', color='gray', fontsize=15)
ax.set_xlabel('Distance',fontsize=16)
ax.xaxis.set_visible(False)
ax.tick_params(axis='y', which='major', labelsize=15)
plt.savefig('Images/ex2_barh.png', bbox_inches='tight')
plt.show()


df_best = pd.DataFrame(df_plot.index[-2:])
df_best.to_csv('best.csv')
