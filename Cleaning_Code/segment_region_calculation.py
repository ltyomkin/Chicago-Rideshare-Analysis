
import pandas as pd

segments = pd.read_csv("clean_segment_data.csv")

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

starts = pd.data.frame("location" = regions.pickup_centroid_location.unique())
ends = pd.data.frame("location" = regions.dropoff_centroid_location.unique())

regions = pd.data.frame("location" = pd.concat(starts,ends, axis = 1).unique())

regions["region"] = range(len(regions))


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
    for region in range(len(regions)):
        distances[region] = haversine(regions["location"][region],
                                     (segments["centroid_lon"], segments["centroid_lat"]))
    distance_dic[s_id] = distances

region_dic = {}
for k,v in distance_dic.items():
    seg_region = regions["region"][v.index(min(v))]
    region_dic[k] = seg_region

segment_regions = pd.data.frame("segment_id" = region_dic.keys(),
                                "region" = region_dic.values())

# Export

segment_regions.to_csv(r"segment_region_lookup.csv")