import itchat
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
import time

itchat.auto_login(hotReload=True)
# friend = itchat.search_friends(name = "Kelly")[0]
friend = itchat.search_friends(name = "鹿游原")[0]

friend_user_name = friend["UserName"]

resp = requests.get('http://open.iciba.com/dsapi')

if resp.status_code == 200:
    contentJson = resp.json()
    content = contentJson.get("content")

def send_stuff():
    itchat.send(u"测试2 - cute dog", friend_user_name)
    itchat.send_image("/Users/aaronyu/Downloads/adorable-animal-animal-photography-1663421.jpg", friend_user_name)
    print('发送成功..\n')

def send_stuff2():
    itchat.send("测试 at {}".format(time.asctime()), friend_user_name)
    print('发送成功..\n')


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(send_stuff2, "interval", seconds = 10)
    scheduler.start()

    # itchat.send(content, friend_user_name)
    # itchat.send("https://zhuanlan.zhihu.com/p/24546514", friend_user_name)
    # itchat.send(u"测试 - cute dog", friend_user_name)
    # itchat.send_image("/Users/aaronyu/Downloads/adorable-animal-animal-photography-1663421.jpg", friend_user_name)