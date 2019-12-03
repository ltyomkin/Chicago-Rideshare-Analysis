python date_table.py &&
python ~/Chicago-Rideshare-Analysis/Cleaning_Code/regions_cleanup.py &&
python ~/Chicago-Rideshare-Analysis/Cleaning_Code/regions_traffic_cleanup.py &&
python ~/Chicago-Rideshare-Analysis/Cleaning_Code/taxi_trips_cleanup.py &&
python ~/Chicago-Rideshare-Analysis/Cleaning_Code/rideshare_trips_cleanup.py &&
python ~/Chicago-Rideshare-Analysis/Cleaning_Code/trips_merge.py &&
python ~/Chicago-Rideshare-Analysis/Cleaning_Code/trips_region_lookup.py &&
gsutil cp ~/clean_full_traffic_data.csv gs://rideshare-csvs/headerless_processed_data &&
gsutil cp ~/dim_date.csv gs://rideshare-csvs/headerless_processed_data &&
gsutil cp ~/headerless_clean_regions.csv gs://rideshare-csvs/headerless_processed_data &&
gsutil cp ~/trip_region_lookup.csv gs://rideshare-csvs/headerless_processed_data &&
gsutil cp ~/final_trips.csv gs://rideshare-csvs/headerless_processed_data