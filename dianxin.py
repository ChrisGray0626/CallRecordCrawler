from selenium import webdriver
import lxml
from lxml import etree
from time import sleep
import PIL.Image as Image
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def main(phoneNum,password,idNum,name):
    # 初始化
    loginUrl = "http://login.189.cn/web/login"

    options = Options()
    options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    driver.get(loginUrl)

    # 输入账号
    accountInput = driver.find_element_by_name("Account")
    accountInput.send_keys(phoneNum)
    accountInput.click()

    sleep(0.5)

    # 密码
    pwdInput = driver.find_element_by_id("txtShowPwd")
    pwdInput.click()

    # 输入框发生了变化
    pwdInput = driver.find_element_by_name("Password")
    pwdInput.send_keys(password)

    # 保存验证码
    driver.get_screenshot_as_file("screen.png")
    body = driver.find_element_by_xpath("//body[1]")
    caption = driver.find_element_by_id("imgCaptcha")
    caption.screenshot("code.png")

    # 读取验证码
    Captcha = driver.find_element_by_name("Captcha")
    caption = input("请输入验证码: ")
    sleep(1)
    Captcha.send_keys(caption)

    # 登录
    loginBtn = driver.find_element_by_id("loginbtn")
    loginBtn.click()
    wait.until(EC.presence_of_element_located((By.XPATH,"//a[@class='headmain_bg']")))



    # 开始请求
    detailUrl = "https://www.189.cn/dqmh/ssoLink.do?method=linkTo&platNo=10012&toStUrl=https://zj.189.cn/service/queryorder/"
    driver.get(detailUrl)

    wait.until(EC.presence_of_element_located((By.XPATH,"//img[@class='dpb mb5']")))

    queryUrl = "http://zj.189.cn//zjpr/service/query/query_order.html?menuFlag=1"
    driver.get(queryUrl)
    wait.until(EC.presence_of_element_located((By.XPATH,"//a[@id='codekey']")))

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


        print("月份:",title)
        if i == 1:
            codekey = driver.find_element_by_id("codekey")
            codekey.click()
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
        wait.until(EC.presence_of_element_located((By.XPATH,"//input[@name='button']")))
        try:
            source = driver.page_source
        except:
            source = ""

        getRecord(source, title)
        driver.close()

        driver.switch_to.window(driver.window_handles[0])


def getRecord(source, title):
    if "您没有该项清单" in source:
        print("您没有该项清单")
        save("",title)
        return
    html = etree.HTML(source)

    data = []
    for i in range(3,100):
        context = html.xpath('//table[@class="cdrtable"][1]/tbody/tr[{}]/td/text()'.format(i))
        headers = html.xpath('//table[@class="cdrtable"][1]/tbody/tr[2]/td/text()')

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
            headers[1]: number,
            headers[2]: phoneType,
            headers[3]: time,
            headers[4]:length,
            headers[5]: location,
            headers[6]:callType,
            headers[7]:fee,
            headers[8]:reduce,
            headers[9]:all,
        }

        data.append(dic)
    save(data, title)
    print(data)


def save(data, title):
    path = title+".json"
    data = json.dumps(data, ensure_ascii=False)
    with open(path,"a",encoding="utf-8") as f:
        f.write(data)


if __name__ == '__main__':
    #依次填入手机号，服务密码，身份证号，姓名
    phoneNum = input("请输入手机号: ")
    password = input("请输入服务密码: ")
    idNum = input("请输入身份证号: ")
    name = input("请输入姓名: ")

    main(phoneNum, password, idNum, name)
