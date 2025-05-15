import json
import re

def normalize_salary(salary_str):
    if not salary_str:
        return ''
    # 去除“·13薪”等后缀
    salary_str = re.sub(r'·\d+薪', '', salary_str)
    # 统一“K”大写
    salary_str = salary_str.replace('k', 'K')
    # 匹配区间
    match = re.match(r'(\d+)-(\d+)(K|元/天)', salary_str)
    if match:
        low, high, unit = match.groups()
        return f"{low}-{high}{unit}"
    # 匹配单一数值
    match = re.match(r'(\d+)(K|元/天)', salary_str)
    if match:
        num, unit = match.groups()
        return f"{num}-{num}{unit}"
    # 其他情况原样返回
    return salary_str

with open(r'C:/Users/bushinanjiejie/Desktop/youngboyneverbrokeagain/JobPositionAnalysis/backend/data/raw/city_jobs_XvRui.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for job in data:
    salary = job.get('薪资', '')
    job['薪资'] = normalize_salary(salary)

with open(r'C:/Users/bushinanjiejie/Desktop/youngboyneverbrokeagain/JobPositionAnalysis/backend/data/raw/city_jobs_XvRui.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('薪资字段已统一，结果保存在 city_jobs_XvRui_salary_normalized.json')