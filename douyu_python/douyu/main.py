import datetime
import time
# 定时任务 # 设定一个标签 确保是运行完定时任务后 再修改时间
flag = 0
# 获取当前时间
now = datetime.datetime.now() # 启动时间 # 启动时间为当前时间 加5秒
sched_timer = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second) + datetime.timedelta(seconds=5)
# 启动时间也可自行手动设置 # sched_timer = datetime.datetime(2017,12,13,9,30,10)
while (True): # 当前时间
    now = datetime.datetime.now() # print(type(now)) # 本想用当前时间 == 启动时间作为判断标准，但是测试的时候 毫秒级的时间相等成功率很低 而且存在启动时间秒级与当前时间毫秒级比较的问题 # 后来换成了以下方式，允许1秒之差
    if sched_timer < now < sched_timer + datetime.timedelta(seconds=1):
        time.sleep(1) # 主程序
        main()
        flag = 1
    else:
        if flag == 1:
            sched_timer = sched_timer + datetime.timedelta(minutes=2)
            flag = 0

def main():

