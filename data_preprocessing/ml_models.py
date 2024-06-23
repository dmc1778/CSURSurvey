import pandas as pd
import csv

data = pd.read_csv('data/full_data.csv', sep=',')

for row, item in data.iterrows():
    if item['broad_category'] == 'ML':
        model_split = item['RQ3'].split(',')
        for ml_model in model_split:
            with open(f"ml_models.csv", 'a', encoding="utf-8", newline='\n') as file_writer:
                write = csv.writer(file_writer)
                write.writerow([ml_model])