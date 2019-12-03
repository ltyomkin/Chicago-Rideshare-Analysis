# Chicago Rideshare Analysis

Repository for Data Engineering Platforms final project at the University of Chicago. Created by @ltyomkin, @luisflosi, @minhahoang, and @sarahdudek 

This project is a look at the impact of rideshare transportation on traffic in the city of Chicago. Our goal is to compare pre-rideshare taxi trip data with current rideshare data. We will also cross-reference this data with CTA train and bus stops.

## Questions to Answer

- What is the impact of Transportation Network Providers on traffic congestion in Chicago?
- Are there trends in heavy congestion at certain times/days? How does that congestion behave before and after rideshare traffic was introduced to Chicago?
- How and where are rideshare companies such as Uber, Lyft and Via increasing and decreasing the flow of automobile traffic?
- What are the differences between taxi vs rideshare for trip duration, fares, and frequency?
- What kinds of events trigger an increase or decrease in congestion?


## Our Tech Stack

- Collection:
  * City of Chicago Transportation Datasets:
    + Network Providers Data
    + Number of registered drivers
    + Trip Data
  * Python
  * SQL

- Data Processing/Cleaning:
  * Python (JSON / Numpy / Pandas)
  * RStudio
  * MySQL
  * OpenRefine
  
- Warehousing:
  * Google Cloud Platform
  
- Analysis
  * Tableau

## Our Automation Process
1. Create MySQL instance in GCP (+50GB)
2. Import final_DDL.sql to setup DW structure
3. Import each csv in order:

	i. headerless_clean_regions.csv -> dim_base_region
 
	ii. trip_region_lookup.csv -> dim_trip_region
 
	iii. dim_date.csv -> dim_time
 
	iv. clean_full_traffic_data.csv -> dim_traffic
 
	v. final_trips.csv -> trips

  
## List of Data Sources

- [Transportation Network Providers - Vehicles](https://data.cityofchicago.org/Transportation/Transportation-Network-Providers-Vehicles/bc6b-sq4u "TNP Vehicles")
- [Transportation Network Providers - Drivers](https://data.cityofchicago.org/Transportation/Transportation-Network-Providers-Drivers/j6wf-834c "TNP Drivers")
- [Transportation Network Providers - Trips](https://data.cityofchicago.org/Transportation/Transportation-Network-Providers-Trips/m6dm-c72p "TNP Trips")
- [Taxi Trip Data](https://data.cityofchicago.org/Transportation/Taxi-Trips/wrvz-psew "Taxi Trips")
- [Historical Congestion](https://data.cityofchicago.org/Transportation/Chicago-Traffic-Tracker-Historical-Congestion-Esti/77hq-huss "Historical Congestion")
- [Traffic Tracker](https://data.cityofchicago.org/Transportation/Chicago-Traffic-Tracker-Historical-Congestion-Esti/sxs8-h27x "Traffic Tracker")
- [Congestion Estimates](https://data.cityofchicago.org/Transportation/Chicago-Traffic-Tracker-Congestion-Estimates-by-Se/n4j6-wkkf "Congestion Estimates")
- [CTA Bus Routes Ridership](https://data.cityofchicago.org/Transportation/CTA-Ridership-Bus-Routes-Monthly-Day-Type-Averages/bynn-gwxy "CTA Bus Routes")
- [CTA Bus Route Totals](https://data.cityofchicago.org/Transportation/CTA-Ridership-Bus-Routes-Daily-Totals-by-Route/jyb9-n7fm "CTA Bus Route Totals")
- [CTA List of L Stops](https://data.cityofchicago.org/Transportation/CTA-System-Information-List-of-L-Stops/8pix-ypme "List of L Stops")
- [CTA L Station Entries](https://data.cityofchicago.org/Transportation/CTA-Ridership-L-Station-Entries-Daily-Totals/5neh-572f "L Entries")

