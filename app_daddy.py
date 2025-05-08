#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_table
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
import requests

import warnings
warnings.filterwarnings('ignore')


position_select = 'SFLEX'
my_username = ''
draft_id = ''
with open('db/drafted.txt', 'w'):
    pass

players_all = pd.DataFrame(columns = ['player', 'tier', 'value', 'pick', 'rank_diff', 'best', 'avg_plot', 'colors', 'adp'])
players_rb = pd.DataFrame(columns = ['player', 'tier', 'rank_diff', 'best', 'avg_plot', 'colors'])
players_qb = pd.DataFrame(columns = ['player', 'tier', 'rank_diff', 'best', 'avg_plot', 'colors'])
players_wr = pd.DataFrame(columns = ['player', 'tier', 'rank_diff', 'best', 'avg_plot', 'colors'])
players_te = pd.DataFrame(columns = ['player', 'tier', 'rank_diff', 'best', 'avg_plot', 'colors'])
players_flex = pd.DataFrame(columns = ['player', 'tier', 'rank_diff', 'best', 'avg_plot', 'colors'])

players_drafted = pd.DataFrame(columns=['player', 'tier', 'player_id'])

players_all_initial = pd.read_csv('db/players.csv')
with open("db/rankings.txt", "r") as txt_file:
    rankings_select = txt_file.read()
rankings_select = rankings_select.splitlines()
rankings_select = [x.replace('rankings_', '').upper() for x in rankings_select]
players_all_initial['player'][pd.isnull(players_all_initial['my_guys']) == False] = '****   ' + players_all_initial['player'] + '  ****'
with open("db/colors.txt", "r") as txt_file:
    unique_colors = txt_file.read()
unique_colors = unique_colors.splitlines()
players_all_initial['player'] = '  ' + players_all_initial['player']
 

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "Draft Things"

