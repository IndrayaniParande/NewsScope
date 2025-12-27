import pandas as pd
import glob
import os

def count_rows(folder_path):
    print(f"scanning folder:{folder_path}")

    csv_file = glob.glob(os.path.join(folder_path, "*.csv"))
    if not csv_file:


        print("no csv file found")
        return
    print(f"found {len(csv_file)} csv files.")
    all_data = [pd.read_csv(file) for file in csv_file]
    combined = pd.concat(all_data, ignore_index=True)
    total_rows = len(combined)
    print(f"Total rows: {total_rows}")

count_rows("newsapi_daily_data")

folder_path = "C:/Users/ASUS/Desktop/News_Analyzer/app/collector"
all_dataframe =[]

for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        filepath = os.path.join(folder_path, filename)
        data = pd.read_csv(filepath)
        all_dataframe.append(data)

combined_data = pd.concat(all_dataframe, ignore_index=True)

combined_data.to_csv("final_data1.csv", index=False)
print(f"combined {len(all_dataframe)} csv files saved into 'final_data.csv' with {len(combined_data)} rows.")








