
import pandas as pd

traffic_df = pd.read_csv("Chicago_Traffic_2018-2019.csv")

# traffic_df.head()

# traffic_df.dtypes

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
                      "comments",
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

remove_columns = ["street",
                  "direction",
                  "from_street",
                  "to_street",
                  "length",
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
traffic_df.drop(remove_columns, axis = 1)

# Change datetime
traffic_df.timestamp_id = pd.to_datetime(traffic_df.timestamp_id)

# Add speed category and comments columns
def speed_condition(c):
  if c['speed'] < 10:
    return 'slow'
  elif 10 <= c['speed'] < 20:
    return 'medium'
  elif c['speed'] >= 20:
    return 'regular'
  else:
    return 'undefined'

traffic_df["speed_category"] = traffic_df.apply(speed_condition, axis = 1)

# Reorder columns
traffic_from2018 = traffic_df[["segment_id","timestamp_id","speed","speed_category","comments","bus_count","gps_pings"]]


# Join with upto2018
traffic_upto2018 = pd.read.csv("Cleaned_Chicago_Traffic_2011-2018.csv")

traffic_full = pd.concat([traffic_upto2018,traffic_from2018])

# create traffic unique id
traffic_full["traffic_id"] = traffic_full.timestamp_id.strftime('%Y-%m-%d %H:%M:%S') + str(traffic_full.segment_id)

# Export final traffic data
traffic_full.to_csv(r"full_traffic_data.csv")
