import requests
import csv
import json
import os
import random


# 设置多个请求头 User-Agent
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
]

# 设置多个 cookie 值
cookies = [
    "wt2=DhU7fexgE_NSt__-40rhbND2DlloaSh84KuVE1mpkNJNs4gI17daa5fP_bTzioEX-h050UEVqubPEJZ7jkEDLJg~~; wbg=0; zp_at=HvjYUFUp7VJ3ZpRQvXWMkf7Pet5Y4lEHZ4kUStEhXWo~; ab_guid=24b36fb6-b391-4790-83af-fae78144a48c; lastCity=101191100; __zp_seo_uuid__=bb55a848-4bc5-43d7-9d0d-1b284d6cfcb6; __l=r=https%3A%2F%2Fcn.bing.com%2F&l=%2F&s=1; __g=-; bst=V2R98mGO302FhjVtRuyxUZKCiy7DrTwio~|R98mGO302FhjVtRuyxUZKCiy7DrVxSs~; __c=1747138705; __a=34602280.1747114679.1747127140.1747138705.26.3.2.26; __zp_stoken__=5bc4fw42FDjMKQEToSYGQRGFkVYHR2cUllwr9OY8KpZ8K0WcKfw4JTacKmW8K1w4bCumfCqnLCs8OGwqF4wpZPwrpPwpvCqsKOTcOqTsKMwrbCmsScw6tzwpvEjsKwwrnCojw4Cg0QCQ0LEA0MEH98FhMXCxANDBAOCQwNCTk1w7zCkzA7P0E9K1VSUw9XZmhMZEsQXktQOToNFWcYOjM8PTk%2Bw4N8wrrDocOIecK%2Fw6XDg37CvsOkPUE%2BOcK%2FDi5Cw4DChgl2Ck8QfA3CvsKKEMONYRkRw5jCu8KGHz8%2Bwr3EukdAGkdAO0I9PEE7QCo7wrnCicOJZBoRw5LCv1osORtIPTxHOUA9PEU7Qik8SDIqPT0pRxQVCw4VL0LCucKrwr7DoT08",
]


def get_random_headers():
    return {
        "User-Agent": random.choice(user_agents),
        "Referer": "https://www.zhipin.com/web/geek/job",
        "Cookie": random.choice(cookies),
    }


def fetch_job_data(CityName="北京", PageSize="100", page=1):
    CityCode = getCityCode(CityName)  # 假设你已有此函数
    if CityCode == 0:
        print("城市不存在")
        return

    url = (
        "https://www.zhipin.com/wapi/zpgeek/search/joblist.json?"
        f"page={page}&pageSize={PageSize}&query=Python&city={CityCode}&scene=1&_=1747138817419"
    )

    headers = get_random_headers()

    print(f"请求 URL：{url}")
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"请求失败，状态码：{response.status_code}")
        return []

    data = response.json()
    print(json.dumps(data, ensure_ascii=False, indent=2))
    job_list = data["zpData"]["jobList"]
    print(json.dumps(job_list, ensure_ascii=False, indent=2))

    jobs_data = []
    for job in job_list:
        jobs_data.append(
            {
                "职位名称": job.get("jobName"),
                "公司名称": job.get("brandName"),
                "薪资": job.get("salaryDesc"),
                "工作经验": job.get("jobExperience"),
                "学历": job.get("jobDegree"),
                "城市": job.get("cityName"),
                "区域": job.get("areaDistrict"),
                "商圈": job.get("businessDistrict"),
                "技能": ",".join(job.get("skills", [])),
                "福利": ",".join(job.get("welfareList", [])),
                "公司行业": job.get("brandIndustry"),
                "公司规模": job.get("brandScaleName"),
            }
        )

    # 文件保存路径
    current_dir = os.getcwd()
    base_path = os.path.join(current_dir, "JobPositionAnalysis", "backend", "data")
    os.makedirs(os.path.join(base_path, "processed"), exist_ok=True)
    os.makedirs(os.path.join(base_path, "raw"), exist_ok=True)

    csv_path = os.path.join(base_path, "processed", f"{CityName}.csv")
    json_path = os.path.join(base_path, "raw", f"{CityName}.json")

    # 写入 CSV
    with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=jobs_data[0].keys())
        writer.writeheader()
        writer.writerows(jobs_data)

    # 写入 JSON
    with open(json_path, mode="w", encoding="utf-8") as file:
        json.dump(jobs_data, file, ensure_ascii=False, indent=2)

    print(f"已保存 {len(jobs_data)} 条数据到：\n - {csv_path}\n - {json_path}")


def getCityCode(CityName="北京"):
    current_dir = os.getcwd()
    file_path = os.path.join(
        current_dir, "JobPositionAnalysis", "backend", "data", "raw", "city_codes.json"
    )

    # 读取json
    city_data = []
    with open(file_path, mode="r", encoding="utf-8") as file:
        city_data = json.load(file)

    for city in city_data:
        if city.get("city_name") == CityName:
            CityCode = city.get("city_code")
            break
    else:
        return 0
    return CityCode


if __name__ == "__main__":
    # CityName = input("输出抓取的城市名称：")
    fetch_job_data()
