############################## This script has been disposed because the VM doesn't have enough memory ##################
############################## Having more memory OR splitting this script could solve that problem, but the DW would need adjusting ##################

import pandas as pd

full_trips = pd.read_csv("~/cleaned_full_trips.csv")
trip_region = pd.read_csv("~/trip_region_lookup.csv")

full_trips = full_trips.fillna("Missing", inplace = True)

lookup_dic = {}
for i in range(len(trip_region)):
    k = trip_region["trip_centroids"][i]
    v = trip_region["trip_region_id"][i]
    lookup_dic[k] = v


full_trips["pickup_trip_region_id"] = full_trips["pickup_centroid_location"].map(lookup_dic)

full_trips["dropoff_trip_region_id"] = full_trips["dropoff_centroid_location"].map(lookup_dic)

full_trips = full_trips.drop(["dropoff_centroid_location",
                              "pickup_centroid_location",
                              "trip_centroids",
                              "base_region_id"],
                             axis = 1,
                             errors = "ignore",
                             inplace = True)

full_trips.to_csv(r"~/cleaned_full_trips_final.csv")