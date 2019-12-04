gcloud sql import sql trips_instance gs://rideshare_bucket/ddl.sql &&
gcloud sql import sql trips_instance gs://rideshare_bucket/cleaned_region.csv -d dim_base_region &&
gcloud sql import sql trips_instance gs://rideshare_bucket/cleaned_trip_region.csv -d dim_trip_region &&
gcloud sql import sql trips_instance gs://rideshare_bucket/dim_date_headerless.csv -d dim_time &&
gcloud sql import sql trips_instance gs://rideshare_bucket/cleaned_full_traffic_data.csv -d dim_traffic &&
gcloud sql import sql trips_instance gs://rideshare_bucket/limited_trips.csv -d dim_trips &&