app.layout = html.Div([
dcc.Interval(id = 'data-poll', interval = 10000, n_intervals = 0),
dcc.Interval(id = 'data-update', interval = 5000, n_intervals = 0),

html.Div([
    
    html.Div([
    dcc.RadioItems(id='radio-button-position',
    options=[{'label': 'SFLEX', 'value': 'SFLEX'},
             {'label': 'FLEX', 'value': 'FLEX'},
             {'label': 'QB', 'value': 'QB'},
             {'label': 'RB', 'value': 'RB'},
             {'label': 'WR', 'value': 'WR'},
             {'label': 'TE', 'value': 'TE'}],
    value='SFLEX')],style={'display': 'inline-block', "margin-left": "200px", "margin-top": "50px", "verticalAlign": "top"}),
        
    html.Div([
    dcc.Dropdown(id='rankings-dropdown',
    options=[{'label': i, 'value': i} for i in rankings_select],
    value= rankings_select,
    multi=True)],style={'display': 'inline-block', "margin-left": "200px", "margin-top": "50px", "verticalAlign": "top"}),
    
    
    html.Div([
    dcc.Input(
    id="input-draft-id",
    type="text",
    style={'height': '50px','width': '500px', 'textAlign': 'center'},
    placeholder="Sleeper Draft ID Hurr")
    ],style={'display': 'inline-block', "margin-left": "350px", "margin-top": "50px", "verticalAlign": "top", 'backgroundColor': 'black'})
    
    # html.Div([
    # dcc.Input(
    # id="input-username",
    # type="text",
    # style={'height': '50px','width': '500px', 'textAlign': 'center'},
    # placeholder="Sleeper Username Hurr")
    # ],style={'display': 'inline-block', "margin-left": "200px", "margin-top": "50px", "verticalAlign": "top", 'backgroundColor': 'darkgray'})
    
]),

html.Div([

    html.Div([   
    dcc.Graph(id='graph')
    ],style={'display': 'inline-block', "margin-right": "15px"}),
    
    
    html.Div([
        
        html.Div([
        html.Label("ALL"),
        dash_table.DataTable(
        id='table_players_all',
        columns=[{"name": i, "id": i} for i in ['player', 'tier']],
        data=players_all[['player', 'tier']].to_dict('records'),
        style_data_conditional=([{'if': {'filter_query': '{player} contains "*"','column_id': ['player']},'textAlign': 'left'}] +
                               [{'if': {'filter_query': '{{tier}} = {}'.format(i), 'column_id': ['player', 'tier']}, 'background-color': unique_colors[i], 'color': 'white'} for i in range(len(unique_colors))]),           
        style_cell_conditional=[{'if': {'column_id': 'player'}, 'width': '200px'}, {'if': {'column_id': 'tier'},'width': '75px'}],
        style_header={'backgroundColor': 'darkgray', 'fontWeight': 'bold'},),    
        ],style={'display': 'inline-block', "margin-right": "15px", "margin-top": "110px", "verticalAlign": "top"}),
        
        html.Div([
        
            html.Div([
        
                html.Div([
                html.Label("RB"),
                dash_table.DataTable(
                id='table_players_rb',
                columns=[{"name": i, "id": i} for i in ['player', 'tier']],
                data=players_rb[['player', 'tier']].to_dict('records'),
                style_data_conditional=([{'if': {'filter_query': '{player} contains "*"','column_id': ['player']},'textAlign': 'left'}] +
                                       [{'if': {'filter_query': '{{tier}} = {}'.format(i), 'column_id': ['player', 'tier']}, 'background-color': unique_colors[i], 'color': 'white'} for i in range(len(unique_colors))]),           
                style_cell_conditional=[{'if': {'column_id': 'player'}, 'width': '200px'}, {'if': {'column_id': 'tier'},'width': '75px'}],
                style_header={'backgroundColor': 'darkgray', 'fontWeight': 'bold'},),
                ],style={'display': 'inline-block', "margin-right": "15px"}),
                
                html.Div([
                html.Label("WR"),
                dash_table.DataTable(
                id='table_players_wr',
                columns=[{"name": i, "id": i} for i in ['player', 'tier']],
                data=players_wr[['player', 'tier']].to_dict('records'),
                style_data_conditional=([{'if': {'filter_query': '{player} contains "*"','column_id': ['player']},'textAlign': 'left'}] +
                                       [{'if': {'filter_query': '{{tier}} = {}'.format(i), 'column_id': ['player', 'tier']}, 'background-color': unique_colors[i], 'color': 'white'} for i in range(len(unique_colors))]),           
                style_cell_conditional=[{'if': {'column_id': 'player'}, 'width': '200px'}, {'if': {'column_id': 'tier'},'width': '75px'}],
                style_header={'backgroundColor': 'darkgray', 'fontWeight': 'bold'},),
                ],style={'display': 'inline-block', "margin-right": "15px"}),
            
            ]),
             
            html.Div([
            
                html.Div([
                html.Label("QB"),
                dash_table.DataTable(
                id='table_players_qb',
                columns=[{"name": i, "id": i} for i in ['player', 'tier']],
                data=players_qb[['player', 'tier']].to_dict('records'),
                style_data_conditional=([{'if': {'filter_query': '{player} contains "*"','column_id': ['player']},'textAlign': 'left'}] +
                                       [{'if': {'filter_query': '{{tier}} = {}'.format(i), 'column_id': ['player', 'tier']}, 'background-color': unique_colors[i], 'color': 'white'} for i in range(len(unique_colors))]),           
                style_cell_conditional=[{'if': {'column_id': 'player'}, 'width': '200px'}, {'if': {'column_id': 'tier'},'width': '75px'}],      
                style_header={'backgroundColor': 'darkgray', 'fontWeight': 'bold'},),
                ],style={'display': 'inline-block', "margin-right": "15px"}),
                
                html.Div([
                html.Label("TE"),
                dash_table.DataTable(
                id='table_players_te',
                columns=[{"name": i, "id": i} for i in ['player', 'tier']],
                data=players_te[['player', 'tier']].to_dict('records'),
                style_data_conditional=([{'if': {'filter_query': '{player} contains "*"','column_id': ['player']},'textAlign': 'left'}] + 
                                       [{'if': {'filter_query': '{{tier}} = {}'.format(i), 'column_id': ['player', 'tier']}, 'background-color': unique_colors[i], 'color': 'white'} for i in range(len(unique_colors))]),           
                style_cell_conditional=[{'if': {'column_id': 'player'}, 'width': '200px'}, {'if': {'column_id': 'tier'},'width': '75px'}],
                style_header={'backgroundColor': 'darkgray', 'fontWeight': 'bold'},),
                ],style={'display': 'inline-block', "margin-right": "15px"}),
                
            ]),
            
        ],style={'display': 'inline-block', "margin-top": "100px", "verticalAlign": "top"}),
            
        html.Div([
        html.Label("VALUE"),
        dash_table.DataTable(
        id='table_players_value',
        columns=[{"name": i, "id": i} for i in ['player', 'pick', 'tier']],
        data=players_all[['player', 'pick', 'tier']].to_dict('records'),
        style_data_conditional=[{'if': {'column_id': ['player', 'pick', 'tier']},'backgroundColor': 'mediumseagreen','color': 'white'},
                                {'if': {'filter_query': '{pick} > 12','column_id': ['player', 'pick', 'tier']},'backgroundColor': 'goldenrod','color': 'white'},
                                {'if': {'filter_query': '{pick} > 24','column_id': ['player', 'pick', 'tier']},'backgroundColor': 'indianred','color': 'white'},
                                {'if': {'filter_query': '{player} contains "*"','column_id': ['player']},'textAlign': 'left'}],           
        style_cell_conditional=[{'if': {'column_id': 'player'}, 'width': '200px'}, {'if': {'column_id': 'pick'},'width': '75px'}, {'if': {'column_id': 'tier'},'width': '75px'}],
        style_header={'backgroundColor': 'darkgray', 'fontWeight': 'bold'},),
        ],style={'display': 'inline-block', "margin-right": "15px", "margin-top": "110px", "verticalAlign": "top"})
    
    ],style={'display': 'inline-block', "verticalAlign": "top"}),
    
]),
    

    dcc.Store(id='json-data'),
    dcc.Store(id='drafted-api-placeholder')
    
])




