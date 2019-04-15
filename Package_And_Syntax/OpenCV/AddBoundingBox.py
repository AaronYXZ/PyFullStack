import cv2
import yaml
import numpy as np

img = cv2.imread("resources/account001.png")
print(img.shape)

def getBB(matches_yml):
    with open(matches_yml) as tmp:
        tmpDict = yaml.load(tmp)
    matched_lst = tmpDict['matches']
    m = [ [(int(x['left']), int(x['top'])), (int(x['right']), int(x['bottom']))] for x in matched_lst]
    return m

def getCrop(template_file, img_file, thresh = 0.8):
    tmp_rgb = cv2.imread(template_file)
    tmp_gray = cv2.cvtColor(tmp_rgb, cv2.COLOR_BGR2GRAY)

    img_rgb = cv2.imread(img_file)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(img_gray, tmp_gray, method = cv2.TM_CCOEFF_NORMED)
    w, h = tmp_gray.shape[::-1]
    loc = np.where(res > thresh)
    return w, h, loc

    # return [ [(pt[0] + w, pt)] for pt in zip(*loc[::-1])]


if __name__ == '__main__':
    template_file = "resources/template_account001.png"
    img_file ="resources/account001.png"
    img = cv2.imread(img_file)
    # m = getBB("resources/account001.yml")
    color = (0,255,0)
    thickness = 4
    w, h, loc = getCrop(template_file, img_file)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), color = color, thickness=thickness)
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # for cor in m:
    #     cv2.rectangle(img, cor[0], cor[1], color, thickness=thickness)
    # cv2.imwrite("resources/account001_match_mark.png", img)
