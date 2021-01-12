from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,InvalidArgumentException
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
from selenium.webdriver.common.keys import Keys
import sys
import time

#button button_icon reader-paginate__item reader-paginate__item_right reader-footer__btn
#fa-chevron-right
#reader-view__wrap
#button button_primary
def get_buttons(driver,url):
    try:
        driver.get(url)
    except InvalidArgumentException:
        print('Invalid URL')
        exit()
    return driver.find_elements_by_class_name('fa-cloud-download')

def logining(driver,url,login,password):
    try:
        driver.get(url)
        driver.find_element_by_class_name('header__sign-in').click()
        time.sleep(4)
        elem = driver.find_element_by_name("email")
        elem.click()
        elem.send_keys(login)
        elem = driver.find_element_by_name("password")
        elem.click()
        elem.send_keys(password)
        driver.find_element_by_class_name("button_md").click()
    except InvalidArgumentException:
        print('Invalid URL')
        exit()


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Write URL to argulent")
        exit()
    LOGIN = sys.argv[1]
    PASSWORD = sys.argv[2]
    URL = sys.argv[3]

    op = webdriver.ChromeOptions()
    #op.add_argument('headless')
    op.add_experimental_option('prefs',  {
    "download.default_directory": "/home/pavel/Projects/other/mangalib_parser/tmp",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    'profile.default_content_setting_values.automatic_downloads': 1})
    
    driver = webdriver.Chrome(options=op)
    logining(driver,URL,LOGIN,PASSWORD)
    buttons = get_buttons(driver,URL)
    size = len(buttons)
    for button in buttons:
        button.click()
        time.sleep(1)
    check = len(driver.find_elements_by_class_name('fa-check-circle'))
    while check != size:
        time.sleep(3)
        check = len(driver.find_elements_by_class_name('fa-check-circle'))

    time.sleep(30)
    driver.close()
