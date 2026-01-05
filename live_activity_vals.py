from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_live_activity_vals(url):
    driver = webdriver.Chrome()

    driver.get(url)

    iframe_selector = "iframe[title='Live Location Counts - Bar Layout']"

    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, iframe_selector))
    )

    chart_div = driver.find_element(By.ID, "chartContainer")
    time.sleep(5)

    children = chart_div.find_elements(By.XPATH, "./*")

    vals = []
    for child in children:
        vals.append(float(child.find_element(By.TAG_NAME, "div").get_attribute("data-value"))/100)
    driver.quit()
    return vals
