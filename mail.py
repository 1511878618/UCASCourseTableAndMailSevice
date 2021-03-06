#coding=utf-8
from email.mime.text import MIMEText#专门发送正文
from email.mime.multipart import MIMEMultipart#发送多个部分
from email.mime.application import MIMEApplication#发送附件
import smtplib#发送邮件
 
    
import pandas as pd 
import datetime
import re
import sys
import os 
##获取当天的信息
with open('semester.info','r') as f:
    info = f.read()
beginWeek = re.findall("周:\d*",info)[0].split(':')[1]

###获取第二天的日期
today = datetime.datetime.today()

targetweek = today.isocalendar()[1] - int(beginWeek)+1
tomorrowDay  = today+datetime.timedelta(days=1)
targetWeekNum = tomorrowDay.isocalendar()[2]

def turnChineseWeekToNumberWeek(chineseWeek):
    
    dic={"星期一":1,"星期二":2,"星期三":3,"星期四":4,"星期五":5,"星期六":6,"星期日":7}
    return dic[chineseWeek]


## 获取要发送的附件
def check(user):
    # with open('semester.info','r') as f:
    #     info = f.read()
    # beginWeek = re.findall("周:\d*",info)[0].split(':')[1]
    # #获取第二天的日期
    # today = datetime.datetime.today()

    # targetweek = today.isocalendar()[1] - int(beginWeek)+1
    # targetWeekNum = today.isocalendar()[2]+1
    # targetweek = 3
    # targetWeekNum = 5

    #获取第二天的课程
    path = 'table/''{}/'.format(user) + '{}周.csv'.format(targetweek)
    test = pd.read_csv(path)
    print(targetWeekNum)
    # print(test.columns.drop('time')[targetWeekNum-1])
    targetDayTable = pd.read_csv(path)[['time',test.columns.drop('time')[targetWeekNum-1]]]
    # print(test.columns)
    print(targetDayTable)
    if targetDayTable.iloc[:,1].isnull().all():
        noClass=True
        mailtext= '恭喜{}，没课'.format(user)
        print(mailtext)
        sys.exit(0)
        
    else:
    #     print('sending')    
        try:
            os.makedirs("tomorrow")
        except:
            pass

        targetDayTable.index = range(1,13)
        targetDayTable.to_csv("tomorrow/"+user+'.csv',index=0)
        test.to_csv("tomorrow/"+user+'{}周.csv'.format(targetweek),index=0)
        return True




### 如果发送    
    
#设置服务器所需信息
#163邮箱服务器地址
def emailTable(receiversMail,targetDayTablePath):
    mail_host = 'smtp.163.com'  
    #163用户名
    mail_user = 'xutingfengtest'  
    #密码(部分邮箱为授权码) 
    mail_pass = 'JFCNDHDFCHIGEIQY'   #使用授权码
    #邮件发送方邮箱地址
    sender = 'xutingfengtest@163.com'  

    #邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发

    ##使用：请在该处添加你的邮件
    receivers = [receiversMail]  #'1511878618@qq.com'


    #设置email信息

    #邮件主题       
    subject = 'courseInfo'  #邮件主题


    #构造一个邮件体：正文 附件
    msg = MIMEMultipart()
    msg['Subject']=subject    #主题
    msg['From']=sender      #发件人
    msg['To']=receivers[0]           #收件人

    ## 设置正文
    targetDayTable = pd.read_csv(targetDayTablePath)
    morningTable = targetDayTable.iloc[0:4,:]
    morningClass = morningTable.iloc[:,1].value_counts().index

    if len(morningClass) ==0:
        morningText="上午没课嗷，可以快乐玩耍！~"
        pass
    else:
        morningClassStart = morningTable[morningTable.iloc[:,1] == morningClass[0]]['time'].iloc[0].split('~')[0]
        morningClassEnd = morningTable[morningTable.iloc[:,1] == morningClass[0]]['time'].iloc[-1].split('~')[1]
        morningText="上午的课程是{}，上课时间为：{}，下课时间为：{}。".format(morningClass[0],morningClassStart,morningClassEnd)
    print(morningText)
    #下午
    noonTable = targetDayTable.iloc[4:8,:]
    noonClass = noonTable.iloc[:,1].value_counts().index

    if len(noonClass) ==0:
        noonText="中午没课嗷，可以快乐玩耍！~"
        pass
    else:
        noonClassStart = noonTable[noonTable.iloc[:,1] == noonClass[0]]['time'].iloc[0].split('~')[0]
        noonClassEnd = noonTable[noonTable.iloc[:,1] == noonClass[0]]['time'].iloc[-1].split('~')[1]
        noonText="下午的课程是{}，上课时间为：{}，下课时间为：{}。".format(noonClass[0],noonClassStart,noonClassEnd)
    print(noonText)
        
    #晚上
    nightTable = targetDayTable.iloc[8:12,:]
    # print(nightTable)
    nightClass = nightTable.iloc[:,1].value_counts().index
    if len(nightClass) ==0:
        nightText="晚上没课嗷，可以快乐玩耍！~"
        pass
    else:
        nightClassStart = nightTable[nightTable.iloc[:,1] == nightClass[0]]['time'].iloc[0].split('~')[0]
        nightClassEnd = nightTable[nightTable.iloc[:,1] == nightClass[0]]['time'].iloc[-1].split('~')[1]
        nightText="晚上的课程是{}，上课时间为：{}，下课时间为：{}。".format(nightClass[0],nightClassStart,nightClassEnd)
    print(nightText)



    email_text = '明天，也就是：星期{}'.format(targetWeekNum)+morningText+noonText+nightText #邮件正文

    ###构建正文
    part_text=MIMEText(email_text,)
    msg.attach(part_text)             #把正文加到邮件体里面去

    ## 设置附件内容
    # file = pd.read_csv("tomorrow/"+user+'{}周.csv'.format(targetweek))

    #file = targetDayTablePath
    file = targetDayTablePath[:-4] + '{}周.csv'.format(targetweek)
    print(file)
    part_attach1 = MIMEApplication(open(file,'rb').read())   #打开附件

    part_attach1.add_header('Content-Disposition','attachment',filename=file) #为附件命名

    msg.attach(part_attach1)   #添加附件
    
    # 发送邮件 SMTP
    try:
        smtpObj = smtplib.SMTP() 
        #连接到服务器
        smtpObj.connect(mail_host,25)
        #登录到服务器
        smtpObj.login(mail_user,mail_pass) 
        #发送
        smtpObj.sendmail(
            sender,receivers,msg.as_string()) 
        #退出
        smtpObj.quit() 
        print('success')
    except smtplib.SMTPException as e:
        print('error',e) #打印错误



def main():
    # print("hi")
    usersData = pd.read_csv('user.csv')
    for x,y in usersData.iterrows():
        user = y['userName']
        receivers = y['mailAddress']
        if check(user=user):
            #发送邮件
            print('发送邮件给:{}:{}'.format(user,receivers))
            targetDayTablePath = "tomorrow/"+user+'.csv'
            emailTable(receivers,targetDayTablePath)
        else:
            print('没有发送邮件给{}:{}'.format(user,receivers))


main()




