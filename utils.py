import re, csv, sys, subprocess, os, glob, shutil

REG_PTR = re.compile('Keywords:')
REG_PTR_ORION = re.compile('Keywords:')


def read_txt(_path):
    with open(_path, "r") as f:
        lines = [line.strip() for line in f.readlines()]
    return lines

def write_text(file_name, my_list):
    with open(file_name, "w") as file:
        for item in my_list:
            file.write(item + "\n")

def decompose_papers(splitted_lines):
    super_temp = []
    j = 0
    indices = []
    while j < len(splitted_lines):
        if not splitted_lines[j]:
            indices.append(j)
        if not splitted_lines[j]:
            indices.append(j)
        j += 1

    if len(indices) == 1:
        for i, item in enumerate(splitted_lines):
            if i != 0:
                super_temp.append(item)
        super_temp = [super_temp]
    else:
        i = 0
        j = 1
        while True:
            temp = [] 
            for row in range(indices[i], indices[j]):
                temp.append(splitted_lines[row])
            super_temp.append(temp)
            if j == len(indices)-1:
                temp = [] 
                for row in range(indices[j], len(splitted_lines)):
                    temp.append(splitted_lines[row])
                super_temp.append(temp)
                break
            i+= 1
            j+= 1

    return super_temp

def decompose():
    log_data_latest = read_txt('sample.txt')
    log_decomposed = decompose_papers(log_data_latest)

    for item in log_decomposed:
        if item:
            data = [item[2]]
            with open(f"scienceDirect.csv", "a", encoding="utf-8", newline='\n') as file:
                write = csv.writer(file)
                write.writerow(data)

def getUnique():
    data = read_txt('filteredTitles/all.txt')
    data = list(set(data))
    write_text('filteredTitles/all_filtered.txt', data)

if __name__ == '__main__':
    getUnique()