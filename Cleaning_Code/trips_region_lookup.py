import math
import pandas as pd


base_regions = pd.read_csv("~/clean_regions.csv")

base_regions.columns = base_regions.columns.to_series().apply(lambda x: x.strip())

base_regions = base_regions[["region_id",
                     "north",
                     "west"]]

base_regions.dropna()

trip_regions = pd.read_csv("~/cleaned_full_trips.csv")

starts = pd.DataFrame({"location" : trip_regions.pickup_centroid_location.unique()})
ends = pd.DataFrame({"location" : trip_regions.dropoff_centroid_location.unique()})

r = pd.concat((starts,ends))

trip_regions = pd.DataFrame({"location" : r["location"].unique()}).dropna()

# Split point. Source: https://chrisalbon.com/python/data_wrangling/pandas_split_lat_and_long_into_variables/

# Create two lists for the loop results to be placed
lat = []
lon = []

# For each row in a varible,
for row in trip_regions['location']:
        lo = row.split(' ')[1].replace("(","")
        la = row.split(' ')[2].replace(")","")
        lat.append(float(la))
        lon.append(float(lo))

# Create two new columns from lat and lon
reg = pd.DataFrame({"trip_latitude" : lat,
                    "trip_longitude" : lon})

reg["trip_region_id"] = range(len(trip_regions))



# Function to calculate distance
# Source: https://janakiev.com/blog/gps-points-distance-python/
def haversine(coord1, coord2):
    R = 6372800  # Earth radius in meters
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    phi1, phi2 = math.radians(lat1), math.radians(lat2) 
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)
    
    a = math.sin(dphi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    
    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))

# Find closes region to each segment centroid

distance_dic = {}
for trip_r in range(len(reg)):
    t_r_id = reg["trip_region_id"][trip_r]
    distances = []
    for base_r in range(len(base_regions)):
        distances.append(haversine((base_regions["west"][base_r], base_regions["north"][base_r]),
                                   (reg["trip_longitude"][trip_r], reg["trip_latitude"][trip_r])))
    distance_dic[t_r_id] = distances

region_dic = {}
for k,v in distance_dic.items():
    trip_region = base_regions["region_id"][v.index(min(v))]
    region_dic[k] = trip_region

trip_region_id = list(region_dic.keys())
base_region_id = list(region_dic.values())
centroids = list(trip_regions["location"])

trips_regions = pd.DataFrame({"trip_region_id" : trip_region_id,
                                "base_region_id" : base_region_id,
                                "trip_centroids" : centroids})
    
missing_region = pd.DataFrame({"trip_region_id" : [max(trips_regions["trip_region_id"])+1],
                               "base_region_id" : [max(trips_regions["base_region_id"])+1],
                               "trip_centroids" : ["Missing"]})

trips_regions = trips_regions.append(missing_region, ignore_index = True)

# Export

trips_regions.to_csv(r"~/trip_region_lookup.csv", index = False, header = False)