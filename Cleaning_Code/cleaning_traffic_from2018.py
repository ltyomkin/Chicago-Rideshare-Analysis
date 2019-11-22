
import pandas as pd

traffic_df = pd.read_csv("Chicago_Traffic_2018-2019.csv")

# Change names
traffic_df.columns = ["timestamp_id",
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
traffic_df.drop(["street",
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
                  "end_longitude",
                  "start_location",
                  "end_location"],
                 axis = 1)

# Change datetime
traffic_df.timestamp_id = pd.to_datetime(traffic_df.timestamp_id)

# Filter out dates
min_date = '2018-02-28'
max_date = '2018-10-31'
traffic_df = traffic_df[(traffic_df['timestamp_id'] >= min_date) & (traffic_df['timestamp_id'] <= max_date)]

# Aggregate timestamp by hour
traffic_df = traffic_df.set_index('timestamp_id')

traffic_df = traffic_df.groupby(["segment_id"]).resample("H").agg({
        'bus_count' : 'sum',
        'gps_pings' : 'sum',
        'speed' : 'mean'}).ffill()

traffic_df = traffic_df.reset_index()

# Fill missing hours
filled_df = (traffic_df.set_index('timestamp_id')
             .groupby('segment_id')
             .apply(lambda d: d.reindex(pd.date_range(min(traffic_df.timestamp_id),
                                                      max(traffic_df.timestamp_id),
                                                      freq='H')))
             .drop('segment_id', axis=1)
             .reset_index('segment_id')
             .groupby('segment_id')
             .ffill())

fill_values = {"bus_count" : 0, "gps_pings" : 0, "speed" : -1}

filled_df = filled_df.fillna(value = fill_values)

# Add speed category and comments columns
def speed_condition(c):
  if c['speed'] == -1:
      return ''
  elif c['speed'] < 10:
    return 'slow'
  elif 10 <= c['speed'] < 20:
    return 'medium'
  elif c['speed'] >= 20:
    return 'regular'
  else:
    return 'undefined'

filled_df["speed_category"] = filled_df.apply(speed_condition, axis = 1)

# Reorder columns
filled_df["timestamp_id"] = filled_df.index
filled_df = filled_df.reset_index()
traffic_from2018 = filled_df[["segment_id","timestamp_id","speed","speed_category","bus_count","gps_pings"]]


# Join with upto2018
traffic_upto2018 = pd.read.csv("Cleaned_Chicago_Traffic_2011-2018.csv")

traffic_full = pd.concat([traffic_upto2018,traffic_from2018])

# create traffic unique id
traffic_full["traffic_id"] = traffic_full.timestamp_id.strftime('%Y-%m-%d %H') + str(traffic_full.segment_id)

# Export final traffic data

traffic_full.to_csv(r"full_traffic_data.csv")

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
    
upload_blob("rideshare-csvs", "full_traffic_data.csv", "rideshare_data")