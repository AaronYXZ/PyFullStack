from collections import OrderedDict

ordered = OrderedDict()
ordered['foo'] = 1
ordered['boo'] = 2
ordered['spam'] = 3
ordered['bark'] = 4

for k,v in ordered.items():
    print(k, v)

ordered2 = {}
ordered2['foo'] = 1
ordered2['boo'] = 2
ordered2['spam'] = 3
ordered2['bark'] = 4

for k,v in ordered2.items():
    print(k, v)
