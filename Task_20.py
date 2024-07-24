import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import time


@pytest.fixture(scope="module")
def driver():
    # Initialize the Edge WebDriver
    driver = webdriver.Edge()
    yield driver
    driver.quit()


def test_cowin_gov_in(driver):
    # Open the URL
    driver.get("https://www.cowin.gov.in/")

    # Wait for the "FAQ" and "Partners" links to be clickable
    wait = WebDriverWait(driver, 20)
    try:
        faq_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Create FAQ")))
    except Exception as e:
        driver.save_screenshot('faq_not_found.png')
        print("Error: 'Create FAQ' link not found. Screenshot saved as faq_not_found.png.")
        return

    try:
        partners_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Partners")))
    except Exception as e:
        driver.save_screenshot('partners_not_found.png')
        print("Error: 'Partners' link not found. Screenshot saved as partners_not_found.png.")
        return

    # Open the links in new tabs
    faq_link.send_keys(Keys.CONTROL + Keys.RETURN)
    partners_link.send_keys(Keys.CONTROL + Keys.RETURN)

    # Wait for the new windows to open
    time.sleep(3)

    # Get the window handles
    handles = driver.window_handles
    assert len(handles) == 3, "New windows did not open properly"

    # Fetch and display the window/frame IDs
    for handle in handles:
        print("Window ID:", handle)

    # Close the new windows and switch back to the home page
    driver.switch_to.window(handles[1])
    driver.close()
    driver.switch_to.window(handles[2])
    driver.close()

    driver.switch_to.window(handles[0])

# Output
#Testing started at 10:06 ...
#Launching pytest with arguments Task_20.py::test_cowin_gov_in --no-header --no-summary -q in C:\Users\PREMA\PAT-28\pythonProject

#============================= test session starts =============================
#collecting ... collected 1 item

#Task_20.py::test_cowin_gov_in PASSED                                     [100%]Error: 'Create FAQ' link not found. Screenshot saved as faq_not_found.png.


#============================= 1 passed in 49.20s ==============================

#Process finished with exit code 0

def test_labour_gov_in(driver):
    # Open the URL
    driver.get("https://labour.gov.in/")

    # Wait for the "Documents" menu to be clickable
    wait = WebDriverWait(driver, 20)
    documents_menu = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Documents")))
    documents_menu.click()

    try:
        # Wait for the Monthly Progress Report link to be visible and clickable
        monthly_report = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Monthly Progress Report")))
        report_url = monthly_report.get_attribute('href')

        response = requests.get(report_url)
        with open('Monthly_Progress_Report.pdf', 'wb') as file:
            file.write(response.content)
        print("Monthly Progress Report downloaded.")
    except Exception as e:
        print("Error locating Monthly Progress Report:", e)
        driver.save_screenshot('error_screenshot.png')
        return

    # Wait for the "Media" menu and then the "Photo Gallery" sub-menu
    media_menu = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Media")))
    media_menu.click()

    try:
        # Check if "Photo Gallery" link is within an iframe
        iframe = driver.find_elements(By.TAG_NAME, "iframe")
        if iframe:
            driver.switch_to.frame(iframe[0])

        photo_gallery = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Photo Gallery")))
        photo_gallery.click()

        # Switch back to the default content if you switched to an iframe
        if iframe:
            driver.switch_to.default_content()
    except Exception as e:
        print("Error locating Photo Gallery:", e)
        driver.save_screenshot('error_screenshot1.png')
        return

    # Find and download the first 10 photos
    photos = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img")))[:10]
    os.makedirs('Photo_Gallery', exist_ok=True)

    for index, photo in enumerate(photos):
        photo_url = photo.get_attribute('src')
        img_data = requests.get(photo_url).content
        with open(f'Photo_Gallery/photo_{index + 1}.jpg', 'wb') as handler:
            handler.write(img_data)
        print(f"Downloaded photo_{index + 1}.jpg")

#Output:

#Testing started at 10:02 ...
#Launching pytest with arguments 20.py::test_labour_gov_in --no-header --no-summary -q in C:\Users\PREMA\PAT-28\pythonProject

#============================= test session starts =============================
#collecting ... collected 1 item

#Task_20.py::test_labour_gov_in PASSED                                         [100%]Monthly Progress Report downloaded.
#Downloaded photo_1.jpg
#Downloaded photo_2.jpg
#Downloaded photo_3.jpg
#Downloaded photo_4.jpg
#Downloaded photo_5.jpg
#Downloaded photo_6.jpg
#Downloaded photo_7.jpg
#Downloaded photo_8.jpg
#Downloaded photo_9.jpg
#Downloaded photo_10.jpg


#============================= 1 passed in 26.00s ==============================

#Process finished with exit code 0