import pandas as pd
from sodapy import Socrata

client = Socrata("data.cityofchicago.org", None)

results = client.get("77hq-huss")
results_df = pd.DataFrame.from_records(results)
