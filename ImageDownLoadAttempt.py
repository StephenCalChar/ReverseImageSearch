import urllib
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json
import glob
import os
import shutil





numberOfDownLoadsPerDoc = 100

#Load each image from this directory
dfPath = ''
#Save to this directory. Each img duplicate in separate folder.
dfPathTwo = ''
searchUrl = 'http://www.google.hr/searchbyimage/upload'
searchedFileFolder = 'searchedFileFolder'


file_list = glob.glob(os.path.join(os.getcwd(), dfPath, "*.png"))


for file in file_list:

    browser = webdriver.Firefox(executable_path='/home/stephen2/Documents/geckodriver')
    time.sleep(15)
    browser.get('https://www.google.co.uk/imghp')

    # Click "Search by image" icon
    elem = browser.find_element_by_class_name('gsst_a')
    elem.click()

    # Switch from "Paste image URL" to "Upload an image"
    browser.execute_script("google.qb.ti(true);return false")
    # Set the path of the local file and submit
    time.sleep(3)
    ele0 = browser.find_element_by_id("qbfile")
    ele0.send_keys(file)

    time.sleep(25)

    #  Clicking 'Visually Similar Images'
    ele1 = browser.find_element_by_link_text("Visually similar images")
    ele1.click()

    currentUrl = str(browser.current_url)
    browser.quit()

    driver = webdriver.Firefox(executable_path='/home/stephen2/Documents/geckodriver')
    driver.get(currentUrl)

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    #print soup
    driver.quit()

    newFolder = file.split('/')[-1]
    newFolder = newFolder.split('.')[0]
    ##Create new Folder here
    os.chdir(dfPathTwo)
    newPath = dfPathTwo + '/' + newFolder
    os.makedirs(newPath)
    masterFileFolder = newPath + '/' + searchedFileFolder
    os.makedirs(masterFileFolder)
    #copies the searched file into its own folder along with its googled images
    shutil.copy(file, masterFileFolder)




    foundImages =[]
    for a in soup.find_all("div", {"class": "rg_meta"}):
        link, Type = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
        foundImages.append((link, Type))


    for image in foundImages[:numberOfDownLoadsPerDoc+1]:
        link = image[0]
        fileName = link.split('/')[-1]
        savePath = newPath + "/" + fileName[:5]
        try:
            urllib.urlretrieve(link, savePath)
        except:
            pass
        time.sleep(2)




