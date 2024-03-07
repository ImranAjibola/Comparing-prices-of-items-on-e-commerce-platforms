# from bs4 import BeautifulSoup
# import requests

# response = requests.get('https://www.jumia.com.ng/catalog/?q=iphone')
# webpage = response.text

# soup = BeautifulSoup(webpage, 'html.parser')
# # print(soup)
# links= soup.find_all(name='a', class_ ='core')
# for tag in links:
#     print(tag.get('href'))
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

li_element = driver.find_element(By.CLASS_NAME,"bbe45_3oExY")

# Find the <a> tag within the <li> element
a_tag = li_element.find_element(By.TAG_NAME,"a")

# Get the href attribute of the <a> tag
href_value = a_tag.get_attribute("href")

# Print the href attribute
print(href_value)

# Close the webdriver
driver.quit()
