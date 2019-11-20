import pandas as pd
from datetime import datetime, timedelta

taxi_trip_df = pd.read_csv("Taxi_Trips.csv")

columns_to_delete = ["taxi id",
                     "pickup community area",
                     "dropoff community area",
                     "company",
                     "pickup centroid latitude",
                     "pickup centroid longitude",
                     "pickup centroid location",
                     "dropoff centroid latitude",
                     "dropoff centroid longitude",
                     "dropoff centroid location"]

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
           "payment_type"]

columns_to_add = ["ride_type_id",
                  "start_segment_id", 
                  "end_segment_id"] 

taxi_trip_df.drop(columns_to_delete, axis = 1)
taxi_trip_df = new_column_names
taxi_trip_df = pd.concat([taxi_trip_df, columns_to_add])

taxi_trip_df = ["taxi id",
                "ride_type_id",
                "pickup community area",
                "dropoff community area",
                "company",
                "pickup centroid latitude",
                "pickup centroid longitude",
                "pickup centroid location",
                "dropoff centroid latitude",
                "dropoff centroid longitude",
                "dropoff centroid location",
                "start_segment_id", 
                "end_segment_id"]

now = datetime.now()

def hour_rounder(t):
  return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour) + timedelta(hours=t.minute//30)

taxi_trip_df.start_timestamp_id = hour_rounder(pd.to_datetime(taxi_trip_df.start_timestamp_id))
taxi_trip_df.end_timestamp_id = hour_rounder(pd.to_datetime(taxi_trip_df.end_timestamp_id))

taxi_trip_df["ride_type_id"] = 1

taxi_trip_df.ro_csv(r"clean_taxi_trip_data.csv")

