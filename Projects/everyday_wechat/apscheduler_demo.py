from apscheduler.schedulers.blocking import BlockingScheduler
import time

# 实例化一个调度器
scheduler = BlockingScheduler()


from apscheduler.schedulers.blocking import BlockingScheduler
import time

# 实例化一个调度器
scheduler = BlockingScheduler()

def job1():
    print("{}: 执行任务".format(time.asctime()))

# 添加任务并设置触发方式为3s一次
scheduler.add_job(job1, 'interval', seconds=3)

# 开始运行调度器
scheduler.start()