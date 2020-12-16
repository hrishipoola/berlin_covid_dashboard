# Berlin Covid Dashboard

https://covidberlin.herokuapp.com/

This dashboard explores Berlin's covid profile and evolution by district. It was borne out of the fact that I, along with other Berliners, have friends and colleagues scattered across districts and needed a way to understand, visualize, and explore covid epidemiology on a district level. The purpose of this dashboard is to help fellow Berliners make more informed personal decisions and policymakers and health agencies allocate resources. It includes rolling 7-day average number of cases, statistical spread of daily incidence, average daily incidence, and an average daily incidence map. Users can dig deeper by selecting start and end dates and using hover, box & lasso select, zoom, and download tooltips.

Daily district-level confirmed case data was scraped from Das Landesamt für Gesundheit und Soziales. Demographic data by district, used to calculate incidence per 100,000, was scraped from Wikipedia. While population data dates from the last census in Germany in 2010 and Berlin’s population has grown dramatically since then, it’s sufficient for the purpose here of calculating an approximate incidence to make comparisons. Not factored in are exogenous variables like increased testing and the fact that the true positivity rate in the population may be much higher than that indicated by confirmed positive tests.

High level takeaways:

1) Overall 7-day average number of cases have improved since November 17, 2020 ('lockdown lite' began on October 26, 2020), though they've ticked up again since December 3, 2020 (a hard lockdown was reinstated on December 16, 2020)

2) Berlin’s recent rolling 7-day averages of confirmed cases is roughly 6x of the peak of the 1st wave in late March. The highest case averages are in Mitte, Neukolln, Tempelhof-Shoneberg, and Friedrichshain-Kreuzberg.

3) Mitte, Friedrichshain-Kreuzberg, and Neukolln feature the highest 7-day average incidence (per 100,000) IQR and most higher-end outliers. Pankow, Charlottenburg-Wilmersdorf, Treptow-Kopenick, Steglitz have a lower median and spread (tighter distribution). Spandau has picked up in the past few weeks as a growing hotspot in terms of covid incidence.

4) Taken together, Mitte and Neukolln, even accounting for differences in population (though we don’t incorporate population density), have fared worse than districts like Pankow, which includes Prenzlauer Berg, and Charlottenburg-Wilmersdorf.

If you want to learn more, give us a shout at info@crawstat.com!

## Covid Scrape

### Requirements
appdirs==1.4.4
attrs==20.3.0
beautifulsoup4==4.9.3
Brotli==1.0.9
bs4==0.0.1
certifi==2020.12.5
chardet==3.0.4
click==7.1.2
cycler==0.10.0
Cython==0.29.21
dash==1.17.0
dash-core-components==1.13.0
dash-html-components==1.1.1
dash-renderer==1.8.3
dash-table==4.11.0
DateTime==4.3
decorator==4.4.2
distlib==0.3.1
filelock==3.0.12
Flask==1.1.2
Flask-Compress==1.8.0
future==0.18.2
geojson-rewind==0.2.0
idna==2.10
ipython-genutils==0.2.0
itsdangerous==1.1.0
Jinja2==2.11.2
jsonschema==3.2.0
jupyter-core==4.7.0
kiwisolver==1.3.1
lxml==4.6.2
MarkupSafe==1.1.1
matplotlib==3.3.3
nbformat==5.0.8
numpy==1.19.4
pandas==1.1.4
pandas-datareader==0.9.0
Pillow==8.0.1
plotly==4.13.0
pyparsing==2.4.7
pyrsistent==0.17.3
python-dateutil==2.8.1
pytz==2020.4
requests==2.25.0
retrying==1.3.3
scipy==1.5.4
seaborn==0.11.0
six==1.15.0
soupsieve==2.0.1
traitlets==5.0.5
urllib3==1.26.2
urlopen==1.0.0
virtualenv==20.2.1
Werkzeug==1.0.1
zope.interface==5.2.0



## Covid Dashboard

### Requirements
Brotli==1.0.9
certifi==2020.12.5
chardet==3.0.4
click==7.1.2
dash==1.18.1
dash-core-components==1.14.1
dash-html-components==1.1.1
dash-renderer==1.8.3
dash-table==4.11.1
DateTime==4.3
Flask==1.1.2
Flask-Compress==1.8.0
future==0.18.2
geojson==2.5.0
geojson-rewind==0.2.0
gunicorn==20.0.4
idna==2.10
itsdangerous==1.1.0
Jinja2==2.11.2
MarkupSafe==1.1.1
numpy==1.19.4
pandas==1.1.5
patsy==0.5.1
plotly==4.14.1
plotly-express==0.4.1
python-dateutil==2.8.1
pytz==2020.4
requests==2.25.0
retrying==1.3.3
scipy==1.5.4
six==1.15.0
statsmodels==0.12.1
urllib3==1.26.2
urlopen==1.0.0
Werkzeug==1.0.1
zope.interface==5.2.0

