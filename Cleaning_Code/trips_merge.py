import pandas as pd

taxi_cleaned = pd.read_csv("~/clean_taxi_trips.csv")
rideshare_cleaned = pd.read_csv("~/clean_rideshare_trips.csv")

trips_final = pd.concat((taxi_cleaned,rideshare_cleaned), ignore_index = True)

trips_final = trips_final.drop(["Unnamed: 0", "start_census_tract", "end_census_tract"], axis = 1, errors = "ignore", inplace = True)

trips_final.to_csv(r"~/cleaned_full_trips.csv") # will be used for further calculations

trips_final[["tolls","extra_charges"]] = trips_final[["tolls","extra_charges"]].fillna(0, inplace = True)

trips_final.dropna(axis = 0, inplace = True) # Removing trips that involve pickup or dropoff outside Chicago (have null centroids)

trips_final.to_csv(r"~/final_trips.csv", header = False) # Actual table to be inserted into trips table in DW