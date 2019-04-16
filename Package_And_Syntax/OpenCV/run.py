import cv2
import numpy as np
import os
import fnmatch
from Helper.Util import getBB, getCrop
from Helper.Eval import IoU


def matchTemplate(img_rgb, template_rgb, method=cv2.TM_CCOEFF_NORMED, thresh=0.9):
    """

    :param img_rgb: rgb representaion of the image (canvas to be searched on)
    :param template_rgb: rgb representation of the template (to be searched for)
    :param method: OpenCV template matching methods
    :param thresh: threshold to filter matching results
    :return:
    """
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template_rgb, cv2.COLOR_BGR2GRAY)
    w, h = template_gray.shape[::-1]
    res = cv2.matchTemplate(img_gray, template_gray, method)
    loc = np.where(res >= thresh)  ## https://www.zhihu.com/question/62844162
    ReframeList = []
    for pt in zip(*loc[::-1]):
        Reframe = [pt[0], pt[1], pt[0] + w, pt[1] + h]
        ReframeList.append(Reframe)

def getColorCode(Reframe, GTframeList, threshold):
    """

    :param Reframe: Cropped frame based on template matching
    :param GTframe: Ground truth frame from yml
    :return: GTframe with highest IoU
    """
    colorCode = None
    IoU_max = 0

    for GTframe in GTframeList:
        IoU = IoU(Reframe, GTframe)
        if IoU > threshold and IoU > IoU_max:
            IoU_max = IoU
            colorCode = GTframe.color
    return Reframe, IoU_max, colorCode

def HistSimilarityScore(Reframe, template, *args):
    """

    :param Reframe:
    :param template:
    :return: Reframe and Template similarity score
    """
    ############# crop rectangles that are in loc, then compare histograms and keep the ones that match colors
    h_bins = 50
    s_bins = 60
    histSize = [h_bins, s_bins]

    # hue varies from 0 to 179, saturation from 0 to 255
    h_ranges = [0, 180]
    s_ranges = [0, 256]
    ranges = h_ranges + s_ranges  # concat lists
    # Use the 0-th and 1-st channels
    channels = [0, 1]

    cropped_hsv = cv2.cvtColor(Reframe, cv2.COLOR_BGR2HSV)
    template_hsv = cv2.cvtColor(template, cv2.COLOR_BGR2HSV)
    cropped_hist = cv2.calcHist([cropped_hsv], channels, None, histSize, ranges, accumulate=False)
    template_hist = cv2.calcHist([template_hsv], channels, None, histSize, ranges, accumulate=False)

    cv2.normalize(template_hist, cropped_hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    similarity_score = cv2.compareHist(template_hist, cropped_hist)
    return similarity_score


path = "/Users/aaronyu/Desktop/Project14_Image/WorkSpace/Train"

if __name__ == '__main__':

    imgPath = os.path.join(path, "img")
    templatePath = os.path.join(path, "template")
    ymlPath = os.path.join(path, "yml")
    files = fnmatch.filter(os.listdir(imgPath), "*.png")
    for file in files:
        # print("----" * 100)
        # print(file)
        imgFile = os.path.join(imgPath, file)
        ymlFile = os.path.join(ymlPath, file.replace("png", "yml"))
        templateFile = os.path.join(templatePath, file)
        m = getBB(ymlFile)

        w, h, loc = getCrop(imgFile, templateFile, 0.9, cv2.TM_CCOEFF_NORMED)
        for pt in zip(*loc[::-1]):
            Reframe = [pt[0], pt[1], pt[0] + w, pt[1] + h]
            score = 0
            for cor in m:
                GTframe = [x for ele in cor for x in ele]
                score = max(IoU(Reframe, GTframe), score)
            print(score)
            if score > threshold:
                TP += 1
            else:
                FP += 1
    print("----" * 100)
    print(1.0 * TP / (TP + FP))
