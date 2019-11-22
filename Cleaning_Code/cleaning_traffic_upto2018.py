
import pandas as pd

traffic_df = pd.read_csv("Chicago_Traffic_2011-2018.csv")

# Change column names

traffic_df.columns = ["timestamp_id",
                      "segment_id",
                      "bus_count",
                      "gps_pings",
                      "speed"]

# Change datetime

traffic_df.timestamp_id = pd.to_datetime(traffic_df.timestamp_id)

# Filter out dates
min_date = '2014-01-01'
max_date = '2019-10-31'
traffic_df = traffic_df[(traffic_df['timestamp_id'] >= min_date) & (traffic_df['timestamp_id'] <= max_date)]

# Create multi index

dates = pd.period_range(min_date,
                        max_date, freq = "H")

segments = traffic_df['segment_id'].unique()

idx = pd.MultiIndex.from_product((dates, segments),
                                 names=['timestamp_id', 'segment_id'])

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

# Add speed category
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
filled_df = filled_df[["segment_id","timestamp_id","speed","speed_category","bus_count","gps_pings"]]

# Export cleaned csv
filled_df.to_csv(r"Cleaned_Chicago_Traffic_2011-2018.csv")