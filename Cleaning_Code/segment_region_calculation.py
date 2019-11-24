import math
import pandas as pd

segments = pd.read_csv("clean_segment_data.csv")

segments.columns = segments.columns.to_series().apply(lambda x: x.strip())

segments = segments[["segment_id",
                     "start_latitude",
                     "start_longitude",
                     "end_latitude",
                     "end_longitude"]]

# Get mid point between end and start of segments
# Average can be used because locations are close enough together
segments["centroid_lat"] = segments["start_latitude"] + segments["end_latitude"] / 2
segments["centroid_lon"] = segments["start_longitude"] + segments["end_longitude"] / 2

regions = pd.read_csv("clean_taxi_trips.csv", nrows = 1000)

starts = pd.DataFrame({"location" : regions.pickup_centroid_location.unique()})
ends = pd.DataFrame({"location" : regions.dropoff_centroid_location.unique()})

r = pd.concat((starts,ends))

regions = pd.DataFrame({"location" : r["location"].unique()})

# Split point. Source: https://chrisalbon.com/python/data_wrangling/pandas_split_lat_and_long_into_variables/

# Create two lists for the loop results to be placed
lat = []
lon = []

# For each row in a varible,
for row in regions['location']:
        la = row.split(' ')[1].replace("(","")
        lo = row.split(' ')[2].replace(")","")
        lat.append(float(la))
        lon.append(float(lo))

# Create two new columns from lat and lon
reg = pd.DataFrame({"latitude" : lat,
                    "longitude" : lon})

reg["region"] = range(len(regions))


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
for segment in range(len(segments)):
    s_id = segments["segment_id"][segment]
    distances = []
    for region in range(len(reg)):
        distances[region] = haversine((reg["longitude"][region], reg["latitude"][region]),
                                     (segments["centroid_lon"], segments["centroid_lat"]))
    distance_dic[s_id] = distances

region_dic = {}
for k,v in distance_dic.items():
    seg_region = regions["region"][v.index(min(v))]
    region_dic[k] = seg_region

segment_regions = pd.DataFrame({"segment_id" : region_dic.keys(),
                                "region" : region_dic.values()})

# Export

segment_regions.to_csv(r"segment_region_lookup.csv")