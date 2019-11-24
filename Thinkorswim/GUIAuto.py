import csv
import time
import pyautogui


with open('tradelog.csv','a', newline='') as newFile:
    newFileWriter = csv.writer(newFile)
    for i in range(10):
        newFileWriter.writerow([i])