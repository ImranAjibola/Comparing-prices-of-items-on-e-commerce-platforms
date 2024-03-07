from bs4 import BeautifulSoup
import requests

search = input('What product price do you want to check for? ')
search = search.replace(' ', '+')
URL = f'https://www.jumia.com.ng/catalog/?q={search}'


response = requests.get(URL)
website_html = response.text

soup = BeautifulSoup(website_html, 'html.parser')

all_prices = soup.find_all(name='div', class_ = 'prc')
price_titles = [price.getText() for price in all_prices]
price_titles = [element for element in price_titles if element != ""]

for i in range(len(price_titles)):
    if "-" in price_titles[i]:
        price_range = price_titles[i].split("-")
        part1 = price_range[0].strip()
        part2 = price_range[1].strip()
        price_titles[i] = part2


# for tag in links:
#     print(tag.get('href'))

# print(len(price_titles))

all_products = soup.find_all(name='h3', class_ = 'name')
product_titles = [product.getText() for product in all_products]

links = soup.find_all(name='a', class_ ='core')
hyper_link = [hyper.get('href') for hyper in links]
# print(product_titles)

result = []
for product, price,hyper in zip(product_titles, price_titles,hyper_link):
    line = product + " - " + price  + " - " + 'https://www.jumia.com.ng/' + hyper
    result.append(line) 

with open('jumia.txt', mode='w', encoding="utf-8") as file:
    for result in result:
        file.write(f'{result}\n')