import pandas as pd
import csv

data1 = pd.read_csv('data/ReprT1.csv', sep=',')
data_full = pd.read_csv('data/full_data.csv', sep=',')
dl_data = data_full.loc[data_full['broad_category'] == 'DL']

for idx, row in data1.iterrows():
    result = dl_data[dl_data['BibliographyID'] == row['References']]['model_family']
    if not result.empty:
        new_data = [row['References'], row['Year'], result.values[0]]
        with open(f"dltimeline.csv", 'a', encoding="utf-8", newline='\n') as file_writer:
            write = csv.writer(file_writer)
            write.writerow(new_data)