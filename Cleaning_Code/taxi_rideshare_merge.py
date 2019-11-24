import pandas as pd

taxi_cleaned = pd.read_csv("clean_taxi_trips.csv")
rideshare_cleaned = pd.read.csv("clean_rideshare_trips.csv")

trips_final = taxi_cleaned.merge(rideshare_cleaned, on = "trip_id")
trips_final.to_csv(r"merged_taxi_rideshare.csv")
