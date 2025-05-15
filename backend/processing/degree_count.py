import json
import csv

# 读取数据
with open('JobPositionAnalysis/backend/data/raw/江苏各城市数据.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

degree_count = {}
for item in data:
    degree = item.get('学历', '未知')
    degree_count[degree] = degree_count.get(degree, 0) + 1

# 写入CSV
with open('JobPositionAnalysis/backend/data/processed/degree_count.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['学历名称', '数量'])
    for degree, count in degree_count.items():
        writer.writerow([degree, count])