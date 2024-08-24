from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import time
from utils.data import *

def scrape_products():
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome()
    driver.get(WEB) 
    wait = WebDriverWait(driver, 10)
    
    # Scroll down and wait for all elements to load
    driver.execute_script("document.body.style.webkitTransform='scale(0.1)';")
    driver.execute_script("document.body.style.webkitTransformOrigin='left top'; ")
    ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
    time.sleep(3)
    # wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, ALL_PRODUCT)))
    
    # Product List all Products
    grid_element = driver.find_element(By.CLASS_NAME, ALL_PRODUCT)

    # Product Item Wrapper
    product_elements = grid_element.find_elements(By.CLASS_NAME, PRODUCT_LIST)
    
    # Product Link
    links = [product_element.find_element(By.XPATH, PRODUCT_LINK).get_attribute('href')
             for product_element in product_elements]
    
    df = pd.DataFrame(columns=['name', 'id','size', 'weight', 
                               'model', 'price', 'unit', 'promotion',
                               'detail'
                               ])
    
    for link in links:
        # new instance
        driver.get(str(link))

        # image_element = driver.find_element(By.XPATH, PRODUCT_IMAGE)
        # except_element = driver.find_element(By.XPATH, EXCEPT_PRODCUT_IMAGE)
        # image_element = image_element if image_element.is_displayed() else except_element
        # p_img = image_element.get_attribute("src")

        # Get all data
        # p_img = None
        p_name = driver.find_element(By.XPATH, PRODUCT_NAME).text
        p_id = driver.find_element(By.XPATH, PRODUCT_ID).text
        p_size = driver.find_element(By.XPATH, PRODUCT_SIZE).text
        p_weight = driver.find_element(By.XPATH, PRODUCT_WEIGHT).text
        p_price = driver.find_element(By.XPATH, PRODUCT_PRICE).text
        p_unit = driver.find_element(By.CLASS_NAME, PRODUCT_PRICE_UNIT).text
        p_promo = [p.text for p in driver.find_elements(By.CSS_SELECTOR, PRODUCT_PROMOTIONS)]
        p_model = next((word for word in PRODUCT_MODEL if word in p_name), 'อื่นๆ ')
            
        
        # Set Window to 50% and wait for all elements to load
        driver.execute_script("document.body.style.webkitTransform='scale(0.5)';")
        driver.execute_script("document.body.style.webkitTransformOrigin='left top'; ")
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, SEE_MORE_BUTTON))).click()
        
        # driver.find_elements(By.CSS_SELECTOR, MANUAL_TAB)                
        p_detail = [d.text for d in driver.find_elements(By.CSS_SELECTOR, PRODUCT_DETAILS)]
        p_manual = [m.text for m in driver.find_elements(By.CLASS_NAME, PRODUCT_MANUAL)
                   ] if (wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, MANUAL_TAB))).click()
                   )else []
        
        # p_manual = element_click(driver, wait)
        # print(p_model)
        
        # Save to dataframe
        df.loc[len(df)] = [p_name, p_id, p_size, p_weight, p_model, 
                           p_price, p_unit, p_promo, p_detail]

    # df.to_excel('products_test_detail.xlsx', index=False)
    driver.quit()

def element_click(driver, wait):
    manual_tab = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, MANUAL_TAB)))
    if manual_tab:
        manual_tab.click()
        p_manual = [m.text for m in driver.find_elements(By.CLASS_NAME, PRODUCT_MANUAL)]
    else:
        p_manual = []
    return p_manual

if __name__ == "__main__":
    scrape_products()
