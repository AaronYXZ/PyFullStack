import itchat

itchat.auto_login(hotReload=True)

# 注意实验楼环境的中文输入切换
itchat.send(u'测试消息发送', 'filehelper')
itchat.send(u'测试消息发送', "Kelly")
itchat.send(u'测试消息发送', "Kelly_zxy22")
itchat.send(u'测试消息发送', "Lucifer")
friend_list = itchat.get_friends()[1:]
friend = friend_list[0]
if friend['NickName'] == "Kelly":
    itchat.send(u"测试 晚安宝贝❤️", friend['UserName'])
print("test")


# @itchat.msg_register(itchat.content.TEXT)
# def text_reply(msg):
#     return msg.text
#
# itchat.run()
