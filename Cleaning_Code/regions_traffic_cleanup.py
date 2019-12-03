import pandas as pd

traffic_from2018_df = pd.read_csv("~/region_traffic_from_2018.csv")

# Change names
traffic_from2018_df.columns = ["timestamp_id",
                      "region_id",
                      "speed",
                      "region",
                      "bus_count",
                      "gps_pings",
                      "hour",
                      "day_of_week",
                      "month",
                      "description",
                      "record_id",
                      "west",
                      "east",
                      "south",
                      "north",
                      "nw_location",
                      "se_location"]


# Remove columns
traffic_from2018_df = traffic_from2018_df.drop(["hour",
                                                "day_of_week",
                                                "month",
                                                "description",
                                                "record_id",
                                                "west",
                                                "east",
                                                "south",
                                                "north",
                                                "nw_location",
                                                "se_location"],
                                               axis = 1)

# Change timestamp to datetime
traffic_from2018_df.timestamp_id = pd.to_datetime(traffic_from2018_df.timestamp_id)

# Filter out dates
min_date = '2018-02-28'
max_date = '2018-10-31'
traffic_from2018_df = traffic_from2018_df[(traffic_from2018_df['timestamp_id'] >= min_date) &
                        (traffic_from2018_df['timestamp_id'] <= max_date)]

# Aggregate timestamp by hour
traffic_from2018_df = traffic_from2018_df.set_index('timestamp_id')

traffic_from2018_df = traffic_from2018_df.groupby(["region_id"]).resample("H").agg({
                                                    'bus_count' : 'sum',
                                                    'gps_pings' : 'sum',
                                                    'speed' : 'mean'}).ffill()

traffic_from2018_df = traffic_from2018_df.reset_index()

# Fill missing hours
filled_df = (traffic_from2018_df.set_index('timestamp_id')
             .groupby('region_id')
             .apply(lambda d: d.reindex(pd.date_range(min(traffic_from2018_df.timestamp_id),
                                                      max(traffic_from2018_df.timestamp_id),
                                                      freq='H')))
             .drop('region_id', axis=1)
             .reset_index('region_id')
             .ffill())

fill_values = {"bus_count" : 0, "gps_pings" : 0, "speed" : -1}

filled_df = filled_df.fillna(value = fill_values)

# Reorder columns
filled_df["timestamp_id"] = filled_df.index
filled_df = filled_df.reset_index()

traffic_from2018 = filled_df[["region_id",
                              "timestamp_id",
                              "speed",
                              "bus_count",
                              "gps_pings"]]

# Load upto2018

traffic_upto2018_df = pd.read_csv("~/region_traffic_upto_2018.csv")

# Change column names

traffic_upto2018_df.columns = ["timestamp_id",
                               "region_id",
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

traffic_upto2018_df = traffic_upto2018_df.groupby(["region_id"]).resample("H").agg({
                                                                'bus_count' : 'sum',
                                                                'gps_pings' : 'sum',
                                                                'speed' : 'mean'}).ffill()

traffic_upto2018_df = traffic_upto2018_df.reset_index()

# Fill missing hours

filled_df = (traffic_upto2018_df.set_index('timestamp_id')
             .groupby('region_id')
             .apply(lambda d: d.reindex(pd.date_range(min(traffic_upto2018_df.timestamp_id),
                                                      max(traffic_upto2018_df.timestamp_id),
                                                      freq='H')))
             .drop('region_id', axis=1)
             .reset_index('region_id')
             .ffill())
             
traffic_upto2018 = filled_df.fillna(value = fill_values)

# Reorder columns
traffic_upto2018["timestamp_id"] = filled_df.index
traffic_upto2018 = traffic_upto2018.reset_index()
traffic_upto2018 = traffic_upto2018[["region_id","timestamp_id","speed","bus_count","gps_pings"]]

# Join with upto2018

traffic_full = pd.concat([traffic_upto2018,traffic_from2018], ignore_index = True)
    
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

# Reorder
traffic_full = traffic_full[["region_id","timestamp_id","speed","speed_category","bus_count","gps_pings"]]

# Export final traffic data

traffic_full.to_csv(r"~/clean_full_traffic_data.csv", header = False)