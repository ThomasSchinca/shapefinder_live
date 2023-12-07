# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 15:27:12 2023

@author: thoma
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_leaflet as dl
from dash.dependencies import Input, Output
from matplotlib.colors import to_hex
import matplotlib.pyplot as plt
import geopandas as gpd
import plotly.express as px
import json
import pandas as pd
import pickle 
import base64

world = gpd.read_file('world_plot.geojson')
pred_df=pd.read_csv('Pred_df.csv',parse_dates=True,index_col=(0))
missing_columns = set(world['name']) - set(pred_df.columns)
pred_df = pred_df.assign(**{col: [0] * 6 for col in missing_columns})
pred_df.index = [f"t+{i}" for i in range(1,len(pred_df)+1)]
pred_df_min =pd.read_csv('Pred_df_min.csv',parse_dates=True,index_col=(0))
pred_df_min = pred_df_min.assign(**{col: [0] * 6 for col in missing_columns})
pred_df_max =pd.read_csv('Pred_df_max.csv',parse_dates=True,index_col=(0))
pred_df_max = pred_df_max.assign(**{col: [0] * 6 for col in missing_columns})
hist_df=pd.read_csv('Hist.csv',parse_dates=True,index_col=(0))
hist_df = hist_df.assign(**{col: [0] * 10 for col in missing_columns})
with open('saved_dictionary.pkl', 'rb') as f:
    dict_m_o = pickle.load(f)
rena={'Bosnia-Herzegovina':'Bosnia and Herz.','Cambodia (Kampuchea)':'Cambodia',
                                   'Central African Republic':'Central African Rep.','DR Congo (Zaire)':'Dem. Rep. Congo',
                                   'Ivory Coast':'Côte d\'Ivoire','Kingdom of eSwatini (Swaziland)':'eSwatini',
                                   'Macedonia, FYR':'Macedonia','Madagascar (Malagasy)':'Madagascar','Myanmar (Burma)':'Myanmar',
                                   'Russia (Soviet Union)':'Russia','Serbia (Yugoslavia)':'Serbia','South Sudan':'S. Sudan',
                                   'Yemen (North Yemen)':'Yemen','Zimbabwe (Rhodesia)':'Zimbabwe','Vietnam (North Vietnam)':'Vietnam'}
dict_m = {rena[key] if key in rena else key: item for key, item in dict_m_o.items()}
dict_m.update({col: [] for col in missing_columns})

new_dict = {}
for key, series_int_list in dict_m.items():
    series_list = [item[0] for item in series_int_list[:15]]
    new_dict[key] = series_list
    
dist_dict = {}
for key, series_int_list in dict_m.items():
    series_list = [item[1] for item in series_int_list[:5]]
    dist_dict[key] = series_list

def generate_subplot(series):
    fig = px.line(series, title=series.name)
    fig.update_layout(
                showlegend=False,plot_bgcolor="white",
                margin=dict(t=30,l=30,b=5,r=5),
                xaxis_title='',
                yaxis_title='')
    fig.update_traces(line=dict(color='grey'))
    return fig

def get_color(log_per_pr):
    cmap = plt.get_cmap('Reds')
    norm_log_per_pr = (log_per_pr - world['log_per_pred'].min()) / (world['log_per_pred'].max() - world['log_per_pred'].min())
    rgba_color = cmap(norm_log_per_pr)
    hex_color = to_hex(rgba_color)
    return hex_color

world['color'] = world['log_per_pred'].apply(get_color)
l_country = [dl.GeoJSON(data=json.loads(world.iloc[index:index+1].to_json()), style={'color': row['color'], 'opacity': 0, 'fillOpacity': '1'}) for index, row in world.iterrows()]
pace_png = base64.b64encode(open('PaCE_final_icon.png', 'rb').read()).decode('ascii')
git_png = base64.b64encode(open('github-mark.png', 'rb').read()).decode('ascii')
x_logo = base64.b64encode(open('x_logo.png', 'rb').read()).decode('ascii')

external_stylesheets=[dbc.themes.LUX]
webapp = dash.Dash(__name__,external_stylesheets=external_stylesheets)
webapp.title = 'Pace Risk Map'
webapp._favicon = ("icone_pace.ico")
server = webapp.server
config = {'displayModeBar': False}

