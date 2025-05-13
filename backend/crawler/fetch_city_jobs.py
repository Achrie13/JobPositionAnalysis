import requests
import csv
import json
import os


import requests
import csv
import os


def fetch_job_data(CityName="北京", PageSize="10", page=1000):
    CityCode = getCityCode(CityName)
    if CityCode == 0:
        print("城市不存在")
        return
    url = (
        f"https://www.zhipin.com/wapi/zpgeek/search/joblist.json?"
        f"page={page}&pageSize={PageSize}&city={CityCode}&query={time}"
    )

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Referer": "https://www.zhipin.com/web/geek/job",
        "Cookie": "",
    }

    print(f"请求 URL：{url}")
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"请求失败，状态码：{response.status_code}")
        return []

    data = response.json()

    job_list = data["zpData"]["jobList"]

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
    os.makedirs(base_path, exist_ok=True)

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
    CityName = input("输出抓取的城市名称：")
    fetch_job_data()
