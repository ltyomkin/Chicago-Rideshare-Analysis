import pandas as pd

regions_df = pd.read_csv("~/regions.csv")

regions_df.rename(columns = {'REGIONID':'region_id'}, inplace = True) 

regions_df.columns = map(str.lower, regions_df.columns)

regions_df.columns = regions_df.columns.to_series().apply(lambda x: x.strip())

regions_df = regions_df.drop(["current_speed","last_updated","description", "east", "south"], axis = 1)

regions_df = regions_df[["region_id","region","west","north"]]

regions_df.to_csv(r"~/clean_regions.csv", index = False) # To be used in other calculations

regions_df.to_csv(r"~/headerless_clean_regions.csv", index = False, header = False) # Actual DW table for dim_base_region