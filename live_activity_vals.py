from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.webdriver.chrome.options import Options

import time

def get_live_activity_vals(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") # For Chrome 109+
    chrome_options.add_argument("--disable-gpu") # Recommended for certain environments
    chrome_options.add_argument("--window-size=1920,1080") # Set a default window size

    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)

    iframe_selector = "iframe[title='Live Location Counts - Bar Layout']"

    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, iframe_selector))
    )

    chart_div = driver.find_element(By.ID, "chartContainer")
    time.sleep(5)

    children = chart_div.find_elements(By.XPATH, "./*")

    vals = []
    date0 = None
    for child in children:
        full_text = child.text

        if date0 is None:
            # Split the text by lines and look for the one starting with "Updated"
            lines = full_text.split('\n')
            updated_text = next((line.strip() for line in lines if "Updated:" in line), None)

            dt = updated_text.split("Updated: ")[1]
            date_obj = datetime.strptime(dt, "%m/%d/%Y %I:%M %p")
            date0 = date_obj
        vals.append(float(child.find_element(By.TAG_NAME, "div").get_attribute("data-value"))/100)
    driver.quit()
    return vals, date0
