import pandas as pd
import numpy as np
from datetime import datetime

# Web scraping using BeautifulSoup and converting to pandas dataframe
import requests
import urllib.request
import json # library to handle JSON files
from pandas.io.json import json_normalize # tranform JSON file into a pandas dataframe
from urllib.request import urlopen
from bs4 import BeautifulSoup

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def covid_scrape():
    global covid_raw
    url1 = ('https://www.berlin.de/lageso/gesundheit/infektionsepidemiologie-infektionsschutz/corona/tabelle-bezirke-gesamtuebersicht/')
    site1 = urlopen(url1)
    soup1 = BeautifulSoup(site1, 'lxml')

    # Create table object to extract the raw table inside that webpage
    table1 = soup1.find_all('table')

    # Scrape just the new case by district table, which is the 1st table and convert it into a dataframe
    covid_raw = pd.read_html(str(table1[0]), index_col=None, header=0)[0]

    return covid_raw


def covid_wide_dataframe():
    global covid
    # Change column names to English and spell out district acroynyms. Remove the last row of null values
    covid = covid_raw.rename(columns={'Datum': 'Date', 'MI': 'Mitte', 'FK':'Friedrichshain-Kreuzberg', 'PA':'Pankow', 'CW': 'Charlottenburg-Wilmersdorf', 'SP':'Spandau', 'SZ':'Steglitz-Zehlendorf','TS':'Tempelhof-Schöneberg','NK':'Neukölln','TK':'Treptow-Köpenick','MH':'Marzahn-Hellersdorf','LI':'Lichtenberg','RD':'Reinickendorf'}).dropna()

    # Non-date values are floats. Change data type of values to integers. Change type of Date column to datetime
    covid = covid.astype({'Mitte':int, 'Friedrichshain-Kreuzberg':int,'Pankow':int,'Charlottenburg-Wilmersdorf':int,'Spandau':int,'Steglitz-Zehlendorf':int,'Tempelhof-Schöneberg':int,'Neukölln':int,'Treptow-Köpenick':int, 'Marzahn-Hellersdorf':int,'Lichtenberg':int,'Reinickendorf':int})

    covid['Date'] = pd.to_datetime(covid['Date'].str.strip(), infer_datetime_format=True, dayfirst=True).dt.strftime('%Y-%m-%d')

    return covid

def covid_long_dataframe():

    global covid_long
    # Convert to long format using .melt. Set variable name to District and value name to Cases
    covid_long = covid.melt(id_vars=['Date'], var_name = 'District', value_name='Cases')

    # Set index to Date
    covid_long.set_index('Date', inplace=True)

    # Convert index to datetime type
    covid_long.index = pd.to_datetime(covid_long.index)

    return covid_long

def rolling_7_dataframe():

    global rolling_7_long
    # Set index to date
    covid.set_index('Date', inplace=True)

    # Convert index to datetime type
    covid.index = pd.to_datetime(covid.index)

    # Create dataframe for rolling 7-day average of cases
    rolling_7 = covid.rolling(7).mean()

    # Reshape dataframe from wide to long for easier analysis and plotting

    # Reset index
    rolling_7_long = rolling_7.reset_index()

    # Change index column name to month
    rolling_7_long.rename(columns={'index':'Date'})

    # Convert to long format using .melt. Set variable name to District and value name to Cases
    rolling_7_long = rolling_7_long.melt(id_vars=['Date'], var_name = 'District', value_name='Cases').dropna()

    # Set index to Date
    rolling_7_long.set_index('Date', inplace=True)

    return rolling_7_long

def population_scrape():

        global population_raw
        url2 = ('https://en.wikipedia.org/wiki/Demographics_of_Berlin')
        site2 = urlopen(url2)
        soup2 = BeautifulSoup(site2, 'lxml')

        # Create table object to extract the raw table inside that webpage
        table2 = soup2.find_all('table')

        # Scrape just population by district table, which is the 3rd table and convert it into a dataframe
        population_raw = pd.read_html(str(table2[4]), index_col=None, header=0)[0]

        return population_raw

def population_dataframe():

        global population
        # Edit population dataframe
        population = population_raw.rename(columns={'Borough': 'District'})

        # Keep only population column
        keep = ['District','Population 2010']
        population = population[keep]

        # Drop last row (Total Berlin) as we're focusing on district breakouts
        population.drop(population.tail(1).index, inplace=True)

        return population

def incidence_dataframe():

        global incidence

        # Calculate incidence per 100000
        # Assign new Incidence column by mapping District from cases dataframe to index of population dataframe, dividing cases by population, multiplying by 100000
        incidence = covid_long.assign(Incidence=(covid_long.Cases / covid_long.District.map(population.set_index('District')['Population 2010']))*100000).dropna()

        return incidence

covid_scrape()
covid_wide_dataframe()
covid_long_dataframe()
rolling_7_dataframe()
population_scrape()
population_dataframe()
incidence_dataframe()

# Export needed dataframes as csv
#covid_raw.to_csv(r'/users/hpoola/Desktop/covid_raw.csv')
#covid.to_csv(r'/users/hpoola/Desktop/covid.csv')
#covid_long.to_csv(r'/users/hpoola/Desktop/covid_long.csv')
rolling_7_long.to_csv(r'/users/hpoola/Desktop/berlin_covid_dash/rolling_7_long.csv')
#population_raw.to_csv(r'/users/hpoola/Desktop/population_raw.csv')
#population.to_csv(r'/users/hpoola/Desktop/population.csv')
incidence.to_csv(r'/users/hpoola/Desktop/berlin_covid_dash/incidence.csv')
