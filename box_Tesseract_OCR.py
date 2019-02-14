"""
Runs Tesseract OCR on box images (output of box_detection_user_friendly.py), then
 appends results so that all of a menu's data is together.
Author: Sebastian Brown (sebastian.brown80@gmail.com)
Last edited on 13 February 2019 by Sebastian Brown

Notes: Currently won't save OCRed text unless first character of text is a digit (date)
"""

from PIL import Image
import pytesseract
from os import chdir
import glob
import re


# Sorting function from https://stackoverflow.com/questions/2545532/python-analog-of-phps-natsort-function-sort-a-list-using-a-natural-order-alg
def natural_key(string_):
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]

# Tesseract executable location
pytesseract.pytesseract.tesseract_cmd = r'R:\JoePriceResearch\RA_work_folders\Merrill_Warnick\Tesseract-OCR\tesseract'

getfolder = r'R:\JoePriceResearch\RA_work_folders\Sebastian_Brown\GoodBoxes'
savingfolder = r'R:\JoePriceResearch\RA_work_folders\Sebastian_Brown\OCR_finished'
chdir(getfolder)


lastfile = ""
#../
for filename in sorted(glob.glob("*.png"), key=natural_key):
    chdir(getfolder)
    print(filename)
    #See if filename ends in .png
    #if re.search(".png$",filename) != None:
    
    #Recognize the image (should be a box)
    text = pytesseract.image_to_string(Image.open(filename))
    
    #The saving file name will be the original file name minus the last underscore and subsequent number (we'll append the cells together on each page)
    print(text)
    if text == '':
        print('Empty text box')  
    elif text[0].isdigit():
        savename = re.sub("_[0-9]+.png","",filename)
        print(savename)
    else:
        print('Text box doesn\'t start with date')
    
    #Check if the save file name begins with the same school district name as the last file -- if not, create a new file; otherwise, append onto it
    chdir(savingfolder)
    
    if re.sub("[_[0-9]+]+.png$","",savename) != re.sub("[_[0-9]+]+.png$","",lastfile):
    #if not path.isfile(savename + ".txt"):
        f = open(savename + ".txt", 'w')
    else:
        f = open(savename + ".txt", 'a')
    #Write or append recognized text onto file 
    f.write(text)
    f.write('\n')        
    f.close()
    lastfile = savename

