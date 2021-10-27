import pytesseract
from PIL import Image
import cv2
import math
import config
import os


pytesseract.pytesseract.tesseract_cmd = config.tesseract_path

class Character:
    def __init__(self):
        self.left_col = None
        self.right_col = None


def solve_captcha(unsolved_img):
    image = cv2.imread(unsolved_img,0)
    ret, image = cv2.threshold(image, 60, 255, cv2.THRESH_BINARY)
    
    rows, cols = image.shape
    mark = []
    #removes stray pixel from selenium screencap
    image[0, :] = image[1, :]
    #loops through image column by column 
    #adds all column indices with >0 black pixels
    for i in range(cols):
        for j in range(rows):
            if (image[j][i] == 0):
                mark.append(i)
                break
    characters = []
    start = mark[0]
    for i in range (0, len(mark) - 1):
        if mark[i] != mark[i + 1] - 1:
            temp = Character()
            temp.left_col = start
            temp.right_col = mark[i]
            characters.append(temp)
            start = mark[i + 1]
        elif i + 1 == len(mark) - 1:
            temp = Character()
            temp.left_col = start
            temp.right_col = mark[i + 1]
            characters.append(temp)
            start = None

    i = 0
    j = len(characters) - 1

    left_index = 5
    right_index = cols - 18
    for k in range(characters[i].left_col, characters[i].right_col + 1):
        image[:, left_index] = image[:, k]
        image[:, k] = 255
        left_index += 1
    left_index += 1
    left_index = math.floor((characters[i + 1].left_col + left_index) / 2)
    for k in range(characters[j].right_col, characters[j].left_col - 1, -1):
        image[:, right_index] = image[:, k]
        image[:, k] = 255
        right_index -= 1
    right_index -= 1
    right_index = math.floor((characters[j - 1].right_col + right_index) / 2)
    i += 1
    j -= 1
    for k in range(characters[i].left_col, characters[i].right_col + 1):
        image[:, left_index] = image[:, k]
        image[:, k] = 255
        left_index += 1
    left_index += 1
    i += 1
    j -= 1
    for k in range(characters[j].right_col, characters[j].left_col - 1, -1):
        image[:, right_index] = image[:, k]
        image[:, k] = 255
        right_index -= 1

    cv2.imwrite("copy.png", image)
    captcha = pytesseract.image_to_string(Image.open("copy.png"), lang='eng', config='--psm 7 --oem 1 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    os.remove("copy.png")
    
    captcha = captcha.replace(" ", "")
    captcha = captcha[0:5]
    return captcha

def main():
    while True:
        file_name = input("Enter file name or enter 'q' to quit: ")
        if (file_name == 'q'):
            return 0
        answer = solve_captcha(file_name)
        print(answer)

if __name__ == "__main__":
    main()