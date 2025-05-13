import re
import time
import random
import json
from bs4 import BeautifulSoup
import pandas as pd
import seaborn as sns
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

job = "Python"
page = 6
htmls_list = []
job_list = []

# 设置 chromedriver 的路径
chromedriver_path = r"C:\Program Files (x86)\QQBrowser\chromedriver.exe"

# 设置 Chrome 浏览器选项
chrome_options = Options()
chrome_options.add_argument('--disable-gpu')

# 创建一个 Service 对象来传递 chromedriver 路径
service = Service(executable_path=chromedriver_path)

# 设置页面加载超时和脚本超时
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.set_page_load_timeout(120)  # 页面加载超时设置为 120 秒
driver.set_script_timeout(120)     # 脚本超时设置为 120 秒

# 遍历页码抓取网页
for num in range(1, page + 1):
    url = "https://www.zhipin.com/c101010100/?query={}&page={}&ka=page-{}".format(job, num, num)

    driver.get(url)

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.job-primary"))
        )
        htmls = driver.page_source
        htmls_list.append(str(htmls))  # 将获取页面信息添加至网页存储列表
    except Exception as e:
        print(f"页面加载失败: {e}")
    
    # 程序休眠，防止频繁请求
    ran_time = random.randint(10, 20)
    time.sleep(ran_time)  # 程序休眠

driver.quit()

# 解析所有页面的职位信息并保存
for htmls in htmls_list:
    soup = BeautifulSoup(htmls, 'html.parser')  # 解析网页

    # 遍历所有招聘岗位的 div
    for i in soup.find_all("div", class_="job-primary"):
        job = i.find_all("a")                                            # 获取招聘岗位信息
        area = i.find_all('span', class_='job-area')                     # 获取工作地点
        salary = i.find_all('span', class_='red')                        # 获取薪酬信息
        title = i.find_all("h3")[1].get_text()                           # 获取企业名称
        industry = i.find_all('a', class_="false-link")[0].get_text()    # 获取所属行业
        edu = i.find_all('p')[0].text                                    # 获取学历要求
        scale = i.find_all('p')[1].text                                  # 获取条件信息
        url = "https://www.zhipin.com/" + i.find_all("div", class_="primary-box")[0]['href']  # 获取详情页信息

        # 将所有信息保存至 job_list
        job_list.append({
            "企业名称": title,
            "行业": industry,
            "职位名称": job[0]['title'],
            "工作地点": area[0].get_text(),
            "学历要求": edu,
            "条件要求": scale,
            "薪资": salary[0].get_text(),
            "详情链接": url
        })

with open("Python_info.json", "w", encoding="utf-8") as f:
    json.dump(job_list, f, ensure_ascii=False, indent=4)
print("数据已成功写入 job_info.json 文件")
