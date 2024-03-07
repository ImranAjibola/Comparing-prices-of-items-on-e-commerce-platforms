from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.EdgeOptions()
options.add_argument("-headless")

driver = webdriver.Edge(options=options)

search = input('What product price do you want to check for? ')
search = search.replace(' ', '%20')
driver.get(f"https://www.konga.com/search?search={search}")

prices = WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'd7c0f_sJAqi')))
names = WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'af885_1iPzH')))


# links = WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, '_4941f_1HCZm')))
# button.get_attribute("href")
# for link in links:
#     href = link.get_attribute("href")
# links = [link.__getattribute__("href") for link in links]

result = []
for name, price in zip(names, prices):
    line = name.text + " - " + price.text
    result.append(line)

with open('konga.txt', mode='w', encoding="utf-8") as file:
    for result in result:
        file.write(f'{result}\n')

driver.quit()