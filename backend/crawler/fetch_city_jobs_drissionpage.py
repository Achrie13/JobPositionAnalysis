from DrissionPage import ChromiumOptions

# 初次使用的时候设置浏览器路径，要使用管理员权限，可以直接去cmd中用管理员身份运行py文件
# pip install drissionpage
# path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
# ChromiumOptions().set_browser_path(path).save()

from DrissionPage import ChromiumPage
import csv
import json
import os
import time


def getCityJobs(MaxPage=20, CityLisst=["北京"]):
    jobs_data = []
    for city in CityLisst:
        CityCode = getCityCode(city)
        if CityCode == 0:
            print("城市不存在")
            return

        dp = ChromiumPage()
        dp.listen.start("search/joblist.json")
        dp.get(
            f"https://www.zhipin.com/web/geek/jobs?city={CityCode}&query=Python")

        for i in range(1, MaxPage + 1):
            print(f"{city},第 {i} 页")
            try:
                r = dp.listen.wait(timeout=5)
                json_data = r.response.body
                job_list = json_data["zpData"]["jobList"]
            except Exception as e:
                print(f"请求超时: {e}")
                break

            for job in job_list:
                jobs_data.append(
                    {
                        "职位": job.get("jobName"),
                        "学历": job.get("jobDegree"),
                        "经验": job.get("jobExperience"),
                        "技能列表": job.get("skills", []),
                        "薪资": job.get("salaryDesc"),
                        "公司": job.get("brandName"),
                        "公司人数": job.get("brandScaleName"),
                        "城市": job.get("cityName"),
                        "区域": job.get("areaDistrict"),
                    }
                )

            tab = dp.ele("css:.job-list-container")
            dp.scroll.to_bottom()
            tab.scroll.to_bottom()
            time.sleep(1)

        # 保存路径
    current_dir = os.getcwd()
    base_path = os.path.join(
        current_dir, "JobPositionAnalysis", "backend", "data")

    os.makedirs(os.path.join(base_path, "processed"), exist_ok=True)
    os.makedirs(os.path.join(base_path, "raw"), exist_ok=True)

    csv_path = os.path.join(base_path, "processed", f"1.csv")
    json_path = os.path.join(base_path, "raw", f"1.json")

    # 保存到JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(jobs_data, f, ensure_ascii=False, indent=4)
    # 保存到CSV
    with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=jobs_data[0].keys())
        writer.writeheader()
        writer.writerows(jobs_data)


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
    # 江苏省市
    cities = [
        '南京', '无锡', '徐州', '常州', '苏州',
        '南通', '连云港', '淮安', '盐城', '扬州',
        '镇江', '泰州', '宿迁',
    ]
    getCityJobs(MaxPage=20, CityLisst=cities)
