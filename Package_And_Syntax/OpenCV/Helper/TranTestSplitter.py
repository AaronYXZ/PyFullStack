import os
import fnmatch
import shutil
from sklearn.model_selection import train_test_split
import random

imgPath = "/Users/aaronyu/Desktop/Project14_Image/surface-based-samples/other/canvas"
templatePath = "/Users/aaronyu/Desktop/Project14_Image/surface-based-samples/other/fragment"
allPath = "/Users/aaronyu/Desktop/Project14_Image/WorkSpace/All"
trainPath = "/Users/aaronyu/Desktop/Project14_Image/WorkSpace/Train"
testPath = "/Users/aaronyu/Desktop/Project14_Image/WorkSpace/Test"



def createAll(imgPath, templatePath, allPath):
    """

    :param imgPath: Path containing all images (canvas to be searched on)
    :param templatePath: Path containing all template (to be searched for in canvas)
    :param allPath: Path for image, yml, template
    :return: 3 folders under allPath, image, yml, template respectively
    """

    allImgPath = os.path.join(allPath, "img")
    allTemplatePath = os.path.join(allPath, "template")
    allYmlPath = os.path.join(allPath, "yml")
    if not os.path.exists(allImgPath):
        os.makedirs(allImgPath)
    if not os.path.exists(allTemplatePath):
        os.makedirs(allTemplatePath)
    if not os.path.exists(allYmlPath):
        os.makedirs(allYmlPath)

    imgFiles = fnmatch.filter(os.listdir(imgPath), "*.png")
    for img in imgFiles:
        imgFile = os.path.join(imgPath, img)
        ymlFile = os.path.join(imgPath, img.replace("png", "yml"))
        templateFile = os.path.join(templatePath, img)
        if not os.path.isfile(ymlFile):
            continue
        if not os.path.isfile(templateFile):
            continue
        shutil.copy(imgFile, allImgPath)
        shutil.copy(ymlFile, allYmlPath)
        shutil.copy(templateFile, allTemplatePath)

def createTrainTest(allPath, trainPath, testPath, testPerc = 0.2, seed = 2019):
    """

    :param allPath:
    :param trainPath:
    :param testPath:
    :return:
    """
    ## Create train/test path for each type - img, template, yml
    folders = ["img", "template", "yml"]
    for folder in folders:
        tmpTrainPath = os.path.join(trainPath, folder)
        if not os.path.exists(tmpTrainPath):
            os.makedirs(tmpTrainPath)
        tmpTestpath = os.path.join(testPath, folder)
        if not os.path.exists(tmpTestpath):
            os.makedirs(tmpTestpath)

    path1 = os.path.join(allPath, folders[0])
    imgFiles = fnmatch.filter(os.listdir(path1), "*.png")
    # path2 = os.path.join(all)
    totalSize = len(imgFiles)
    testSize = int(totalSize * testPerc)
    randomShuffler = random.Random(seed)
    randomShuffler.shuffle(imgFiles)

    ## Create Test
    for img in imgFiles[:testSize]:
        imgFile = os.path.join(allPath,folders[0], img)
        ymlFile = os.path.join(allPath,folders[2],  img.replace("png", "yml"))
        templateFile = os.path.join(allPath,folders[1], img)
        shutil.copy(imgFile, os.path.join(testPath, folders[0], img))
        shutil.copy(ymlFile, os.path.join(testPath, folders[2], img.replace("png", "yml")))
        shutil.copy(templateFile, os.path.join(testPath, folders[1], img))

    ## Create Train
    for img in imgFiles[testSize:]:
        imgFile = os.path.join(allPath,folders[0], img)
        ymlFile = os.path.join(allPath,folders[2],  img.replace("png", "yml"))
        templateFile = os.path.join(allPath,folders[1], img)
        shutil.copy(imgFile, os.path.join(trainPath, folders[0], img))
        shutil.copy(ymlFile, os.path.join(trainPath, folders[2], img.replace("png", "yml")))
        shutil.copy(templateFile, os.path.join(trainPath, folders[1], img))



if __name__ == '__main__':
    createAll(imgPath, templatePath, allPath)
    createTrainTest(allPath, trainPath, testPath)


