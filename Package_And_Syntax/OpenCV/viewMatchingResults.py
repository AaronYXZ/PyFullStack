import numpy as np
import os
import fnmatch
import cv2
from Helper.Util import annotate, crop


if __name__ == '__main__':
    pathImg = "/Users/aaronyu/Desktop/Project14_Image/surface-based-samples/other/canvas"
    pathTemplate = "/Users/aaronyu/Desktop/Project14_Image/surface-based-samples/other/fragment"
    color = (0,255, 0)
    thickness = 4
    imgFiles = fnmatch.filter(os.listdir(pathImg), "*.png")
    # ymlFiles = fnmatch.filter(os.listdir(pathImg), "*.yml")
    imgFiles = sorted(imgFiles)
    for img in imgFiles:
        imgFile = os.path.join(pathImg, img)
        ymlFile = os.path.join(pathImg, img.replace("png", "yml"))
        templateFile = os.path.join(pathTemplate, img)

        annotate(imgFile, ymlFile, color, thickness)

        crop(imgFile, templateFile, color, thickness)

