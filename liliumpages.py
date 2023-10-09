import requests
from bs4 import BeautifulSoup
import pandas as pd

# Initialize empty lists to store data
persiannames = []
englishnames = []
ratings = []
currentprices = []
oldprices = []

# Loop through multiple pages
base_url = "https://liliome.ir/brand/perfume/dior/page/{}"
page_number = 1

while True:
    url_site = base_url.format(page_number)
    site = requests.get(url_site)
    if site.status_code != 200:
        break  # Stop if the page doesn't exist or you've reached the end

    soup = BeautifulSoup(site.text, 'html.parser')
    div1 = soup.find('div', {'class': 'products'})
    div2 = div1.find_all('div', {'class': 'box-text box-text-products text-center grid-style-2'})

    for item in range(len(div2)):
        product_title = div2[item].find('p', {'class': 'name product-title woocommerce-loop-product__title'})
        if product_title:
            persianname, englishname = product_title.text.split(' | ')
            persiannames.append(persianname)
            englishnames.append(englishname)

        rating_element = div2[item].find('strong', {'class': 'rating'})
        if rating_element:
            rating = rating_element.text
            ratings.append(rating)
        else:
            ratings.append(None)

        currentprice_element = div2[item].find('ins')
        if currentprice_element:
            currentprice = currentprice_element.text
            currentprice = int(currentprice.replace(',', '').replace('تومان', ''))
            currentprices.append(currentprice)
        else:
            currentprices.append(None)

        oldprice_element = div2[item].find('del')
        if oldprice_element:
            oldprice = oldprice_element.text
            oldprice = int(oldprice.replace(',', '').replace('تومان', ''))
            oldprices.append(oldprice)
        else:
            oldprices.append(None)

    page_number += 1

# Create a DataFrame
liliumDictionary = {
    'persianname': persiannames,
    'englishname': englishnames,
    'rating': ratings,
    'currentprice': currentprices,
    'oldprice': oldprices
}

df = pd.DataFrame(liliumDictionary)

# Save the data to a CSV file
df.to_csv('liliumDictionary.csv', index=False)
