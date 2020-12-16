import pandas as pd
import numpy as np
from datetime import datetime

import plotly.express as px
import plotly.offline as pyo
import plotly.graph_objs as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from urllib.request import urlopen
import json # library to handle JSON files
from pandas.io.json import json_normalize # tranform JSON file into a pandas dataframe

from geojson_rewind import rewind

# Read in data that we scraped and created
rolling_7_long = pd.read_csv('https://raw.githubusercontent.com/hrishipoola/berlin_covid_dashboard/main/covid%20scrape/rolling_7_long.csv', parse_dates=['Date'], index_col='Date')
incidence = pd.read_csv('https://raw.githubusercontent.com/hrishipoola/berlin_covid_dashboard/main/covid%20scrape/incidence.csv', parse_dates=['Date'], index_col='Date')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

markdown_text = '''
## Berlin Covid Dashboard

This diashboard explores Berin's covid profile and evolution by district. It was borne
out of the fact that I, along with other Berliners, have friends and colleagues scattered across districts and
needed a way to understand, visualize, and explore covid epidemiology on a district level. The purpose
of this dashboard is to help fellow Berliners make more informed personal decisions and policymakers and
health agencies allocate resources. It includes rolling 7-day average number of cases, statistical spread
of daily incidence, average daily incidence, and an average daily incidence map. Users can dig deeper
by selecting start and end dates and using hover, box & lasso select, zoom, and download tooltips.

High level takeaways:

1) Overall 7-day average number of cases have improved since November 17, 2020 ('lockdown lite' began on October 26, 2020),
though they've ticked up again since December 3, 2020 (a hard lockdown was reinstated on December 16, 2020)

2) Berlin’s recent rolling 7-day averages of confirmed cases is roughly 6x of the peak of the 1st wave in late March.
The highest case averages are in Mitte, Neukolln, Tempelhof-Shoneberg, and Friedrichshain-Kreuzberg.

3) Mitte, Friedrichshain-Kreuzberg, and Neukolln feature the highest 7-day average incidence (per 100,000) IQR and most higher-end outliers.
Pankow, Charlottenburg-Wilmersdorf, Treptow-Kopenick, Steglitz have a lower median and spread (tighter distribution). Spandau
has picked up in the past few weeks as a growing hotspot in terms of covid incidence.

4) Taken together, Mitte and Neukolln, even accounting for differences in population (though we don’t incorporate population density),
have fared worse than districts like Pankow, which includes Prenzlauer Berg, and Charlottenburg-Wilmersdorf.

Daily district-level confirmed case data was scraped from
[Das Landesamt für Gesundheit und Soziales](https://www.berlin.de/lageso/gesundheit/infektionsepidemiologie-infektionsschutz/corona/tabelle-bezirke-gesamtuebersicht/).
Demographic data by district, used to calculate incidence per 100,000, was scraped
from [Wikipedia](https://en.wikipedia.org/wiki/Demographics_of_Berlin). While population
data dates from the last census in Germany in 2010 and Berlin’s population has grown dramatically
since then, it’s sufficient for the purpose here of calculating an approximate incidence
to make comparisons. Not factored in are exogenous variables like
increased testing and the fact that the true positivity rate in the population may be much higher
than that indicated by confirmed positive tests.

If you want to learn more, give us a shout at info@crawstat.com!
'''

app.layout = html.Div([
    dcc.Tabs(id='dash-tabs', value='tab-1', children=[
        dcc.Tab(label='Berlin Covid Dashboard', value='tab-1'),
        dcc.Tab(label='Rolling 7-Day Average Cases', value='tab-2'),
        dcc.Tab(label='Daily Incidence Statistical Spread', value='tab-3'),
        dcc.Tab(label='Average Daily Incidence', value='tab-4'),
        dcc.Tab(label='Map', value='tab-5')
    ], colors={'border': 'white',
               'primary': 'darkturquoise',
               'background': 'whitesmoke'}),
    html.Div(id='dash-tabs-content')
])

