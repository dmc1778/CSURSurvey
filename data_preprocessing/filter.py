import pandas as pd

list_a = pd.read_csv('data/final_papers.csv', sep=',')
list_b = pd.read_csv('data/high_rank.csv', sep=',')

A = []

# Filter the DataFrame
difference_set = list(set(list(list_a.iloc[:,0])) - set(list(list_b.iloc[:, 0])))

# Print the filtered DataFrame
for item in difference_set:
    print(item)