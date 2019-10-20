import requests
import urllib
import random
from datetime import datetime
import http.cookiejar as cookielib
import sys
import io
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import Select
from PIL import Image
import json
phoneNum = '13777822579'
serviceCode = 'xxx'
messageCode1 = 'xxx'
messageCode2 = 'xxx'
verificationCode = 'xxx'
########################
suofang: float = 1.25
#  code_mod1 = 1 service ;= 0 message1
loginMod = 1
region = "cj"
mesbotton1 = 1
mesbotton2 = 0

option = webdriver.ChromeOptions()

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
browser = webdriver.Chrome(options=option)
#browser.minimize_window()
browser.get('https://login.10086.cn/login.html?channelID=12003&backUrl=https://shop.10086.cn/i/?f=home')
#browser.maximize_window()

#loginMod = input("选择服务密码请输入1，选择短信验证码请输入2:")
#print(loginMod)
#if loginMod is "2":
browser.find_element_by_id("sms_login_1").click()
time.sleep(0.5)
phoneInput1 = browser.find_element_by_id("sms_name")
phoneNum = input("手机号码：")
for num in phoneNum:                                                                            #输入手机号码
    phoneInput1.send_keys(num)
    time.sleep(0.1)

browser.find_element_by_id("getSMSPwd1").click()                                                #发送短信验证码
timeStart = time.time()
messageCodeInput1 = browser.find_element_by_id("sms_pwd_l")
messageCode1 = input("短信验证码：")
for num in messageCode1:                                                                        #输入短信验证码
    messageCodeInput1.send_keys(num)
    time.sleep(0.1)


browser.find_element_by_id("submit_bt").click()                                                       #登录
time.sleep(10)
# new_window = browser.current_window_handle

browser.find_element_by_xpath("//div/div[3]/div/div/div/ul[2]/li/ul/li[4]").click()                   #详单查询
time.sleep(1)
browser.find_element_by_xpath("//div/div[3]/div[3]/div/div/ul/li[2]").click()                         #通话查询

js="var q=document.documentElement.scrollTop=0"                                                       #将滑动条拉至顶部，否则图片验证码的截取会出错
browser.execute_script(js)

browser.find_element_by_xpath("//div/div[3]/div/div/div/ul[2]/li/ul/li[4]").click()  # 详单查询
time.sleep(1)
browser.find_element_by_xpath("//div/div[3]/div[3]/div/div/ul/li[2]").click()  # 通话查询
time.sleep(1)
for i in range(1,7):
    browser.find_element_by_id("month" + str(i)).click()
    time.sleep(2)
    if i == 1:
        browser.find_element_by_id("stc-send-sms").click()                                           #发送短信验证码
        time.sleep(3)
        severCodeInput = browser.find_element_by_id("vec_servpasswd")
        serviceCode = input("服务密码：")
        for num in serviceCode:                                                                      #输入服务密码
            severCodeInput.send_keys(num)
            time.sleep(0.1)
        browser.maximize_window()  # 窗口最大化
        browser.save_screenshot("printscreen.png")  # 截屏
        yzmImg = browser.find_element_by_id("imageVec")
        location = yzmImg.location  # 图片验证码坐标
        size2 = yzmImg.size  # 图片验证码尺寸
        # print(location)
        rangle = (int(location['x']), int(location['y']),
                  int(location['x'] + size2['width']), int(location['y'] + size2['height']))
        num = Image.open("printscreen.png")
        size1 = num.size
        num = num.resize((int(size1[0] / suofang), int(size1[1] / suofang)))
        img = num.crop(rangle)
        img.save('Yzm_img.png')
        # src = yzmImg.get_attribute('src')
        verificationInput = browser.find_element_by_id("vec_imgcode")
        verificationCode = input("图形验证码：")
        verificationInput.send_keys(verificationCode)
        time.sleep(2)
        fail = browser.find_element_by_id("failremind").is_displayed()
        while fail == True:
            yzmImg.click()

            browser.maximize_window()  # 窗口最大化
            browser.save_screenshot("printscreen.png")  # 截屏
            # yzmImg = browser.find_element_by_id("imageVec")
            # location = yzmImg.location  # 图片验证码坐标
            # size2 = yzmImg.size  # 图片验证码尺寸
            # print(location)
            rangle = (int(location['x']), int(location['y']),
                      int(location['x'] + size2['width']), int(location['y'] + size2['height']))
            num = Image.open("printscreen.png")
            size1 = num.size
            num = num.resize((int(size1[0] / suofang), int(size1[1] / suofang)))
            img = num.crop(rangle)
            img.save('Yzm_img.png')
            verificationInput.clear()
            verificationCode = input("图形验证码：")
            verificationInput.send_keys(verificationCode)
            time.sleep(2)
            fail = browser.find_element_by_id("failremind").is_displayed()
        timeEnd = time.time()
        time1 = timeEnd - timeStart
#        print(time1)
        if time1 < 65:
            time.sleep(65-time1)                                                         #!!!
#        browser.switch_to_alert().dismiss()
        browser.switch_to.alert.accept()
        messageCodeInput2 = browser.find_element_by_id("vec_smspasswd")
        messageCode2 = input("短信验证码：")
        for num in messageCode2:                                                                     #输入短信验证码
            messageCodeInput2.send_keys(num)
            time.sleep(0.1)
        #browser.minimize_window()
        browser.find_element_by_id("vecbtn").click()
        time.sleep(2)
        browser.find_element_by_id("month" + str(i)).click()

    dataList = browser.find_elements_by_xpath("//div/div[3]/div[3]/div/table/tbody/tr/td")
    txt = {}
    a = []
    j = 1
    for num in dataList:
        z = num.text
#        print(z)
        if j == 1:
            txt["起始时间"] = z
        elif j == 2:
            txt["通信地点"] = z
        elif j == 3:
            txt["通信方式"] = z
        elif j == 4:
            txt["对方号码"] = z
        elif j == 5:
            txt["通信时长"] = z
        elif j == 6:
            txt["通信类型"] = z
        elif j == 7:
            txt["套餐优惠"] = z
        elif j == 8:
            txt["实收通信费（元）"] = z
            a.append(txt)
            txt = {}
        j = (j%8) + 1
    file_name = "yidong" + str(i) + ".json"
    with open(file_name, 'w', encoding="utf8") as file_obj:
        json.dump(a, file_obj, ensure_ascii=False, indent=4)
    browser.back()
    time.sleep(2)

    #dataList = browser.find_elements_by_xpath("//div/div[3]/div[3]/div/table/tbody//tr").get_attribute('outerHTML')
    #print(dataList)