@app.callback(Output('dash-tabs-content', 'children'),
              Input('dash-tabs', 'value'))


def render_content(tab):
    if tab == 'tab-1':
        return html.Div([dcc.Markdown(children=markdown_text)
        ], style={'fontFamily':'Helvetica'})

    if tab == 'tab-2':
        return html.Div([
                     html.H4('Rolling 7-Day Average Number of Cases'),
                     html.Div([
                               html.H6('Select start and end dates:'),
                               dcc.DatePickerRange(id='date_picker1',
                                                   min_date_allowed=datetime(2020,3,9),
                                                   max_date_allowed=datetime(2020,12,15),
                                                   start_date=datetime(2020,3,9),
                                                   end_date=datetime(2020,12,15),
                                                   display_format='MMM D, YYYY')
                              ],style={'display':'inline-block',
                                       'verticalAlign':'top',
                                       'width':'30%',
                                       'vertical':'40%'},
                                       ),
                     html.Div([
                              html.Button(id='submit-button1',
                                          n_clicks=0,
                                          children='Submit',
                                          style={'fontSize':12})
                              ],style={'display':'inline-block',
                                       'verticalAlign':'bottom'}),
                     html.Div([
                              dcc.Graph(id='bar_graph')
                              ])
        ], style={'fontFamily':'Helvetica'})

    elif tab == 'tab-3':
        return html.Div([
                     html.H4('Daily Incidence Statistical Spread (per 100,000)'),
                     html.Div([
                               html.H6('Select start and end dates:'),
                               dcc.DatePickerRange(id='date_picker2',
                                                   min_date_allowed=datetime(2020,3,9),
                                                   max_date_allowed=datetime(2020,12,15),
                                                   start_date=datetime(2020,3,9),
                                                   end_date=datetime(2020,12,15),
                                                   display_format='MMM D, YYYY')
                              ],style={'display':'inline-block','verticalAlign':'top','width':'30%', 'vertical':'40%'}),
                     html.Div([
                              html.Button(id='submit-button2',
                                          n_clicks=0,
                                          children='Submit',
                                          style={'fontSize':12})
                              ],style={'display':'inline-block', 'verticalAlign':'bottom'}),
                     html.Div([
                              dcc.Graph(id='box_graph')
                              ])
        ], style={'fontFamily':'Helvetica'})

    elif tab == 'tab-4':
        return html.Div([
                    html.H4('Average Daily Incidence (per 100,000)'),
                    html.Div([
                            html.H6('Select start and end dates:'),
                            dcc.DatePickerRange(id='date_picker3',
                                                min_date_allowed=datetime(2020,3,9),
                                                max_date_allowed=datetime(2020,12,15),
                                                start_date=datetime(2020,11,11),
                                                end_date=datetime(2020,12,15),
                                                display_format='MMM D, YYYY')
                                ],style={'display':'inline-block','verticalAlign':'top','width':'30%', 'vertical':'40%'}),
                    html.Div([
                            html.Button(id='submit-button3',
                                      n_clicks=0,
                                      children='Submit',
                                      style={'fontSize':12})
                            ],style={'display':'inline-block', 'verticalAlign':'bottom'}),
                    html.Div([
                            dcc.Graph(id='bar_graph_incidence')
                            ])
    ], style={'fontFamily':'Helvetica'})

    elif tab == 'tab-5':
        return html.Div([
                    html.H4('Map of Average Daily Incidence (per 100,000)'),
                    html.Div([
                            html.H6('Select start and end dates:'),
                            dcc.DatePickerRange(id='date_picker4',
                                                min_date_allowed=datetime(2020,3,9),
                                                max_date_allowed=datetime(2020,12,15),
                                                start_date=datetime(2020,11,11),
                                                end_date=datetime(2020,12,15),
                                                display_format='MMM D, YYYY')
                                ],style={'display':'inline-block','verticalAlign':'top','width':'30%', 'vertical':'40%'}),
                    html.Div([
                            html.Button(id='submit-button4',
                                      n_clicks=0,
                                      children='Submit',
                                      style={'fontSize':12})
                            ],style={'display':'inline-block', 'verticalAlign':'bottom'}),
                    html.Div([
                            dcc.Graph(id='incidence_map')
                            ])
    ], style={'fontFamily':'Helvetica'})


