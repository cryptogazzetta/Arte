from selenium import webdriver
from selenium.webdriver.common.by import By

url = 'https://www.artsy.net/artist/victor-vasarely/auction-results?hide_upcoming=false&allow_empty_created_dates=true&currency=&include_estimate_range=false&include_unknown_prices=true&allow_unspecified_sale_dates=true'

driver = webdriver.Chrome()
driver.get(url)

login_button = driver.find_element(By.XPATH, '//button[@class="Button__Container-sc-1bhxy1c-0 ittcNr"]')
login_button.click()

email = 'gazzetta.art@gmail.com'
password = 'Senha123'

email_field = driver.find_element(By.XPATH, '//input[@name="email"]')
email_field.send_keys(email)
password_field = driver.find_element(By.XPATH, '//input[@name="password"]')
password_field.send_keys(password)

submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

import time

time.sleep(2)