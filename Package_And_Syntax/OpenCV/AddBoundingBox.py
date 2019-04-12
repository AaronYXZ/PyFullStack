import cv2
import yaml

img = cv2.imread("resources/account001.png")
print(img.shape)

def getMatch(matches_yml):
    with open(matches_yml) as tmp:
        tmpDict = yaml.load(tmp)
    matched_lst = tmpDict['matches']
    m = [ [(int(x['left']), int(x['top'])), (int(x['right']), int(x['bottom']))] for x in matched_lst]
    return m



if __name__ == '__main__':
    img = cv2.imread("resources/account001.png")
    m = getMatch("resources/account001.yml")
    color = (0,255,0)
    thickness = 4
    for cor in m:
        cv2.rectangle(img, cor[0], cor[1], color, thickness=thickness)
    cv2.imwrite("resources/account001_marked.png", img)
