import requests
import pickle  # to store hash-maps for future executions
from bs4 import BeautifulSoup  # for html parsing/scraping
from product import Product

url_lines = [line.rstrip('\n') for line in open("URL_list.txt")]
address_lines = [line.rstrip('\n') for line in open("address_book.txt")]

settings = [line.rstrip('\n') for line in open("config.ini")]

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) "
                         + "Chrome/76.0.3809.100 Safari/537.36"}

send_keys = {}  # hash map for recipients' email addresses

for line in address_lines:
    key, address = line.split(" ")
    send_keys[key] = address

thresh_dec = float(settings[1].split("=")[1])/100  # % of price decrease that will trigger an email notification
thresh_inc = float(settings[0].split("=")[1])/100  # % of price increase that will trigger an email notification

try:
    product_price_data = pickle.load(open("item_price_data.pickle", "rb"))
except FileNotFoundError:
    product_price_data = {}  # {item_name : [last_price_label, last_ship_label, last_total_label, was_buyable]}

for line in url_lines:
    URL, k = line.split(" ")
    recipients = [send_keys[c] for c in k]
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    if soup.find(id="productTitle") is None:  # bad page, skip
        continue
    product = Product(soup, URL, recipients)  # initialize product

    if product.title not in product_price_data:  # first time seeing product
        product.send_email(0)  # send notification that product is now being tracked
        if not product.is_buyable:
            product.send_email(5)  # item is starting out as unavailable
    else:  # we have seen product before
        prev_data = product_price_data[product.title]  # look-up previous price
        if not product.is_buyable:
            if prev_data[3]:  # product was buyable but now it isn't
                product.send_email(3)
            continue

        elif not prev_data[3]:  # product wasn't available but now it is
            product.send_email(4)
        prev_total_price = float(prev_data[2].split()[-1])  # get previous price as float

        if (prev_total_price - product.total_price)/prev_total_price > 1 + thresh_dec:  # price drop
            product.send_email(1, prev_data)

        elif (product.total_price - prev_total_price)/product.total_price > 1 + thresh_inc:  # price increase
            product.send_email(2, prev_data)

    product_price_data[product.title] = [
        product.price_label, product.ship_label, product.total_label, product.is_buyable
    ]

out = open("item_price_data.pickle", "wb")
pickle.dump(product_price_data, out)  # export price data hash-map as pickle
out.close()
