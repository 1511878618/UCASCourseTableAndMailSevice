# UCASCourseTableAndMailSevice
邮件通知第二天课程
使用须知：

## 依赖包
- python3
- numpy
- pandas

## 使用方式

### 成功运行脚本需要注意的地方
首先，`UCASTable.py`用于生成记录每周课程的`.csv`文件。

第一次运行会调用其中的`showWeekOfSemester`，获取本学期开学周是今年的多少周。根据提示输入今天是本学期第几周就好。

确保本地目录下面会有你的课程信息也就是`test.txt`，里面记录的是你的课程信息。**生成该文件需要使用者前往sep平台的选课系统中的个人课表**，也就是下图

![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-09-07-114544.png)
然后选择你的任意一个课程，复制下图中的信息

![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-09-07-114613.png)

放入一个`.txt`的文件中，然后重复进行，复制粘贴完所有的课程~~
>因为sep似乎禁止使用爬虫~~~~~，咱就这样讲究吧😂😂😅

下图是我的一个示例：
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-09-07-114805.png)


搞定好这个后 就把`UCASTable.py`中最后一行的`main()`里面写入你所创建的`.txt`的文件名就好了~

然后命令行中输入`python UCASTable.py` 根据提示输入就好了。
>如果邮箱啥的输错了可以自行修改`user.csv`

运行成功后会生成`table`目录，该目录下面便可以找到你每周的课程表

**如果需要打开邮箱提示服务，请注册一个邮箱**。这里推荐使用163mail。
下面以163mail为例子介绍如何配置。
1. 登录163mail，在设置找到：![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-09-07-115231.png)
2. 然后打开SMTP服务![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-09-07-115300.png)
3. 在下面找到授权码，添加授权码![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-09-07-115502.png)
4. 然后在`mail.py`中填写相应信息![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-09-07-115603.png)

然后运行`python mail.py`便可以发送第二天的课程啦~

最后如果想要定时发送，则上传到服务器上使用`crontab -e` 配置定时任务
>请记得在里面添加上PATH，避免定时任务不能获取系统的变量~
>![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-09-07-115928.png)
