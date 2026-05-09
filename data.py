import requests
import pandas as pd
import time

API_KEY = "f2b0ff81d76dbd065b27c340688ca3582b77110008165b62c8a38bfee8757701"
headers = {
    "accept": "application/json",
    "X-API-Key": API_KEY
}

cities = ["Delhi", "Mumbai", "Pune", "Bangalore", "Hyderabad"]
parameters = ["pm25", "pm10"]
records_per_request = 100  # limit max is 100
date_from = "2025-06-01"
date_to = "2025-06-30"

all_data = []

for city in cities:
    print(f"🔄 Fetching data for: {city}")
    for param in parameters:
        page = 1
        while True:
            url = (
                f"https://api.openaq.org/v2/measurements?"
                f"country=IN&city={city}&parameter={param}"
                f"&date_from={date_from}&date_to={date_to}"
                f"&limit={records_per_request}&page={page}&sort=desc&order_by=datetime"
            )
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                results = response.json().get("results", [])
                if not results:
                    break  # no more pages
                df = pd.DataFrame(results)
                df['city'] = city
                df['parameter'] = param
                all_data.append(df)
                page += 1
                time.sleep(0.5)
            except Exception as e:
                print(f"⚠️ Error for {city}-{param}: {e}")
                break

# Save final result
if all_data:
    df_all = pd.concat(all_data, ignore_index=True)
    df_all.to_csv("openaq_india_june2025.csv", index=False)
    print("✅ Data saved to openaq_india_june2025.csv")
else:
    print("❌ No data downloaded.")
