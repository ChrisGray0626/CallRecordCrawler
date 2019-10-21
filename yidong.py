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

def search(elementId):
    try:
        browser.find_element_by_id(elementId)
        return True
    except :
        return False

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
option.add_argument("--headless")         #隐藏网页
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
serviceCode = input("服务密码：")
messageCodeInput1 = browser.find_element_by_id("sms_pwd_l")
messageCode1 = input("短信验证码：")
for num in messageCode1:                                                                        #输入短信验证码
    messageCodeInput1.send_keys(num)
    time.sleep(0.1)


browser.find_element_by_id("submit_bt").click()                                                       #登录
time.sleep(10)
# new_window = browser.current_window_handle
'''
browser.find_element_by_xpath("//div/div[3]/div/div/div/ul[2]/li/ul/li[4]").click()                   #详单查询
time.sleep(1)
browser.find_element_by_xpath("//div/div[3]/div[3]/div/div/ul/li[2]").click()                         #通话查询
'''
#js="var q=document.documentElement.scrollTop=0"                                                       #将滑动条拉至顶部，否则图片验证码的截取会出错
#browser.execute_script(js)
browser.find_element_by_xpath("//div/div[3]/div/div/div/ul[2]/li/ul/li[4]").click()  # 详单查询
time.sleep(2)
browser.find_element_by_xpath("//div/div[3]/div[3]/div/div/ul/li[2]").click()  # 通话查询
time.sleep(3)

for i in range(1,8):

    browser.find_element_by_id("month" + str(i)).click()
    time.sleep(2)
    #fail1 = browser.find_element_by_id("vec_servpasswd").is_displayed()
    if search('vecbtn') == True:
        time.sleep(2)
        severCodeInput = browser.find_element_by_id("vec_servpasswd")

        for num in serviceCode:                                                                      #输入服务密码
            severCodeInput.send_keys(num)
            time.sleep(0.1)
        # src = yzmImg.get_attribute('src')
        yzmImg = browser.find_element_by_id("imageVec")
        yzmImg.screenshot('yzm.png')                       #截图验证码

        verificationInput = browser.find_element_by_id("vec_imgcode")
        verificationCode = input("图形验证码：")
        for num in verificationCode:
            verificationInput.send_keys(num)
            time.sleep(0.1)
        #verificationInput.send_keys(verificationCode)
        time.sleep(2)
        fail2 = browser.find_element_by_id("failremind").is_displayed()
        while fail2 == True:
            yzmImg.click()

            #yzmImg = browser.find_element_by_id("imageVec")
            yzmImg.screenshot('yzm.png')                                                            # 截图验证码
            verificationInput.clear()
            verificationCode = input("图形验证码：")
            for num in verificationCode:
                verificationInput.send_keys(num)
                time.sleep(0.1)
            time.sleep(2)
            fail = browser.find_element_by_id("failremind").is_displayed()
        timeEnd = time.time()
        time1 = timeEnd - timeStart
#        print(time1)
        if time1 < 65:
            time.sleep(65-time1)                                                         #!!!
#        browser.switch_to_alert().dismiss()
        browser.find_element_by_id("stc-send-sms").click()                                           #发送短信验证码
        timeStart = time.time()
        time.sleep(1)
        browser.switch_to.alert.accept()
        messageCodeInput2 = browser.find_element_by_id("vec_smspasswd")
        messageCode2 = input("短信验证码：")
        for num in messageCode2:                                                                     #输入短信验证码
            messageCodeInput2.send_keys(num)
            time.sleep(0.1)
        #browser.minimize_window()
        browser.find_element_by_id("vecbtn").click()


    time.sleep(2)
    dataList = browser.find_elements_by_xpath("//div/div[3]/div[3]/div/table/tbody/tr/td")
    txt = {}
    a = []
    labelList = browser.find_elements_by_xpath("//div[1]/div[3]/div[3]/div/table/thead/tr/th")
    labelListNumber = len(labelList)
    dataListNumber = len(dataList)

    for label in range(0, dataListNumber):
        trueLabel = label
        label = label % labelListNumber
        txt[labelList[label].text] = dataList[trueLabel].text
        if label == 7:
            a.append(txt)
            txt = {}
    file_name = "yidong" + str(i) + ".json"
#    print(a)
    with open(file_name, 'w', encoding="utf8") as file_obj:
        json.dump(a, file_obj, ensure_ascii=False, indent=4)
    #browser.back()
    time.sleep(2)


