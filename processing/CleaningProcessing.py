# 原数据需要处理和清洗，主要包括
# 统一格式，将公司规模的描述统一
import pandas as pd
import os
import re

# 公司规模映射字典
scale_dict = {
    "0-20人": "微型企业",
    "20-99人": "小型企业",
    "100-499人": "中型企业",
    "500-999人": "中大型企业",
    "1000-9999人": "大型企业",
    "10000人以上": "超大型企业",
}


def ProcessBrandScale():
    current_dir = os.getcwd()
    file_path = os.path.join(
        current_dir, "JobPositionAnalysis", "backend", "data", "processed", "江苏各城市数据.csv")
    df = pd.read_csv(file_path, encoding="utf-8")
    if "公司人数" in df.columns:
        df["公司人数"] = df["公司人数"].map(scale_dict)
        df.rename(columns={"公司人数": "公司规模"}, inplace=True)
        df.to_csv(file_path, index=False, encoding="utf-8")


def SalaryStandardization(salary_str):
    if isinstance(salary_str, str):
        match1 = re.match(r"(\d+)-(\d+)K·(\d+)薪", salary_str)
        if match1:
            low, high, months = match1.groups()
            low_y = float(low) * int(months)
            high_y = float(high) * int(months)
            return int((low_y + high_y) / 2)

        match2 = re.match(r"(\d+)-(\d+)K", salary_str)
        if match2:
            low, high = match2.groups()
            low_y = float(low) * 12
            high_y = float(high) * 12
            return int((low_y + high_y) / 2)

        match3 = re.match(r"(\d+)-(\d+)元/月", salary_str)
        if match3:
            low, high = match3.groups()
            low_y = float(low) * 12 / 1000
            high_y = float(high) * 12 / 1000
            return int((low_y + high_y) / 2)

    return salary_str


def ProcessSalary():
    current_dir = os.getcwd()
    file_path = os.path.join(
        current_dir, "JobPositionAnalysis", "backend", "data", "processed", "江苏各城市数据.csv")
    out_path = os.path.join(
        current_dir, "JobPositionAnalysis", "backend", "data", "processed", "江苏各城市数据(已清洗).csv")
    df = pd.read_csv(file_path, encoding="utf-8")

    df = df[~df['薪资'].str.contains('周|天|时|面议', na=False)]
    df["薪资"] = df["薪资"].apply(SalaryStandardization)
    df.rename(columns={"薪资": "年薪"}, inplace=True)
    df.to_csv(out_path, index=False, encoding="utf-8")


if __name__ == "__main__":
    ProcessBrandScale()
    ProcessSalary()
