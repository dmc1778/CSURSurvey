import pandas as pd
from collections import Counter
import os, re, json, tiktoken, backoff, csv
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    api_key=os.environ.get(".env")
)

# @backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def completions_with_backoff(prompt, model='gpt-3.5-turbo'):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt}
        ]
    )
    return response

def global_agent(paper_title):
    prompt_ = f"""
    You are given a title of a research paper and your task is to label whether the paper is a technical paper or not.
    These papers are collected based on a set of keywords that are related to software vulnerability detection using machine learning or deep learning.
    
    Your task is to label whether the paper titled @@{paper_title}@@ is a technical paper in software vulnerability detection using ML or DL techniques.

    A paper that is empirical study is not a valid paper.
    A paper that is survey study is not a valid paper.
    A paper that is in other vulnerability detection domains is not valid. Other domains such as android, web, hardware, and other engineering fields.
    A valid paper is a paper that is in software vulnerability detection and proposed a novel technique using deep learning or machine leanring.

    If the paper is valid, label it as 1 otherwise 0. If you can not label, just label I can't label.
    <answer start>
    """
    response = completions_with_backoff(prompt_)
    return response.choices[0].message.content

def main():
    use_base = True
    data_path = f"initial_records/IEEEPaperList.csv"
    data = pd.read_csv(data_path, sep=',', encoding='utf-8')
    for j, item in data.iterrows():
        print(f"Record {j}/{len(data)}")
        output = global_agent(item.iloc[0])
        out = [item.iloc[0], output]
        with open(f"output/title_filtering/IEEE_Title_filter.csv", 'a', encoding="utf-8", newline='\n') as file_writer:
            write = csv.writer(file_writer)
            write.writerow(out)
                        
if __name__ == '__main__':
    main()
