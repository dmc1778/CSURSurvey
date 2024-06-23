import pandas as pd
import csv, json

def get_mapping():
    data = pd.read_csv('data/full_data.csv', sep=',')
    big_list = []
    for row, item in data.iterrows():
        model_split = item['rq1_sub_type'].split(',')
        cleaned_strings = [s.replace('\u200c', '') for s in model_split]
        for ml_model in cleaned_strings:
            data = [item['BibliographyID'], ml_model.strip()]
            big_list.append(data)

    model_dict = {}

    _name = []

    for item in big_list:
        author = item[0]
        model = item[1]
        
        _name.append(model)
        
        if model not in model_dict:
            model_dict[model] = []
        model_dict[model].append(author)

    # for k, v in model_dict.items():
    #     print(f"The total number of items for {k} is {len(v)}")

    with open('code_types.json', 'w') as json_file:
        json.dump(model_dict, json_file, indent=4)

    for b in set(_name):
        with open(f"output/code_types.csv", 'a', encoding="utf-8", newline='\n') as file_writer:
            write = csv.writer(file_writer)
            write.writerow([b])

def count_():
    with open('code_types.json') as f:
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