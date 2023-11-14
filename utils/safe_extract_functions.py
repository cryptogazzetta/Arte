from selenium.webdriver.common.by import By

## Utils
def safe_extract(driver, xpath):
    try:
        element = driver.find_element(By.XPATH, xpath)
        return element
    except:
        print('Error extracting element with xpath: ' + xpath)
        return None
    
def safe_extract_multiple(driver, xpath):
    try:
        elements = driver.find_elements(By.XPATH, xpath)
        return elements
    except:
        print('Error extracting elements with xpath: ' + xpath)
        return None