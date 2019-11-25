import pandas as pd

taxi_trip_df = pd.read_csv("~/taxi_trips.csv")

columns_to_delete = ["Taxi ID",
                     "Pickup Community Area",
                     "Dropoff Community Area",
                     "Company",
                     "Pickup Centroid Latitude",
                     "Pickup Centroid Longitude",
                     "Dropoff Centroid Latitude",
                     "Dropoff Centroid Longitude",]

new_column_names = ["trip_id", 
           "start_timestamp_id", 
           "end_timestamp_id", 
           "duration_seconds", 
           "miles", 
           "start_census_tract", 
           "end_census_tract", 
           "fare", 
           "tip", 
           "tolls", 
           "extra_charges", 
           "trip_total", 
           "payment_type",
           "pickup_centroid_location",
           "dropoff_centroid_location"]

taxi_trip_df = taxi_trip_df.drop(columns_to_delete, axis = 1)
taxi_trip_df.columns = new_column_names
taxi_trip_df["ride_type_id"] = 1

taxi_trip_df = taxi_trip_df[["trip_id",
                "ride_type_id",
                "start_timestamp_id",
                "end_timestamp_id",
                "duration_seconds",
                "miles",
                "fare",
                "tip",
                "tolls",
                "extra_charges",
                "trip_total",
                "payment_type",
                "start_census_tract",
                "end_census_tract",
                "pickup_centroid_location",
                "dropoff_centroid_location"]]

taxi_trip_df.start_timestamp_id = pd.to_datetime(taxi_trip_df.start_timestamp_id)
taxi_trip_df.end_timestamp_id = pd.to_datetime(taxi_trip_df.end_timestamp_id)

def hour_rounder(t):
  return (t.dt.floor('H'))

taxi_trip_df.start_timestamp_id = hour_rounder(pd.to_datetime(taxi_trip_df.start_timestamp_id))
taxi_trip_df.end_timestamp_id = hour_rounder(pd.to_datetime(taxi_trip_df.end_timestamp_id))

taxi_trip_df.to_csv(r"~/clean_taxi_trips.csv")

