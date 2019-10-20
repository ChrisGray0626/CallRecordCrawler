from selenium import webdriver
from lxml import etree
from time import sleep
import PIL.Image as Image
import json


def main(phoneNum, serverCode, idNum, name):
    # 初始化
    loginUrl = "http://login.189.cn/web/login"
    driver = webdriver.Chrome()
    driver.get(loginUrl)

    # 输入账号
    AccountInput = driver.find_element_by_name("Account")
    AccountInput.send_keys(phoneNum)
    AccountInput.click()
    sleep(0.5)

    # 密码
    PwdInput = driver.find_element_by_id("txtShowPwd")
    PwdInput.click()

    # 输入框发生了变化
    PwdInput = driver.find_element_by_name("Password")
    PwdInput.send_keys(serverCode)
    sleep(1)

    # 保存验证码
    driver.get_screenshot_as_file("screen.png")
    body = driver.find_element_by_xpath("//body[1]")
    caption = driver.find_element_by_id("imgCaptcha")
    left = int(caption.location['x'])
    top = int(caption.location['y'])
    bottom = int(caption.location['y'] + caption.size['height'])
    originHeight = body.size['height']
    originWidth = body.size['width']
    im = Image.open('screen.png')
    picHeight = im.size[1]
    picWidth = im.size[0]

    left = int(left*picWidth/originWidth)
    right = left + caption.size['width']
    top = int(top*picHeight/originHeight)
    bottom = int(bottom*picHeight/originHeight)

    img = im.crop((left,top,right,bottom))
    img.save('code.png')

    # 读取验证码
    Captcha = driver.find_element_by_name("Captcha")
    caption = input("请输入验证码: ")
    sleep(1)
    Captcha.send_keys(caption)

    # 登录
    loginBtn = driver.find_element_by_id("loginbtn")
    loginBtn.click()
    sleep(1.5)

    # 开始请求
    detailUrl = "https://www.189.cn/dqmh/ssoLink.do?method=linkTo&platNo=10012&toStUrl=https://zj.189.cn/service/queryorder/"
    driver.get(detailUrl)
    sleep(2)

    queryUrl = "http://zj.189.cn//zjpr/service/query/query_order.html?menuFlag=1"
    driver.get(queryUrl)
    sleep(2.5)

    nameBox = driver.find_element_by_name("cdrCondition.usernameyanzheng")
    idBox = driver.find_element_by_name("cdrCondition.idyanzheng")
    nameBox.send_keys(name)
    idBox.send_keys(idNum)

    # 开始通过循环查询每月数据

    for i in range(1, 7):
        monthsTag = driver.find_element_by_xpath('//h3[@id="month_title"]/i')
        monthsTag.click()
        sleep(0.5)
        month = driver.find_element_by_xpath("//ul[@id='chmonth']/li[{}]/a".format(i))
        title = month.text
        try:
            month.click()
        except:
            monthsTag = driver.find_element_by_xpath('//h3[@id="month_title"]/i')
            monthsTag.click()
            month = driver.find_element_by_xpath("//ul[@id='chmonth']/li[{}]/a".format(i))
            title = month.text
            month.click()


        print("月份:", title)
        if i == 1:
            codeKey = driver.find_element_by_id("codekey")
            codeKey.click()
            inputCodeKey = driver.find_element_by_name("cdrCondition.randpsw")
            key = input("请输入短信验证码: ")
            inputCodeKey.send_keys(key)
            sleep(1)
            enter = driver.find_element_by_xpath('//p[@class="tn-c mt-20"]/a')
            enter.click()
            sleep(0.5)

        submit = driver.find_element_by_name("Submit")
        submit.click()

        sleep(0.5)

        driver.switch_to.window(driver.window_handles[1])
        sleep(3)
        source = driver.page_source

        getRecord(source, title)
        driver.close()

        driver.switch_to.window(driver.window_handles[0])


def getRecord(source, title):
    if "您没有该项清单" in source:
        print("您没有该项清单")
        save("", title)
        return
    html = etree.HTML(source)

    data = []
    for i in range(3, 100):
        context = html.xpath('//table[@class="cdrtable"][1]/tbody/tr[{}]/td/text()'.format(i))
        if len(context) == 0:
            break
        number = context[0]
        phoneType = context[1]
        time = context[2]
        length = context[3]
        location = context[4]
        callType = context[5]
        fee = context[6]
        reduce = context[7]
        all = context[8]

        dic = {
            "对方号码": number,
            "呼叫类型": phoneType,
            "通话起始时间": time,
            "通话时长": length,
            "通话地": location,
            "通话类型": callType,
            "通话费": fee,
            "减免": reduce,
            "费用小计": all,
        }

        data.append(dic)
    save(data, title)
    print(data)


def save(data, title):
    path = title+".json"
    data = json.dumps(data, ensure_ascii=False)
    with open(path, "a", encoding="utf-8") as f:
        f.write(data)


if __name__ == '__main__':
    phoneNum = input("请输入您的手机号：")
    serverCode = input("请输入您的服务密码：")
    idNum = input("请输入您的身份证号：")
    name = input("请输入您的姓名：")
    main(phoneNum, serverCode, idNum, name)