# App layout
home_layout = html.Div([
    html.Div([
        html.Div([
           html.H2("Fatalities Risk Map",style={'textAlign': 'left', 'margin': '0', 'padding': '0'}),  # Title
           html.A([html.H4("Try The model", style={'textAlign': 'left', 'color': '#555', 'fontSize': '16px','marginTop':10,'marginLeft':50})],
                  href="https://shapefinder.azurewebsites.net/",
                   style={'color': '#555', 'fontSize': '14px','textDecoration': 'none'}),
           html.A([html.H4("Monthly report", style={'textAlign': 'left', 'color': '#555', 'fontSize': '16px','marginTop':10,'marginLeft':50})],
                  href="/report" ,#href="assets/Report.pdf",download="Pace_Monthly_Report.pdf",
                   style={'color': '#555', 'fontSize': '14px','textDecoration': 'none'}),
           html.A([html.H4("About", style={'textAlign': 'left', 'color': '#555', 'fontSize': '16px','marginTop':10,'marginLeft':50})],
                  href="/about" ,#assets/Web_docu.pdf",download="Documentation.pdf",
                   style={'color': '#555', 'fontSize': '14px','textDecoration': 'none'}),
           html.A([html.H4("The Team", style={'textAlign': 'left', 'color': '#555', 'fontSize': '16px','marginTop':10,'marginLeft':50})],
                  href="https://paceconflictlab.wixsite.com/conflict-research-la/team-4",
                   style={'color': '#555', 'fontSize': '14px','textDecoration': 'none'}),
           html.A([html.H4("Contact", style={'textAlign': 'left', 'color': '#555', 'fontSize': '16px','marginTop':10,'marginLeft':85})],
                  href="mailto:schincat@tcd.ie",
                   style={'color': '#555', 'fontSize': '14px','textDecoration': 'none'}),
           html.A([html.Img(src='data:image/png;base64,{}'.format(pace_png),style={
                   'position': 'absolute',
                   'right': '20px',
                   'top': '10px',
                   'display': 'block',
                   'height': '35px',
                   'width': '35px'
               })], href='https://paceconflictlab.wixsite.com/conflict-research-la'),
            html.A([html.Img(src='data:image/png;base64,{}'.format(git_png),style={
                    'position': 'absolute',
                    'right': '70px',
                    'top': '10px',
                    'display': 'block',
                    'height': '35px',
                    'width': '35px'
                })], href='https://github.com/ThomasSchinca/shapefinder_live'),
            html.A([html.Img(src='data:image/png;base64,{}'.format(x_logo),style={
                    'position': 'absolute',
                    'right': '120px',
                    'top': '10px',
                    'display': 'block',
                    'height': '35px',
                    'width': '35px'
                })], href='https://twitter.com/LabConflict')# Logo on the right# Logo on the right
        ], style={'backgroundColor': '#D3D3D3', 'padding': '8px','marginBottom':20, 'display': 'flex'}),
        html.Div([
            dl.Map(center=[38, 5], zoom=2,minZoom=2, children=l_country+[
                dl.GeoJSON(url='/assets/world_plot.geojson',id='total_c',style={'color': 'black', 'weight': 1, 'opacity': 1, 'fillOpacity': 0})
            ], style={'width': 1700,'height':'100%','backgroundColor': '#F5F5F5','marginLeft':150},zoomControl=False,attributionControl=False, id='map'),
            html.Div([dcc.Markdown('source data : [UCDP](https://ucdp.uu.se/downloads/)',style={
                    'position': 'absolute',
                    'left': '120px',
                    'top': '700px'
                })]),
            html.Div([html.Div(id='plot_test', style={'width': '100%', 'height': '100%', 'margin': '0'}),
                      html.Div(id='plot_test2', style={'width': '100%', 'height': '100%', 'margin': '0'}),
                      html.Div(id='plot_test3', style={'width': '100%', 'height': '100%', 'margin': '0'})
                      ], style={"display": "flex", 'flexDirection': 'column','width': '30%','height': '100%', 'margin': '0'}),
        ],style={"display": "flex",'width':'100%','height': '90vh','marginBottom':20})],style={'backgroundColor': '#F5F5F5'}),
    #html.Hr(style={'width': '70%','margin':'auto'}),
    html.Div(id='tite'),
    html.Div([
    html.Div(id='plot_test4')
    ],style={'marginLeft':100})
])

