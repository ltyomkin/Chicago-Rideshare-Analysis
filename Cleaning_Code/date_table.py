import pandas as pd

import datetime

drange = pd.date_range(start = '2013-01-01',end = '2019-11-01', freq = 'H')

date_data = pd.DataFrame({"timestamp_id" : drange})

date_data['time'] = [datetime.datetime.time(d) for d in date_data['timestamp_id']]

date_data['date'] = [datetime.datetime.date(d) for d in date_data['timestamp_id']] 

date_data['month'] = date_data['timestamp_id'].dt.month

date_data['year'] = date_data['timestamp_id'].dt.year

dayOfWeek={0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
date_data['weekday'] = date_data['timestamp_id'].dt.dayofweek.map(dayOfWeek)

date_data.to_csv("~/dim_date.csv",index = False)