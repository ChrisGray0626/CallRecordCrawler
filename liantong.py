from selenium import webdriver
import xlrd
from collections import OrderedDict
import json
import os

# xls文件下载路径
path = "F:\data"
if not os.path.exists(path):
    os.makedirs(path)
options = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups': 0,
         'download.default_directory': path}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(chrome_options=options)
driver.get('https://uac.10010.com/portal/homeLoginNew')

while True:
    try:
        phoneInput = driver.find_element_by_xpath("//input[@class = 'iptStyle width250 username']")
        phoneInput.clear()
        break
    except:
        continue

phoneNum = input("手机号码：")
# phoneNum = "13173625819"
for num in phoneNum:
    phoneInput.send_keys(num)

# 获取短信验证码按钮
while True:
    try:
        driver.find_element_by_xpath("//span[@class = 'randomSpan ie6Png countdown']").click()
        break
    except:
        continue

serverCode = input("服务密码：")
# serverCode = '123589'
severCodeInput = driver.find_elements_by_xpath("//input[@class = 'iptStyle width145 password']")[0]
severCodeInput.clear()
for num in serverCode:
    severCodeInput.send_keys(num)

messageCode1 = input("短信验证码：")
messageCodeInput1 = driver.find_elements_by_xpath("//input[@class = 'iptStyle width145 password']")[1]
messageCodeInput1.clear()
for num in messageCode1:
    messageCodeInput1.send_keys(num)
# 登录按钮
driver.find_element_by_xpath("//input[@class = 'loginBtn ie6Png mtr40 width302']").click()

# 查询按钮，跳转至 https://iservice.10010.com/e5/query.html
while True:
    try:
        driver.find_element_by_xpath("//a[@id = 'query']").click()
        break
    except:
        continue
# 始终获得当前最后的窗口
for handle in driver.window_handles:
    driver.switch_to.window(handle)
print(driver.current_url)
# # all_window = brower.window_handles
# # for window in all_window:
# #     if window != current_window:
# #         brower.switch_to.window(window)
# # current_window = brower.current_window_handle
# print("goto")
# time.sleep(5)

# 通话详单按钮，跳转至 https://iservice.10010.com/e4/query/bill/call_dan-iframe.html
while True:
    try:
        driver.find_element_by_xpath("//div[@id = 'NavId']/div[@class = 'NavDivs width1200 bgFFF']/ul[@class = 'fl threeNav']/li/a[@title = '通话详单']").click()
        break
    except:
        continue

# 始终获得当前最后的窗口
for handle in driver.window_handles:
    driver.switch_to.window(handle)
print(driver.current_url)

# 获取验证码按钮
while True:
    try:
        driver.find_element_by_xpath("//div[@id = 'huoqu_buttons']").click()
        break
    except:
        continue

messageCode2 = input("验证码：")
messageCode2Input = driver.find_element_by_xpath("//input[@id = 'input']")
for num in messageCode2:
    messageCode2Input.send_keys(num)
# 登录按钮
driver.find_element_by_xpath("//input[@id = 'sign_in']").click()

while True:
    try:
        monthsBtn = driver.find_elements_by_xpath("//ul[@class = 'score_list_ul score_list_min ']/li")
        break
    except:
        continue

for i in range(0, 6):
    # 月份选择按钮
    try:
        monthsBtn[i].click()
    except:
        pass
    # 滑动到页面底部
    js = "var q=document.documentElement.scrollTo(0,document.body.scrollHeight)"
    driver.execute_script(js)
    # 导出按钮
    while True:
        try:
            driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[4]/div/div[5]/div[2]/div/div[1]/div[3]/div[2]/div[4]/div[2]/div[3]/div[1]/div[5]/input[2]").click()
            break
        except:
            # 无详单记录【2114030170】
            try:
                if driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[4]/div/div[5]/div[2]/div/div[1]/div[3]/div[2]/div[4]/div[2]/div[3]/div[2]/div/p[1]"):
                    break
            except:
                path
    # 滑动到页面顶部
    js = "var q=document.documentElement.scrollTop=0"
    driver.execute_script(js)

# xls转json格式
files = os.listdir(path)
for file in files:
    if ".xls" not in file:
        continue
    wb = xlrd.open_workbook(os.path.join(path, file))
    dictList = []
    sheet = wb.sheet_by_index(0)  # 选择第一页表格
    title = sheet.row_values(0)  # 表头，作为json的key
    # print(title)
    for row in range(1, sheet.nrows):
        rowValues = sheet.row_values(row)  # 一行的所有值
        Dict = OrderedDict()  # 有序字典
        for col in range(0, len(rowValues)):
            # print("key:{0}, value:{1}".format(title[col], rowValues[col]))
            Dict[title[col]] = rowValues[col]
        dictList.append(Dict)
    with open("liantong" + str(i) + ".json", "w", encoding="utf8") as f:
        json.dump(dictList, f, ensure_ascii=False, indent=4)
