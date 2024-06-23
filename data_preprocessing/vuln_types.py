import pandas as pd
import csv, json

data = pd.read_csv('data/full_data.csv', sep=',', encoding='utf-8')

big_list = []
for row, item in data.iterrows():
    model_split = item['Vulnerability types (RQ4)'].split(',')
    cleaned_strings = [s.replace('\u200c', '') for s in model_split]
    for ml_model in cleaned_strings:
        data = [item['BibliographyID'], ml_model.strip()]
        big_list.append(data)

model_dict = {}

for item in big_list:
    author = item[0]
    model = item[1]
    if model not in model_dict:
        model_dict[model] = []
    model_dict[model].append(author)

with open('cwe_dict.json', 'w') as json_file:
    json.dump(model_dict, json_file, indent=4)
        # with open(f"dl_models.csv", 'a', encoding="utf-8", newline='\n') as file_writer:
        #     write = csv.writer(file_writer)
        #     write.writerow([ml_model])