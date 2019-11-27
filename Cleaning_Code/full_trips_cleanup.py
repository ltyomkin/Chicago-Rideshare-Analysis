import pandas as pd

full_trips = pd.read_csv("~/cleaned_full_trips.csv")
trip_region = pd.read_csv("~/trip_region_lookup.csv")

full_trips = full_trips.fillna("Missing", inplace = True)

### REMOVE
missing_region = pd.DataFrame({"trip_region_id" : [max(trip_region["trip_region_id"])+1],
                               "base_region_id" : [max(trip_region["base_region_id"])+1],
                               "trip_centroids" : ["Missing"]})

trip_region = trip_region.append(missing_region, ignore_index = True)
####


full_trips = pd.merge(full_trips,
                      trip_region,
                      left_on = "dropoff_centroid_location",
                      right_on = "trip_centroids",
                      how = "left")

full_trips = full_trips.drop(["Unnamed: 0_x",
                              "dropoff_centroid_location",
                              "pickup_centroid_location",
                              "Unnamed: 0_y",
                              "trip_centroids",
                              "base_region_id"],
                             axis = 1,
                             errors = "ignore",
                             inplace = True)

full_trips = full_trips("Missing", "", inplace = True)

full_trips.to_csv(r"~/cleaned_full_trips.csv")