report_layout= html.Div([
    html.Div([
        html.Div([
           html.H2("Report",style={'textAlign': 'left', 'margin': '0', 'padding': '0'}),  # Title
           html.A([html.H4("Back to map", style={'textAlign': 'left', 'color': '#555', 'fontSize': '16px','marginTop':10,'marginLeft':50})],
                  href="/home",
                   style={'color': '#555', 'fontSize': '14px','textDecoration': 'none'}),
           html.A([html.H4("Contact", style={'textAlign': 'left', 'color': '#555', 'fontSize': '16px','marginTop':10,'marginLeft':845})],
                  href="mailto:schincat@tcd.ie",
                   style={'color': '#555', 'fontSize': '14px','textDecoration': 'none'}),
           html.A([html.Img(src='data:image/png;base64,{}'.format(pace_png),style={
                   'position': 'absolute',
                   'right': '20px',
                   'top': '10px',
                   'display': 'block',
                   'height': '35px',
                   'width': '35px'
               })], href='https://paceconflictlab.wixsite.com/conflict-research-la'),
            html.A([html.Img(src='data:image/png;base64,{}'.format(git_png),style={
                    'position': 'absolute',
                    'right': '70px',
                    'top': '10px',
                    'display': 'block',
                    'height': '35px',
                    'width': '35px'
                })], href='https://github.com/ThomasSchinca/shapefinder_live'),
            html.A([html.Img(src='data:image/png;base64,{}'.format(x_logo),style={
                    'position': 'absolute',
                    'right': '120px',
                    'top': '10px',
                    'display': 'block',
                    'height': '35px',
                    'width': '35px'
                })], href='https://twitter.com/LabConflict')# Logo on the right# Logo on the right
        ], style={'backgroundColor': '#D3D3D3', 'padding': '8px','marginBottom':20, 'display': 'flex'})]),
    html.Iframe(src='assets/Report.pdf', width='80%', height='800px',style={'marginLeft':160}),
])

