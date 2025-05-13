import requests
import csv
import json

url = "https://www.zhipin.com/wapi/zpCommon/data/city.json"


headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.zhipin.com/web/geek/job",
}


response = requests.get(url, headers=headers)
data = response.json()


city_data = []


for region in data["zpData"]["cityList"]:
    for city in region.get("subLevelModelList", []):
        city_data.append(
            {
                "city_name": city["name"],
                "city_code": city["code"],
            }
        )

csv_file = "city_codes.csv"
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["city_name", "city_code"])
    writer.writeheader()
    writer.writerows(city_data)

print(f"城市信息已保存到 {csv_file} 文件中。")

json_file = "city_codes.json"
with open(json_file, "w", encoding="utf-8") as file:
    json.dump(city_data, file, ensure_ascii=False, indent=4)

print(f"城市信息已保存到 {json_file} 文件中。")
