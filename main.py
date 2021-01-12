from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,InvalidArgumentException
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
from selenium.webdriver.common.keys import Keys
import os
import sys
import time
import zipfile


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
        time.sleep(1)
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

def create_pdf(tmp_path,filename):
    pdf_path = tmp_path + '/pdfs'
    zip_path = tmp_path + '/zips'
    files_path = tmp_path + '/files'

    cur_zip = zipfile.ZipFile(zip_path + '/' + filename)
    cur_zip.extractall(files_path)
    cur_zip.close()

    #Возможно стоит добавить какое-то разделеие на главы и мусор, но пока в порядке в котором упаковал переводчик 
    file_names = os.listdir(files_path)
    for i in range(len(file_names)):
        os.rename(files_path + '/' + file_names[i],files_path+ '/' + str(i) + file_names[i].strip('.')[-1])
    file_names = os.listdir(files_path)

    



if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Write URL to argulent")
        exit()
    LOGIN = sys.argv[1]
    PASSWORD = sys.argv[2]
    URL = sys.argv[3]
    tmp_path = os.getcwd()+'/tmp'

    pdf_path = tmp_path + '/pdfs'
    zip_path = tmp_path + '/zips'
    if not os.path.exists(tmp_path):
        os.mkdir(tmp_path)
    
    if not os.path.exists(pdf_path):
        os.mkdir(pdf_path)

    if not os.path.exists(zip_path):
        os.mkdir(zip_path)

    op = webdriver.ChromeOptions()
    #op.add_argument('headless')
    op.add_experimental_option('prefs',  {
    "download.default_directory": zip_path,
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
    time.sleep(4)
    driver.close()

    zips_names = os.listdir(zip_path)
    for i in range(len(zips_names)):
        os.rename(zip_path + '/' + zips_names[i],zip_path + '/' + str(i) + '.zip')

    zips_names = os.listdir(zip_path)

    files_path = tmp_path + '/files'
    if not os.path.exists(files_path):
        os.mkdir(files_path)


