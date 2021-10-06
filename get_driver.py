import os
import platform
from selenium import webdriver

def get_driver():
    driver_path_list = {
        'darwin':'driver/mac/chromedriver',
        'linux':'driver/linux/chromedriver',
        'windows':'driver/win/chromedriver.exe',
    }
    driver_path = driver_path_list.get(platform.system().lower())
    return webdriver.Chrome(os.path.join(os.getcwd(), driver_path))

if __name__ == '__main__':
    driver = get_driver()
