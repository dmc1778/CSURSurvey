import pandas as pd
import csv, json


def get_mapping():
    data = pd.read_csv('data/full_data.csv', sep=',')
    data = data[((data['broad_category'] == 'ML') | (data['broad_category'] == 'Others') | (data['broad_category'] == 'Hybrid'))]

    big_list = []
    for row, item in data.iterrows():
        model_split = item['RQ3'].split(',')
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

    for k, v in model_dict.items():
        print(f"The total number of items for {k} is {len(v)}")

    with open('ML_model_dict.json', 'w') as json_file:
        json.dump(model_dict, json_file, indent=4)
            # with open(f"dl_models.csv", 'a', encoding="utf-8", newline='\n') as file_writer:
            #     write = csv.writer(file_writer)
            #     write.writerow([ml_model])


def count_():
    with open('ML_model_dict.json') as f:
        d = json.load(f)
    total = 0
    x = []
    y = []
    for k, v in d.items():
        # print(f"Number of records per category {k} is {len(v)}")
        if k != 'N.A':
            print(f"Number of records per category {k} is {len(v)}")
            for item in v:
                x.append(item)
        else:
            for item in v:
                y.append(item)

    # print(f'Total number of records: {len(x)}')
    print(f'Total number of unique records: {len(set(x))}')
    print(f'Total number of unique N.A records: {len(set(y))}')


if __name__ == '__main__':
    count_()