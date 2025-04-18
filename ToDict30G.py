import pyarrow.parquet as pq
import pandas as pd
import json
import time


def country_and_email_dict_process(row_series):

    if row_series['country'] not in country_frequency_dict:
        country_frequency_dict[row_series['country']] = 1
    else :
        country_frequency_dict[row_series['country']] += 1

    global invaild_email_number
    email_domain = row_series['email'].split('@')
    flag = True
    if len(email_domain) != 2:
        invaild_email_number += 1
        flag = False
    else :
        domain_part = email_domain[1].split('.')[0]
        if domain_part == None:
            invaild_email_number += 1
            flag = False
        else:
            if domain_part not in email_frequency_dict:
                email_frequency_dict[domain_part] = 1
            else:
                email_frequency_dict[domain_part] += 1
    
    if flag is True:
        if row_series['country'] not in country_email_dict:
            country_email_dict[row_series['country']] = {}
        if domain_part not in country_email_dict[row_series['country']]:
            country_email_dict[row_series['country']][domain_part] = 1
        else:
            country_email_dict[row_series['country']][domain_part] += 1

def age_process(row_series):
    global invalid_age_number
    if int(row_series['age']) < 10 or int(row_series['age']) >= 100:
        invalid_age_number += 1

def purchase_process(row_series):
    fixed_str = row_series['purchase_history'].replace('""', '"')
    purchase_dict = json.loads(fixed_str)
    category = purchase_dict['categories']
    if category not in category_freq:
        category_freq[category] = 1
    else:
        category_freq[category] += len(purchase_dict['items'])

    for item in purchase_dict['items']:
        iid = item['id']
        if iid not in item_category_dict:
            item_category_dict[iid] = {}
        if category not in item_category_dict[iid]:
            item_category_dict[iid][category] = 1
        else:
            item_category_dict[iid][category] += 1

def income_process(row_series):
    country = row_series['country']
    income = row_series['income']
    if country not in country_income_dict:
        country_income_dict[country] = float(income)
    else:
        country_income_dict[country] += float(income)




if __name__ == "__main__" :

    country_frequency_dict = {}
    email_frequency_dict = {}
    invaild_email_number = 0
    invalid_age_number = 0
    all_number = 0
    country_email_dict = {}

    item_category_dict = {}
    category_freq = {}

    country_income_dict = {}

    time_list = []

    file_list = ["30G_data_new/part-00000.parquet",
                 "30G_data_new/part-00001.parquet",
                 "30G_data_new/part-00002.parquet",
                 "30G_data_new/part-00003.parquet",
                 "30G_data_new/part-00004.parquet",
                 "30G_data_new/part-00005.parquet",
                 "30G_data_new/part-00006.parquet",
                 "30G_data_new/part-00007.parquet",
                 "30G_data_new/part-00008.parquet",
                 "30G_data_new/part-00009.parquet",
                 "30G_data_new/part-00010.parquet",
                 "30G_data_new/part-00011.parquet",
                 "30G_data_new/part-00012.parquet",
                 "30G_data_new/part-00013.parquet",
                 "30G_data_new/part-00014.parquet",
                 "30G_data_new/part-00015.parquet",]
    
    for path in file_list:
        print(path)
        parquet_file = pq.ParquetFile(path)
        length = parquet_file.metadata.num_rows
        all_number += length

        # 按批次读取（默认批次大小=1024行）
        count = 0
        start_time = time.perf_counter()
        for batch in parquet_file.iter_batches(batch_size=1000):
            # 转换为 Pandas DataFrame
            df = batch.to_pandas()

            # 逐行处理
            for _, row in df.iterrows():
                count += 1
                country_and_email_dict_process(row.to_dict())
                age_process(row.to_dict())
                purchase_process(row.to_dict())
                income_process(row.to_dict())

            if count % 10000 == 0:
                print(str(count) + " Rows has been processed, total " + str(length))
        
        elapsed = time.perf_counter() - start_time

        # print(country_frequency_dict)
        # print(email_frequency_dict)
        # print(country_email_dict)
        # print(invaild_email_number)
        # print(invalid_age_number)
        # print(country_income_dict)
        # print(item_category_dict)
        # print(category_freq)

        print(f"耗时: {elapsed:.4f} 秒")
        time_list.append(elapsed)

    
    with open("30_country_frequency_dict.json", "w", encoding="utf-8") as f:
        json.dump(country_frequency_dict, f, indent=4)

    with open("30_email_frequency_dict.json", "w", encoding="utf-8") as f:
        json.dump(email_frequency_dict, f, indent=4)

    with open("30_country_email_dict.json", "w", encoding="utf-8") as f:
        json.dump(country_email_dict, f, indent=4)

    with open("30_country_income_dict.json", "w", encoding="utf-8") as f:
        json.dump(country_income_dict, f, indent=4)

    with open("30_item_category_dict.json", "w", encoding="utf-8") as f:
        json.dump(item_category_dict, f, indent=4)
    
    with open("30_category_freq.json", "w", encoding="utf-8") as f:
        json.dump(category_freq, f, indent=4)

    numbers = [all_number, invaild_email_number, invalid_age_number]
    print(all_number)
    print(invalid_age_number)
    print(invaild_email_number)
    print(time_list)

    with open("30_number.txt", "w", encoding="utf-8") as f:
        for num in numbers:
            f.write(f"{num}\n") 



    