@app.callback(dash.dependencies.Output('drafted-api-placeholder', 'data'), [dash.dependencies.Input('data-poll', 'n_intervals'), dash.dependencies.Input('input-draft-id', 'value')])
def get_drafted(value, draft_id):
    
    #draft_id = '1226206867957493760'
    
    try:
        url = f'http://127.0.0.1:5000/draft-poll/{draft_id}'
        requests.put(url)
    except:
        pass
    
    return 1
           


@app.callback(dash.dependencies.Output('json-data', 'data'), [dash.dependencies.Input('rankings-dropdown', 'value'), dash.dependencies.Input('data-update', 'n_intervals')])
def filter_players_by_drafted(ranking_multi_select, value):
    
    #ombination_id = '111111'
    
    try:
        with open("db/drafted.txt", "r") as txt_file:
            drafted = txt_file.read()
        drafted = drafted.splitlines()
        drafted = [int(x) for x in drafted]
        
        combination_id = ''
        for i in rankings_select:
            if i in ranking_multi_select:
                combination_id += '1'
            else:
                combination_id += '0'
        
        tiers = pd.read_csv(f'tiers/{combination_id}.csv')
        
        try:
            players_drafted = players_all_initial[players_all_initial['sleeper_id'].isin(drafted)].reset_index(drop=True)
            players_all = players_all_initial[~players_all_initial['sleeper_id'].isin(drafted)].reset_index(drop=True)
            players_all = pd.merge(tiers, players_all, how='right', on='sleeper_id')
            players_all = players_all.sort_values('avg_plot', ascending=False)
        except:
            players_drafted = pd.DataFrame(columns=['player', 'tier', 'player_id'])
            players_all = players_all_initial
        players_qb = players_all[players_all['position'] == 'QB'].reset_index(drop=True)
        players_rb = players_all[players_all['position'] == 'RB'].reset_index(drop=True)
        players_wr = players_all[players_all['position'] == 'WR'].reset_index(drop=True)
        players_te = players_all[players_all['position'] == 'TE'].reset_index(drop=True)
        players_flex = players_all[players_all['position'] != 'QB'].reset_index(drop=True)
    except:
        players_all = pd.DataFrame(columns = ['player', 'tier', 'value', 'pick', 'rank_diff', 'best', 'avg_plot', 'colors', 'adp'])
        players_rb = pd.DataFrame(columns = ['player', 'tier', 'rank_diff', 'best', 'avg_plot', 'colors'])
        players_qb = pd.DataFrame(columns = ['player', 'tier', 'rank_diff', 'best', 'avg_plot', 'colors'])
        players_wr = pd.DataFrame(columns = ['player', 'tier', 'rank_diff', 'best', 'avg_plot', 'colors'])
        players_te = pd.DataFrame(columns = ['player', 'tier', 'rank_diff', 'best', 'avg_plot', 'colors'])
        players_flex = pd.DataFrame(columns = ['player', 'tier', 'rank_diff', 'best', 'avg_plot', 'colors'])
        players_drafted = pd.DataFrame(columns=['player', 'tier', 'player_id'])
    
    drafted_len = players_drafted.shape[0]
    players_drafted = players_drafted.to_json()
    players_all = players_all.to_json()
    players_qb = players_qb.to_json()
    players_rb = players_rb.to_json()
    players_wr = players_wr.to_json()
    players_te = players_te.to_json()
    players_flex = players_flex.to_json()
    
    players_dict = {
                    'SFLEX':players_all,
                    'DRAFT':players_drafted,
                    'QB':players_qb,
                    'RB':players_rb,
                    'WR':players_wr,
                    'TE':players_te,
                    'FLEX':players_flex,
                    'DRAFTED_LEN': drafted_len
                    }
    return players_dict

    

