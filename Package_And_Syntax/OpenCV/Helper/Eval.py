import os
import numpy as np

def IoU(re_frame, gt_frame):
    """

    :param obj1: Ground Truth, a GTFrame object
    :param obj2: Detection Result, [left, top, right, bottom]
    :return: Score
    """
    x1 = re_frame[0]
    y1 = re_frame[1]
    width1 = re_frame[2] - re_frame[0]
    height1 = re_frame[3] - re_frame[1]

    x2 = gt_frame.left
    y2 = gt_frame.top
    width2 = gt_frame.right - gt_frame.left
    height2 = gt_frame.bottom - gt_frame.top

    endx = max(x1+width1,x2+width2)
    startx = min(x1,x2)
    width = width1+width2-(endx-startx)

    endy = max(y1+height1,y2+height2)
    starty = min(y1,y2)
    height = height1+height2-(endy-starty)

    if width <=0 or height <= 0:
        ratio = 0 # 重叠率为 0
    else:
        Area = width*height # 两矩形相交面积
        Area1 = width1*height1
        Area2 = width2*height2
        ratio = Area*1./(Area1+Area2-Area)
    # return IOU
    return float(ratio)

# def get