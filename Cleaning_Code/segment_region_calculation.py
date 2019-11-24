
import pandas as pd

segments = pd.read_csv("cleaned_segments.csv")

segments = segments[["segment_id",
                     "start_latitude",
                     "start_longitude",
                     "end_latitude",
                     "end_longitude"]]

regions = pd.read_csv("cleaned_trips")

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



segment_regions.to_csv(r"segment_region_lookup.csv")