@app.callback(dash.dependencies.Output('table_players_all','data'), dash.dependencies.Input('json-data', 'data'))
def update_table_players_all(players_dict):
    players_all = pd.read_json(players_dict['SFLEX'])
    return players_all.iloc[:41][['player', 'tier']].to_dict('records')

@app.callback(dash.dependencies.Output('table_players_qb','data'), dash.dependencies.Input('json-data', 'data'))
def update_table_players_qb(players_dict):
    players_qb = pd.read_json(players_dict['QB'])
    return players_qb.iloc[:20][['player', 'tier']].to_dict('records')

@app.callback(dash.dependencies.Output('table_players_rb','data'), dash.dependencies.Input('json-data', 'data'))
def update_table_players_rb(players_dict):
    players_rb = pd.read_json(players_dict['RB'])
    return players_rb.iloc[:20][['player', 'tier']].to_dict('records')

@app.callback(dash.dependencies.Output('table_players_wr','data'), dash.dependencies.Input('json-data', 'data'))
def update_table_players_wr(players_dict):
    players_wr = pd.read_json(players_dict['WR'])
    return players_wr.iloc[:20][['player', 'tier']].to_dict('records')

@app.callback(dash.dependencies.Output('table_players_te','data'), dash.dependencies.Input('json-data', 'data'))
def update_table_players_te(players_dict):
    players_te = pd.read_json(players_dict['TE'])
    return players_te.iloc[:20][['player', 'tier']].to_dict('records')

@app.callback(dash.dependencies.Output('table_players_value','data'), dash.dependencies.Input('json-data', 'data'))
def update_table_players_value(players_dict):
    pick_number = players_dict['DRAFTED_LEN']
    players_all = pd.read_json(players_dict['SFLEX'])
    players_all['pick'] = players_all['adp'] - pick_number
    players_all['pick'] = players_all['pick'].round(2)
    return players_all.iloc[:53][['player', 'value', 'pick', 'tier']][players_all['value'] < -6].iloc[:41].to_dict('records')

@app.callback(dash.dependencies.Output('graph', 'figure'), [dash.dependencies.Input('json-data', 'data'), dash.dependencies.Input('radio-button-position', 'value')])
def network_graph(players_dict, position_select):

    
    #dataframe = players_all
    dataframe = pd.read_json(players_dict[position_select])[:41]
    best_ranks = dataframe['best'].tolist()[::-1]
    best_ranks_max = dataframe['best'].max()
    worst_ranks = dataframe['rank_diff'].tolist()[::-1]
    worst_ranks_min = dataframe['best'] + dataframe['rank_diff']
    worst_ranks_min = worst_ranks_min.min()
    average_ranks = dataframe['avg_plot'] + .00125
    average_ranks = average_ranks.tolist()[::-1]
    players = dataframe['player'].tolist()[::-1]
    
    axis_min = worst_ranks_min - ((best_ranks_max - worst_ranks_min) * .125)
    axis_max = best_ranks_max*1.05
    
    figure = go.Figure(
                        data=[
                            go.Bar(
                                    x = worst_ranks,
                                    base = best_ranks,
                                    hovertext = dataframe['tier'].to_list()[::-1],
                                    hoverinfo = 'skip',
                                    text = players,
                                    textposition = 'outside',
                                    marker = dict(color=dataframe['colors'].to_list()[::-1]),
                                    orientation = 'h',
                                    width = .5),
                            go.Bar(
                                    x = [-.0025]*len(dataframe),
                                    base = average_ranks,
                                    hoverinfo = 'skip',
                                    marker = dict(color=['lightgray']*len(dataframe)),
                                    orientation = 'h',
                                    width = .5)
                             ]
                      )
    figure.update_layout(
                        barmode='stack',
                        autosize=False,
                        width=1500,
                        height=1500,
                        template="plotly_dark",
                        showlegend=False
                        )
    figure.update_xaxes(range=[axis_min, axis_max])

    return figure


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=8050)
