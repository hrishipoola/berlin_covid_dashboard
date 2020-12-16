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

[Requirements](https://github.com/hrishipoola/berlin_covid_dashboard/blob/main/covid%20dashboard/requirements.txt)


## Covid Dashboard

[Requirements](https://github.com/hrishipoola/berlin_covid_dashboard/blob/main/covid%20dashboard/requirements.txt)

