
import pandas as pd

traffic_from2018_df = pd.read_csv("traffic_from_2018.csv")

# Change names
traffic_from2018_df.columns = ["timestamp_id",
                      "segment_id",
                      "speed",
                      "street",
                      "direction",
                      "from_street",
                      "to_street",
                      "length",
                      "street_heading",
                      "bus_count",
                      "gps_pings",
                      "hour",
                      "day_of_week",
                      "month",
                      "record_id",
                      "start_latitude",
                      "start_longitude",
                      "end_latitude",
                      "end_longitude",
                      "start_location",
                      "end_location"]

# Remove columns
traffic_from2018_df.drop(["street",
                  "direction",
                  "from_street",
                  "to_street",
                  "length",
                  "hour",
                  "day_of_week",
                  "comments",
                  "month",
                  "record_id",
                  "start_latitude",
                  "start_longitude",
                  "end_latitude",
                  "end_longitude"],
                 axis = 1)

# Filter out dates
min_date = '2018-02-28'
max_date = '2018-10-31'
traffic_from2018_df = traffic_from2018_df[(traffic_from2018_df['timestamp_id'] >= min_date) &
                        (traffic_from2018_df['timestamp_id'] <= max_date)]

# Change timestamp to datetime
traffic_from2018_df.timestamp_id = pd.to_datetime(traffic_from2018_df.timestamp_id)

# Aggregate timestamp by hour
traffic_from2018_df = traffic_from2018_df.set_index('timestamp_id')

traffic_from2018_df = traffic_from2018_df.groupby(["segment_id"]).resample("H").agg({
                                                    'bus_count' : 'sum',
                                                    'gps_pings' : 'sum',
                                                    'speed' : 'mean'}).ffill()

traffic_from2018_df = traffic_from2018_df.reset_index()

# Fill missing hours
filled_df = (traffic_from2018_df.set_index('timestamp_id')
             .groupby('segment_id')
             .apply(lambda d: d.reindex(pd.date_range(min(traffic_from2018_df.timestamp_id),
                                                      max(traffic_from2018_df.timestamp_id),
                                                      freq='H')))
             .drop('segment_id', axis=1)
             .reset_index('segment_id')
             .groupby('segment_id')
             .ffill())

fill_values = {"bus_count" : 0, "gps_pings" : 0, "speed" : -1}

filled_df = filled_df.fillna(value = fill_values)

# Reorder columns
filled_df["timestamp_id"] = filled_df.index
filled_df = filled_df.reset_index()
traffic_from2018 = filled_df[["segment_id",
                              "timestamp_id",
                              "speed",
                              "bus_count",
                              "gps_pings"]]

# Load upto2018

traffic_upto2018_df = pd.read_csv("traffic_upto_2018.csv")

# Change column names

traffic_upto2018_df.columns = ["timestamp_id",
                               "segment_id",
                               "bus_count",
                               "gps_pings",
                               "speed"]

# Change datetime

traffic_upto2018_df.timestamp_id = pd.to_datetime(traffic_upto2018_df.timestamp_id)

# Filter out dates
min_date = '2014-01-01'
max_date = '2018-02-27'
traffic_upto2018_df = traffic_upto2018_df[(traffic_upto2018_df['timestamp_id'] >= min_date) &
                                          (traffic_upto2018_df['timestamp_id'] <= max_date)]

# Aggregate timestamp by hour

traffic_upto2018_df = traffic_upto2018_df.set_index('timestamp_id')

traffic_upto2018_df = traffic_upto2018_df.groupby(["segment_id"]).resample("H").agg({
                                                                'bus_count' : 'sum',
                                                                'gps_pings' : 'sum',
                                                                'speed' : 'mean'}).ffill()

traffic_upto2018_df = traffic_upto2018_df.reset_index()

# Fill missing hours

filled_df = (traffic_upto2018_df.set_index('timestamp_id')
             .groupby('segment_id')
             .apply(lambda d: d.reindex(pd.date_range(min(traffic_upto2018_df.timestamp_id),
                                                      max(traffic_upto2018_df.timestamp_id),
                                                      freq='H')))
             .drop('segment_id', axis=1)
             .reset_index('segment_id')
             .groupby('segment_id')
             .ffill())
             
traffic_upto2018 = filled_df.fillna(value = fill_values)

# Reorder columns
filled_df["timestamp_id"] = filled_df.index
filled_df = filled_df.reset_index()
filled_df = filled_df[["segment_id","timestamp_id","speed","bus_count","gps_pings"]]

# Join with upto2018

traffic_full = pd.concat([traffic_upto2018,traffic_from2018])

# Insert region information for segments

region_lookup_df = pd.read_csv("segment_region_lookup.csv")

traffic_full = pd.merge(traffic_full,
                      region_lookup_df["region"],
                      on = "segment_id",
                      how = "left")

traffic_full = traffic_full.drop("segment_id")

# Regroup by region

agg_dic = {"bus_count" : "sum", "gps_pings" : "sum", "speed" : "max"}

traffic_full = traffic_full.groupby(['region','timestamp_id']).agg(agg_dic).ffill()

# Add speed category
def speed_condition(c):
  if c['speed'] == -1:
      return 'unavailable'
  elif c['speed'] < 10:
    return 'slow'
  elif 10 <= c['speed'] < 20:
    return 'medium'
  elif c['speed'] >= 20:
    return 'regular'
  else:
    return 'undefined'

traffic_full["speed_category"] = traffic_full.apply(speed_condition, axis = 1)

# create traffic unique id
traffic_full["traffic_id"] = traffic_full.timestamp_id.strftime('%Y-%m-%d %H') + str(traffic_full.region)

# Export final traffic data

traffic_full.to_csv(r"clean_full_traffic_data.csv")

# Export to bucket

from google.cloud import storage

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))
    
upload_blob("rideshare-csvs", "full_traffic_data.csv", "rideshare_bucket")