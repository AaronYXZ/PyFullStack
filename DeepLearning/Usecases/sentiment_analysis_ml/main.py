# -*- coding: utf-8  -*-


import logging
import os
import codecs, sys


## read in file content
def get_content(fullname):
    # f = codecs.open(fullname, 'r')
    f = open(fullname, "r", encoding="ISO-8859-1")
    content = f.readline()
    f.close()
    return content


if __name__ == '__main__':
    inp = 'data/ChnSentiCorp_htl_ba_2000'
    folders = ['neg', 'pos']
    for folder_name in folders:
        outp = "2000_" + folder_name + ".txt"
        output = codecs.open(outp, "w")
        i = 0

        rootdir = inp + "/" + folder_name
        for parent, dirnames, filenames in os.walk(rootdir):
            for filename in filenames:
                content = get_content(rootdir + "/" + filename)
                output.writelines(content)
        output.close()

