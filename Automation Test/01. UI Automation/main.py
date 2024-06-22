import requests
from xml.etree import ElementTree
import os
from datetime import datetime
from selenium import webdriver
import time
import pyautogui
import cv2
import numpy as np
import platform


def get_urls_from_sitemap(sitemap_url, limit=5):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(sitemap_url, headers=headers)
    
    print(f"HTTP Status Code: {response.status_code}")
    if response.status_code != 200:
        print(f"Failed to retrieve sitemap: HTTP {response.status_code}")
        return []
    
    response_content = response.content.decode('utf-8')  
    print(f"Response Content:\n{response_content[:500]}")  
    
    try:
        
        namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        sitemap = ElementTree.fromstring(response_content)
        urls = [url.text for url in sitemap.findall(".//ns:loc", namespaces)]
        urls = urls[:limit]  
    except ElementTree.ParseError as e:
        print(f"Error parsing XML: {e}")
        urls = []
    return urls

sitemap_url = "https://www.getcalley.com/page-sitemap.xml"
urls = get_urls_from_sitemap(sitemap_url)
print(urls)  


resolutions = {
    'Desktop': [
        (1920, 1080),
        (1366, 768),
        (1536, 864),
    ],
    'Mobile': [
        (360, 640),
        (414, 896),
        (375, 667),
    ]
}


if platform.system() == 'Darwin':  
    browsers = ['chrome', 'firefox', 'safari']
else:
    browsers = ['chrome', 'firefox']


def create_folder_structure():
    base_dir = "screenshots"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    for browser in browsers:
        browser_dir = os.path.join(base_dir, browser)
        if not os.path.exists(browser_dir):
            os.makedirs(browser_dir)
        for device, res_list in resolutions.items():
            device_dir = os.path.join(browser_dir, device)
            if not os.path.exists(device_dir):
                os.makedirs(device_dir)
            for res in res_list:
                res_dir = os.path.join(device_dir, f"{res[0]}x{res[1]}")
                if not os.path.exists(res_dir):
                    os.makedirs(res_dir)
    return base_dir

base_dir = create_folder_structure()


def start_recording():
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('test_run.avi', fourcc, 20.0, (1920,1080))
    return out

def record_frame(out):
    img = pyautogui.screenshot()
    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    out.write(frame)

def stop_recording(out):
    out.release()


def get_driver(browser_name):
    if browser_name == 'chrome':
        return webdriver.Chrome()  
    elif browser_name == 'firefox':
        return webdriver.Firefox()  
    elif browser_name == 'safari' and platform.system() == 'Darwin':
        return webdriver.Safari()

def capture_screenshot(driver, url, save_path):
    driver.get(url)
    time.sleep(3)  
    driver.save_screenshot(save_path)

def run_tests(urls, base_dir):
    out = start_recording()
    for browser in browsers:
        driver = get_driver(browser)
        for device, res_list in resolutions.items():
            for res in res_list:
                driver.set_window_size(res[0], res[1])
                for url in urls:
                    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    filename = f"screenshot-{timestamp}.png"
                    save_path = os.path.join(base_dir, browser, device, f"{res[0]}x{res[1]}", filename)
                    capture_screenshot(driver, url, save_path)
                    record_frame(out)
        driver.quit()
    stop_recording(out)

if urls:
    run_tests(urls, base_dir)
else:
    print("No URLs to test.")
