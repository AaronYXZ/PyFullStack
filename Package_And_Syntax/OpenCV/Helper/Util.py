import cv2
import yaml
import numpy as np
import os


def getBB(yml):
    try:
        with open(yml) as tmp:
            tmpDict = yaml.load(tmp)
        matched_lst = tmpDict['matches']
        m = [[(int(x['left']), int(x['top'])), (int(x['right']), int(x['bottom']))] for x in matched_lst]
        return m
    except FileNotFoundError:
        return []


def getCrop(img_file, template_file, thresh=0.8):
    tmp_rgb = cv2.imread(template_file)
    if tmp_rgb is None:
        return
    tmp_gray = cv2.cvtColor(tmp_rgb, cv2.COLOR_BGR2GRAY)

    img_rgb = cv2.imread(img_file)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(img_gray, tmp_gray, method=cv2.TM_CCOEFF_NORMED)
    w, h = tmp_gray.shape[::-1]
    loc = np.where(res > thresh)
    return w, h, loc


def annotate(img, yml, color, thickness):
    img_rgb = cv2.imread(img)
    img_name = img.split("/")[-1].split(".")[0] + "_annotated.png"
    m = getBB(yml)
    for cor in m:
        cv2.rectangle(img_rgb, cor[0], cor[1], color, thickness=thickness)
    cv2.imwrite(os.path.join("resources/AnnotateResults", img_name), img_rgb)


def crop(img, template, color, thickness):
    img_rgb = cv2.imread(img)
    img_name = img.split("/")[-1].split(".")[0] + "_cropped.png"
    try:
        w, h, loc = getCrop(img, template, 0.8)
    except TypeError:
        return
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), color = color, thickness=thickness)
    cv2.imwrite(os.path.join("resources/AnnotateResults", img_name), img_rgb)
