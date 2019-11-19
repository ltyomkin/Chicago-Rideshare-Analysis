#!/usr/bin/env python
# coding: utf-8

import pandas as pd

traffic_df = pd.read_csv("Chicago_Traffic_2011-2018.csv", nrows = 2000)

traffic_df.head()

traffic_df.dtypes

# Change names
traffic_df.columns = ["timestamp_id",
                      "segment_id",
                      "bus_count",
                      "gps_pings",
                      "speed"]

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

traffic_df["comments"] = ""