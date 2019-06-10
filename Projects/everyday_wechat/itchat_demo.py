import itchat
from collections.abc import Iterable
import time, random

itchat.auto_login(hotReload=True)

# 注意实验楼环境的中文输入切换
friend_list = itchat.get_friends()
# print(isinstance(friend_list, Iterable))
# print(hasattr(friend_list, '__iter__'))
itchat.send("a", "filehelper")
for i, friend in enumerate(friend_list):
    if friend["NickName"] == "鹿游原":
        itchat.send("test", friend["UserName"])

    # if i > 10:
    #     break
    # if friend['NickName'] == "test":
    #     print("has test")
    #     itchat.send(u"测试️", friend['UserName'])
    # elif friend["NickName"] == "Lucifer":
    #     print("has luc")
    #     itchat.send("haha", friend['UserName'])


