import pandas as pd

segment_df = pd.read_csv("~/Downloads/Segment_Data.csv")

segment_df.rename(columns = {'SEGMENTID':'segment_id'}, inplace = True) 

segment_df.columns = map(str.lower, segment_df.columns)

segment_df.to_csv(r"clean_segment_data.csv")
