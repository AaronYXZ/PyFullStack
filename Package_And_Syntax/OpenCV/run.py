import cv2
import numpy as np
import os
import fnmatch
from Helper.Util import getBB, getCrop
from Helper.Eval import IoU
import pandas as pd


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

def HistSimilarityScore(crop_rgb, template_rgb):
    """

    :param Reframe:
    :param template_rgb:
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

    cropped_hsv = cv2.cvtColor(crop_rgb, cv2.COLOR_BGR2HSV)
    template_hsv = cv2.cvtColor(template_rgb, cv2.COLOR_BGR2HSV)
    cropped_hist = cv2.calcHist([cropped_hsv], channels, None, histSize, ranges, accumulate=False)
    template_hist = cv2.calcHist([template_hsv], channels, None, histSize, ranges, accumulate=False)

    cv2.normalize(template_hist, cropped_hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    similarity_score = cv2.compareHist(template_hist, cropped_hist, cv2.HISTCMP_CORREL)
    return similarity_score


path = "/Users/aaronyu/Desktop/Project14_Image/WorkSpace/Train"

if __name__ == '__main__':
    results = []
    threshold = 0.5

    imgPath = os.path.join(path, "img")
    templatePath = os.path.join(path, "template")
    ymlPath = os.path.join(path, "yml")
    files = fnmatch.filter(os.listdir(imgPath), "*.png")
    for file in files:
        imgFile = os.path.join(imgPath, file)
        ymlFile = os.path.join(ymlPath, file.replace("png", "yml"))
        templateFile = os.path.join(templatePath, file)
        lst = getBB(ymlFile)
        template_rgb = cv2.imread(templateFile)
        img_rgb = cv2.imread(imgFile)
        w, h, loc = getCrop(imgFile, templateFile, 0.9, cv2.TM_CCOEFF_NORMED)
        for pt in zip(*loc[::-1]):
            tmp_dict = {}
            re_frame = [pt[0], pt[1], pt[0] + w, pt[1] + h]
            tmp_dict['file'] = file
            tmp_dict['re_frame'] = re_frame
            score = 0
            frame = None
            for gt_frame in lst:
                IoU_score = IoU(re_frame, gt_frame)
                if IoU_score > threshold and IoU_score > score:
                    score = IoU_score
                    frame = gt_frame
            tmp_dict['gt_frame'] = frame
            tmp_dict['IoU'] = score
            try:
                tmp_dict['color'] = frame.color_score
            except AttributeError:
                tmp_dict['color'] = "NA"
            crop_rgb = img_rgb[re_frame[1]:re_frame[3], re_frame[0]:re_frame[2]]
            hist_similarity = HistSimilarityScore(crop_rgb, template_rgb)
            tmp_dict['hist_similarity'] = hist_similarity
            results.append(tmp_dict)
        pd.DataFrame(results).to_csv("results.csv")



