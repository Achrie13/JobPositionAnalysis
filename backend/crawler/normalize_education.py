import json
import re

# 1. 读取原始数据
with open('C:/Users/bushinanjiejie/Desktop/youngboyneverbrokeagain/JobPositionAnalysis/backend/data/raw/city_jobs.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 2. 定义学历关键词映射
def normalize_education(edu_str):
    if not edu_str or '不限' in edu_str:
        return '学历不限'
    if re.search(r'博士', edu_str):
        return '博士'
    if re.search(r'硕士|研究生', edu_str):
        return '硕士'
    if re.search(r'本科|学士', edu_str):
        return '本科'
    if re.search(r'大专|专科', edu_str):
        return '大专'
    return '其他'

# 3. 批量处理
for job in data:
    edu = job.get('学历要求', '')
    job['学历要求'] = normalize_education(edu)

# 4. 保存为新文件
with open('C:/Users/bushinanjiejie/Desktop/youngboyneverbrokeagain/JobPositionAnalysis/backend/data/raw/city_jobs.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('学历要求字段已统一，结果保存在 city_jobs.json')