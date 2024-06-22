import time
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pyautogui
from PIL import ImageGrab
import threading
import cv2


def screen_record(filename="output.avi"):
    screen_size = pyautogui.size()
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(filename, fourcc, 20.0, (screen_size.width, screen_size.height))

    while recording:
        img = ImageGrab.grab()
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
        out.write(frame)
        time.sleep(0.05)

    out.release()


recording = True
record_thread = threading.Thread(target=screen_record)
record_thread.start()


driver = webdriver.Chrome()
driver.maximize_window()


driver.get("https://demo.dealsdray.com/")


time.sleep(3)  
driver.find_element(By.NAME, "username").send_keys("prexo.mis@dealsdray.com")  
driver.find_element(By.NAME, "password").send_keys("prexo.mis@dealsdray.com")  
driver.find_element(By.XPATH, "//button[contains(text(),'Login')]").click()  

time.sleep(5)  
driver.find_element(By.XPATH, "//input[@type='file']").send_keys("D:\\Work\\Function automation\\demo-data.xlsx")  
driver.find_element(By.XPATH, "//button[contains(text(),'Upload')]").click()  

time.sleep(10)  


final_output = driver.find_element(By.TAG_NAME, "body")  
final_output.screenshot("final_output.png")


recording = False
record_thread.join()


driver.quit()


