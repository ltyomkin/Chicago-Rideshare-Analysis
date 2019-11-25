import pandas as pd

taxi_cleaned = pd.read_csv("~/clean_taxi_trips.csv")
rideshare_cleaned = pd.read_csv("~/clean_rideshare_trips.csv")

trips_final = pd.concat((taxi_cleaned,rideshare_cleaned))

trips_final = trips_final.drop(["Unnamed: 0", "start_census_tract", "end_census_tract"], axis = 1, errors = "ignore")

trips_final.to_csv(r"~/cleaned_full_trips.csv")