about_layout=html.Div([
    html.Div([
        html.Div([
           html.H2("About",style={'textAlign': 'left', 'margin': '0', 'padding': '0'}),  # Title
           html.A([html.H4("Back to map", style={'textAlign': 'left', 'color': '#555', 'fontSize': '16px','marginTop':10,'marginLeft':50})],
                  href="/home",
                   style={'color': '#555', 'fontSize': '14px','textDecoration': 'none'}),
           html.A([html.H4("Contact", style={'textAlign': 'left', 'color': '#555', 'fontSize': '16px','marginTop':10,'marginLeft':855})],
                  href="mailto:schincat@tcd.ie",
                   style={'color': '#555', 'fontSize': '14px','textDecoration': 'none'}),
           html.A([html.Img(src='data:image/png;base64,{}'.format(pace_png),style={
                   'position': 'absolute',
                   'right': '20px',
                   'top': '10px',
                   'display': 'block',
                   'height': '35px',
                   'width': '35px'
               })], href='https://paceconflictlab.wixsite.com/conflict-research-la'),
            html.A([html.Img(src='data:image/png;base64,{}'.format(git_png),style={
                    'position': 'absolute',
                    'right': '70px',
                    'top': '10px',
                    'display': 'block',
                    'height': '35px',
                    'width': '35px'
                })], href='https://github.com/ThomasSchinca/shapefinder_live'),
            html.A([html.Img(src='data:image/png;base64,{}'.format(x_logo),style={
                    'position': 'absolute',
                    'right': '120px',
                    'top': '10px',
                    'display': 'block',
                    'height': '35px',
                    'width': '35px'
                })], href='https://twitter.com/LabConflict')# Logo on the right# Logo on the right
        ], style={'backgroundColor': '#D3D3D3', 'padding': '8px','marginBottom':20, 'display': 'flex'})]),
    
    html.Div([
        html.H1("Pace Risk Map Web Application"),
        
        dcc.Markdown("""
        **Overview**
        
        The Pace Risk Map web application is designed to visualize and analyze risk factors related to conflict and fatalities across different countries. It incorporates geographical data, matching models, and historical information to provide insights into potential conflict scenarios.
        
        **Purpose**
        
        - Provide a user-friendly interface for exploring conflict risk data.
        - Display historical information for individual countries.
        - Offer additional resources for further exploration.
        
        **Data Sources**
        
        - Conflict-Fatalities: UCDP Dataset ([UCDP Dataset](https://ucdp.uu.se/downloads/)), aggregated at the country-monthly level.
        - UCDP Georeferenced Event Dataset.
        - UCDP Candidate Events Dataset (to get the latest data).
        
        **The Model**
        
        The applied model operates by examining recent events within a country and aligning them with historical occurrences. It discerns patterns in the temporal evolution of incidents, enabling the identification of analogous scenarios from the past. This matching process contributes to a comprehensive understanding of when and where comparable situations have historically manifested. Consequently, the model plays a pivotal role in predicting the future trajectory of potential conflict-related scenarios based on these historical parallels, called ‘Past Future’.
        
        **Functionality**
        
        - **Map Visualization:**
          Color-coded map indicating risk levels. The risk level corresponds to the log value of the sum of the 6-month future values of matched historical cases. The more red the country, the higher risk value.
          
        - **Clicking on a country reveals Country-specific Data:**
          - **Country-specific Data:**
            - Historical data displayed in line charts, corresponding to the last 10-months aggregated fatalities.
            - Mean and Confidence interval of the following timestamp of the historical cases matched.
            - Bar chart showing the best-matched sequences. The bar values represent the distance from the selected country sequence.
            
          - **Matched Historical Cases:**
            All the plot of the matched historical cases with the name of the country as title and Date as index. The sequences are ordered by similarity (or lowest distance).
        """),
        
        html.H3("Data Sources"),
        
        dcc.Markdown("""
        - **Conflict-Fatalities:** UCDP Dataset ([UCDP Dataset](https://ucdp.uu.se/downloads/)), aggregated at the country-monthly level.
        - **UCDP Georeferenced Event Dataset.**
        - **UCDP Candidate Events Dataset (to get the latest data)."""
        ),
        
        html.H3("The Model"),
        
        dcc.Markdown("""
        The applied model operates by examining recent events within a country and aligning them with historical occurrences. It discerns patterns in the temporal evolution of incidents, enabling the identification of analogous scenarios from the past. This matching process contributes to a comprehensive understanding of when and where comparable situations have historically manifested. Consequently, the model plays a pivotal role in predicting the future trajectory of potential conflict-related scenarios based on these historical parallels, called ‘Past Future’."""
        ),
        
        html.H3("Functionality"),
        
        dcc.Markdown("""
        - **Map Visualization:**
          Color-coded map indicating risk levels. The risk level corresponds to the log value of the sum of the 6-month future values of matched historical cases. The more red the country, the higher risk value.
          
        - **Clicking on a country reveals Country-specific Data:**
          - **Country-specific Data:**
            - Historical data displayed in line charts, corresponding to the last 10-months aggregated fatalities.
            - Mean and Confidence interval of the following timestamp of the historical cases matched.
            - Bar chart showing the best-matched sequences. The bar values represent the distance from the selected country sequence.
            
          - **Matched Historical Cases:**
            All the plot of the matched historical cases with the name of the country as title and Date as index. The sequences are ordered by similarity (or lowest distance)."""
        )
    ],style={'marginLeft':50})
        
    ])
# app.layout = html.Div([
#     #html.H1(children='ShapeFinder Risk Prediction Tool',style = {'textAlign': 'center','marginBottom':40,'marginTop':20,'fontFamily': 'Oswald, sans-serif','color': 'red'}),
#     html.Div([
#         dl.Map(center=[38, 0], zoom=2,minZoom=2, children=l_country+[
#             dl.GeoJSON(url='/assets/world_plot.geojson',id='total_c',style={'color': 'black', 'weight': 1, 'opacity': 1, 'fillOpacity': 0})
#         ], style={'width': '100%','height':'100%','backgroundColor': 'white'}, id='map')],style={"display": "flex",'width':'100%','height': '90vh'}),
#     html.Div(id='sel'),
#     html.Div([html.Div(id='plot_test', style={'width': '100%', 'height': '100%', 'margin': '0'}),
#                   html.Div(id='plot_test2', style={'width': '100%', 'height': '100%', 'margin': '0'}),
#                   html.Div(id='plot_test3', style={'width': '100%', 'height': '100%', 'margin': '0'})
#                   ], style={"display": "flex",'width': '100%', 'margin': '0'}),
#     html.Hr(style={'width': '70%','margin':'auto'}),
#     html.Div(id='tite'),
#     html.Div([
#     html.Div(id='plot_test4')
#     ],style={'marginLeft':100})
# ])



