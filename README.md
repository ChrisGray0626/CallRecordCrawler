# CallRecordCrawler
## 功能说明
  在用户许可并提供相应的信息后，爬取用户的通话记录
  
## 数据需求
### 移动
#### 第一批
* 手机号码
* 短信验证码1
#### 第二批
* 服务密码
* 短信验证码2
* 图形验证码
### 电信
#### 第一批
* 手机号码
* 姓名
* 身份证号
* 服务密码
#### 第二批
* 图片验证码
#### 第三批
* 短信验证码
### 联通
#### 第一批
* 手机号码
* 服务密码
* 短信验证码1
#### 第二批
* 短信验证码2
### PS：所有图形验证码均需要将图片发至用户端，自行输入验证码返回（验证码图像识别技术尚不成熟）
## 环境需求
* lxml
* pillow
* selenium
* xrld
## 软件/插件需求
  * chrome
  * chromedriver
  * chromedriver需要与chrome版本对应，当前版本为77.0.3865.120（正式版本）（64 位）
