import re

pattern1 = "abc"
pattern2 = "xyz"
text = "Does this contain abc ?"

match1 = re.search(pattern1, text)
match2 = re.search(pattern2, text)

if not match2:
    print("No match")
    # print(match2.string)

