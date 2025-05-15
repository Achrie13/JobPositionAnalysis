import pandas as pd
import os
import csv

# 等级名称映射
salary_class_names = {
    1: "初级",
    2: "普通",
    3: "中级",
    4: "高级",
    5: "专家",
    6: "高管"
}


def SalaryClass(annual_salary):
    if annual_salary < 50:
        return 1
    elif annual_salary < 100:
        return 2
    elif annual_salary < 200:
        return 3
    elif annual_salary < 400:
        return 4
    elif annual_salary < 800:
        return 5
    else:
        return 6


def SalaryCount():
    current_dir = os.getcwd()
    file_path = os.path.join(
        current_dir, "JobPositionAnalysis", "backend", "data", "processed", "江苏各城市数据(已清洗).csv")

    salary_counter = {i: 0 for i in range(1, 7)}

    df = pd.read_csv(file_path, encoding="utf-8")
    df["年薪"] = pd.to_numeric(df["年薪"], errors="coerce")

    for _, row in df.iterrows():
        salary = row["年薪"]
        if pd.notna(salary):
            level = SalaryClass(salary)
            salary_counter[level] += 1

    # 组织成适合写入的列表
    result = [{"等级": salary_class_names[k], "数量": v}
              for k, v in salary_counter.items()]

    out_path = os.path.join(
        current_dir, "JobPositionAnalysis", "backend", "data", "processed", "SalaryCount.csv")

    with open(out_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["等级", "数量"])
        writer.writeheader()
        writer.writerows(result)


if __name__ == "__main__":
    SalaryCount()
