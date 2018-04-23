'''
    Author: Dylan Albrecht
    Date: April 23, 2018
'''

import os

import numpy as np
import pandas as pd
import dash
from dash.dependencies import Input
from dash.dependencies import Output
import dash_core_components as dcc
import dash_html_components as html


DATA_FILE = os.path.join('model',
                          'data_clusters_df.csv')
ARCHETYPES_FILE = os.path.join('model',
                               'archetypes_df.csv')

DATA_MIXTURES_FILE = os.path.join('model',
                                  'data_mixtures_df.csv')

DF = pd.read_csv(DATA_FILE, dtype={'zip': np.object})
ARCHETYPES_DF = pd.read_csv(ARCHETYPES_FILE)
DATA_MIXTURES_DF = pd.read_csv(DATA_MIXTURES_FILE,
                               dtype={'zip': np.object})

app = dash.Dash(__name__)

##########
# Layout

BUTTONS = html.Div([
    dcc.Dropdown(
        id='arch_select_id',
        options=[{'label': 'Archetype ' + str(i), 'value': i}
                 for i in range(ARCHETYPES_DF.shape[0])],
        value=0
    )
])

layout = dict(title='zip code cluster',
              width=1000,
              height=700,
              colorbar=True,
              geo=dict(
                  scope='usa',
                  projection=dict(type='albers usa'),
                  showland=True,
                  # landcolor='rgb(250, 250, 250)',
                  subunitcolor='rgb(217, 217, 217)',
                  countrycolor='rgb(217, 217, 217)',
                  countrywidth=0.5,
                  subunitwidth=0.5
              )
             )
map_figure = dict(data=[], layout=layout)
MAP = html.Div([dcc.Graph(id='zip_cluster_graph_id',
                          figure=map_figure)
               ])

LAYOUT = html.Div([
    html.Table(html.Tr([
        html.Td(html.Div([BUTTONS] +
                         [html.Div(id='mixture_components_id')]),
                style={"width": "33%"}),
        html.Td(MAP,
                style={"width": "67%"})
    ])),
    html.Div(id='zip_code_list_id')
])

app.layout = html.Div(children=[LAYOUT])
app.css.append_css({'external_url':
                    ('https://rawgit.com/lwileczek/'
                     'Dash/master/undo_redo5.css')})


#############
# Callbacks

@app.callback(
    Output('zip_cluster_graph_id', 'figure'),
    [Input('arch_select_id', 'value')]
)
def update_graph(value):
    dataframe = DF[DF['cluster'] == value].copy()
    dataframe['zip'] = dataframe['zip'].astype(str).values
    dataframe['zip'] = 'Zip: ' + dataframe['zip']
    data = [dict(type='scattergeo',
                 locationmode='USA-states',
                 lon=dataframe['lng'],
                 lat=dataframe['lat'],
                 text=dataframe['zip'],
                 mode='markers',
                 marker=dict(
                     size=4,
                     opacity=0.4,
                     reversescale=True,
                     autocolorscale=False,
                     symbol='circle',
                     line=dict(
                         width=1,
                         color='rgba(102, 102, 102)'
                     ),
                     cmin=0,
                     color=dataframe['Estimate; SEX AND AGE'
                                     ' - Total population'],
                     cmax=dataframe['Estimate; SEX AND AGE'
                                    ' - Total population'].max(),
                     colorbar=dict(title='Pop')
                 ))]

    layout = dict(title='zip code cluster',
                  width=1000,
                  height=700,
                  colorbar=True,
                  geo=dict(
                      scope='usa',
                      projection=dict(type='albers usa'),
                      showland=True,
                      subunitcolor='rgb(217, 217, 217)',
                      countrycolor='rgb(217, 217, 217)',
                      countrywidth=0.5,
                      subunitwidth=0.5
                  )
                 )

    map_figure = dict(data=data, layout=layout)

    return map_figure


@app.callback(
    Output('mixture_components_id', 'children'),
    [Input('arch_select_id', 'value')]
)
def update_descriptions(value):
    dataframe = ARCHETYPES_DF.iloc[value:value+1, :]

    features = np.array(dataframe.columns)
    sort_idx = np.argsort(dataframe.values.ravel())[::-1]

    table_df = dataframe.iloc[0:1, 0:5].copy()
    table_df.columns = features[sort_idx][:5]

    sorted_entries = dataframe.iloc[0:1, sort_idx].values.ravel()
    table_df.iloc[:, :] = sorted_entries[:5]

    columns = [' - '.join(c.split(' - ')[-2:])
               for c in table_df.columns]

    for i, c in enumerate(columns):
        fmt = '{0} ({1:0.2f})'
        columns[i] = fmt.format(columns[i], sorted_entries[i])

    sort_idx = np.argsort(dataframe.values.ravel())
    table_df.columns = features[sort_idx][:5]

    sorted_entries = dataframe.iloc[0:1, sort_idx].values.ravel()
    table_df.iloc[:,:] = sorted_entries[:5]

    rev_columns = [' - '.join(c.split(' - ')[-2:])
                   for c in table_df.columns]

    for i, c in enumerate(rev_columns):
        fmt = '{0} ({1:0.2f})'
        rev_columns[i] = fmt.format(rev_columns[i], sorted_entries[i])

    return html.Div([html.P(col) for col in columns] +
                    [html.Hr()] +
                    [html.P(col) for col in rev_columns])


@app.callback(
    Output('zip_code_list_id', 'children'),
    [Input('arch_select_id', 'value')]
)
def update_zip_list(value):
    zip_df = DATA_MIXTURES_DF[DATA_MIXTURES_DF['cluster'] == value]
    zip_arch = zip_df[['zip', 'Archetype ' + str(value)]].values
    zip_arch = np.flipud(np.array(sorted(zip_arch, key=lambda x: x[1])))

    zips = zip_arch[:, 0]
    print(zips)
    fmt = '[{0}](http://www.google.com/search?q=zip+code+{1})'
    zip_list = ''
    for zc in zips:
        zip_list += fmt.format(zc, zc)
        zip_list += '\n'

    return dcc.Markdown(zip_list)


if __name__ == '__main__':

    app.run_server(host='0.0.0.0', port=8080, debug=True)