@webapp.callback(Output("plot_test", "children"), 
              Output("plot_test2", "children"),
              Output("plot_test3", "children"),
              Output("plot_test4", "children"),
              Output('tite','children'),
              Input("total_c", "clickData"),
              prevent_initial_call=True)

def display_country_plot(feature):
    if feature is not None:
        country_name = feature['properties']['name'] 
        if country_name in hist_df.columns:
            filtered_data = hist_df.loc[:,country_name]
            fig = px.line(x=filtered_data.index, y=filtered_data, title=country_name) # Replace with actual columns
            fig.update_yaxes(visible=True, fixedrange=True)
            fig.update_layout(annotations=[], overwrite=True)
            fig.update_layout(
                showlegend=False,plot_bgcolor="white",margin=dict(t=60,l=40,b=5,r=5),
                xaxis_title='',yaxis_title='',yaxis=dict(showgrid=True),
                title=dict(text=country_name, font=dict(size=20, color='black'), x=0.5))
            fig.update_traces(line=dict(color='black'))
            filtered_data = pred_df.loc[:,country_name]
            f_min = pred_df_min.loc[:,country_name]
            f_max = pred_df_max.loc[:,country_name]
            fig2 = px.line(x=filtered_data.index, y=filtered_data, title="Mean of Past Future").update_traces(line=dict(color='red'))
            fig2.add_scatter(x =filtered_data.index, y = pred_df_min.loc[:,country_name],
                           mode = 'lines',showlegend=True,opacity=0.2,name='Confidence Interval 95%').update_traces(marker=dict(color='red'))
            fig2.add_scatter(x =filtered_data.index, y = pred_df_max.loc[:,country_name],
                           mode = 'lines',showlegend=True,opacity=0.2,name='Confidence Interval 95%').update_traces(marker=dict(color='red'))
            fig2.update_layout(
                showlegend=False,
                plot_bgcolor="white",
                margin=dict(t=60,l=40,b=5,r=5),
                xaxis_title='',
                yaxis_title='',
                yaxis=dict(showgrid=True),
                title=dict(text="Mean of Past Future", font=dict(size=16, color='darkgrey'), x=0.5))
            m_names = [str(i.name)+': '+str(i.index[0].month)+'-'+str(i.index[0].year) for i in new_dict[country_name][:5]]
            m_dist = dist_dict[country_name]
            if len(m_dist) !=0:
                fig3 = px.bar(x=m_names, y=m_dist, title='Best Matches',
                              color_discrete_sequence=['grey']).update_layout(margin=dict(t=60,l=30,b=5,r=5), 
                              xaxis_title='',yaxis_title='',showlegend=False,plot_bgcolor="white", xaxis_tickangle=60,title=dict(text='Best Matches', font=dict(size=16, color='darkgrey'), x=0.5))
            else:
                fig3 = px.bar().update_layout(margin=dict(t=30,l=30,b=5,r=5), 
                xaxis_title='',yaxis_title='',showlegend=False,plot_bgcolor="white",title=dict(text='Best Matches', font=dict(size=16, color='darkgrey'), x=0.5))        
                fig3.update_xaxes(showticklabels=False)
                fig3.update_yaxes(showticklabels=False)                                     
            figs = [generate_subplot(series) for series in new_dict[country_name]]
            rows = []
            for i in range(0, len(figs), 3):
                row = html.Div([dcc.Graph(figure=fig,style={'width': '400px', 'height': '230px'},config=config) for fig in figs[i:i+3]], className='row',style={"display": "flex"})
                rows.append(row)
            
            return (dcc.Graph(figure=fig,style={'width': '400px', 'height': '240px','margin':'0'},config=config),
                    dcc.Graph(figure=fig2,style={'width': '400px', 'height': '240px','margin':'0'},config=config),
                    dcc.Graph(figure=fig3,style={'width': '400px', 'height': '240px','margin':'0'},config=config),
                    rows,html.H3(children='Matched Sequences',style = {'textAlign': 'center','marginBottom':40,'marginTop':20,'color': 'grey'}))

@webapp.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])

def display_page(pathname):
    if pathname == '/about':
        return about_layout
    elif pathname == '/report':
        return report_layout
    else:
        return home_layout
    

webapp.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

if __name__ == '__main__':
    webapp.run_server()
    