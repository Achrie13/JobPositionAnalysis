import json
import re

def normalize_salary(salary_str):
    if not salary_str:
        return ''
    # 去除“·13薪”等后缀
    salary_str = re.sub(r'·\d+薪', '', salary_str)
    # 统一“K”大写
    salary_str = salary_str.replace('k', 'K')
    # 匹配区间（K、元/天、元/月、元/时）
    match = re.match(r'(\d+)-(\d+)(K|元/天|元/月|元/时)', salary_str)
    if match:
        low, high, unit = match.groups()
        if unit == '元/月':
            low_k = str(int(int(low) / 1000))
            high_k = str(int(int(high) / 1000))
            return f"{low_k}-{high_k}K"
        elif unit == '元/天':
            # 按21.75天/月换算
            low_k = str(int(int(int(low) * 21.75) / 1000))
            high_k = str(int(int(int(high) * 21.75) / 1000))
            return f"{low_k}-{high_k}K"
        elif unit == '元/时':
            # 按8小时/天，21.75天/月换算
            low_k = str(int(int(int(low) * 8 * 21.75) / 1000))
            high_k = str(int(int(int(high) * 8 * 21.75) / 1000))
            return f"{low_k}-{high_k}K"
        return f"{low}-{high}{unit}"
    # 匹配单一数值
    match = re.match(r'(\d+)(K|元/天|元/月|元/时)', salary_str)
    if match:
        num, unit = match.groups()
        if unit == '元/月':
            num_k = str(int(int(num) / 1000))
            return f"{num_k}-{num_k}K"
        elif unit == '元/天':
            num_k = str(int(int(int(num) * 21.75) / 1000))
            return f"{num_k}-{num_k}K"
        elif unit == '元/时':
            num_k = str(int(int(int(num) * 8 * 21.75) / 1000))
            return f"{num_k}-{num_k}K"
        return f"{num}-{num}{unit}"
    # 其他情况原样返回
    return salary_str

with open(r'C:/Users/bushinanjiejie/Desktop/youngboyneverbrokeagain/JobPositionAnalysis/backend/data/raw/city_jobs.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for job in data:
    if '薪资' in job:
        job['薪资'] = normalize_salary(job['薪资'])

with open(r'C:/Users/bushinanjiejie/Desktop/youngboyneverbrokeagain/JobPositionAnalysis/backend/data/raw/city_jobs.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('薪资字段已统一，结果保存在 city_jobs.json')