# Tab 2 callback

@app.callback(Output('bar_graph', 'figure'),
             [Input('submit-button1','n_clicks')],
             [State('date_picker1','start_date'),
              State('date_picker1','end_date')])

def update_bar_graph(n_clicks, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')

    filtered_df = rolling_7_long[(rolling_7_long.index >= start) & (rolling_7_long.index <= end)]

    fig1 = px.bar(filtered_df,
                 x=filtered_df.index,
                 y='Cases',
                 color='District',
                 color_discrete_sequence=['rgb(27,158,119)', 'rgb(217,95,2)', 'rgb(117,112,179)', 'rgb(231,41,138)', 'rgb(102,166,30)', 'rgb(230,171,2)',
                                          'rgb(166,118,29)', 'rgb(102,102,102)', '#1CA71C','#2E91E5','#778AAE','#E15F99'],
                 width=1250,
                 height=475)

    fig1.update_layout(hovermode='closest')

    return fig1

# Tab 3 callback

@app.callback(Output('box_graph', 'figure'),
             [Input('submit-button2','n_clicks')],
             [State('date_picker2','start_date'),
              State('date_picker2','end_date')])

def update_box_graph(n_clicks, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')

    filtered_df = incidence[(incidence.index >= start) & (incidence.index <= end)]

    fig2 = px.box(filtered_df,
             x='Incidence',
             y='District',
             color='District',
             points='all',
             notched=True,
             color_discrete_sequence=px.colors.qualitative.Set2,
             width=1250,
             height=475)

    fig2.update_layout(hovermode='closest')

    return fig2

# Tab 4 callback

@app.callback(Output('bar_graph_incidence', 'figure'),
             [Input('submit-button3','n_clicks')],
             [State('date_picker3','start_date'),
              State('date_picker3','end_date')])

def update_bar_graph_incidence(n_clicks, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')

    filtered_df = incidence[(incidence.index >= start) & (incidence.index <= end)]

    # Create districts dataframe, group mean numbers by district, sort
    districts = filtered_df.groupby(['District']).mean().sort_values(by='Incidence')

    # Plotly express plot
    fig3 = px.bar(districts,
                 x='Incidence',
                 y=districts.index,
                 #title='Average 7-Day Incidence by District',
                 color_discrete_sequence=['darkturquoise'],
                 width = 1250,
                 height=475)

    return fig3

# Tab 5 callback

@app.callback(Output('incidence_map', 'figure'),
             [Input('submit-button4','n_clicks')],
             [State('date_picker4','start_date'),
              State('date_picker4','end_date')])

def incidence_map(n_clicks, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')

    filtered_df = incidence[(incidence.index >= start) & (incidence.index <= end)]

    # Create districts dataframe, group mean numbers by district, sort
    districts = filtered_df.groupby(['District']).mean().sort_values(by='Incidence')

    # Reset index
    districts.reset_index(inplace=True)

    # Load geojson for belin districts
    with urlopen('https://raw.githubusercontent.com/pape1412/airbnb/master/data/berlin_neighbourhood_groups.geojson') as response:
        berlin_districts = json.load(response)

    # Check the property key that we need to match - it's Gemeinde_name
    berlin_districts['features'][0]['properties']

    # Rewind geojson to create map
    districts_rewound = rewind(berlin_districts,rfc7946=False)

    fig4 = px.choropleth(districts,
                        geojson=districts_rewound,
                        locations='District',
                        color='Incidence',
                        color_continuous_scale='Deep',
                        featureidkey='properties.Gemeinde_name',
                        projection="mercator",
                        )

    fig4.update_geos(fitbounds='locations', visible=False)

    fig4.update_layout(height=450)
    fig4.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig4

if __name__ == '__main__':
    app.run_server()
