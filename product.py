from smtplib import SMTP  # to send email notifications


class Product:
    def __init__(self, soup, url, recipients):
        # Product Codes:
        # 0 : new item
        # 1 : price drop
        # 2 : price increase
        # 3 : in stock -> out of stock
        # 4 : out of stock -> in stock
        # 5 : out of stock on first query

        self.URL = url
        self.title = soup.find(id="productTitle").get_text().strip().replace(u'\xa0', u' ')
        self.recipients = recipients  # destination address
        self.is_buyable = False  # is there a price on the page?
        print(self.title)

        self.price_label = soup.find(id="priceblock_ourprice")  # scrape the price
        if self.price_label is None:
            self.price_label = soup.find(class_="a-size-medium a-color-price offer-price a-text-normal")  # books
        if self.price_label is None:  # still can't find the price - probably out of stock
            self.price_label = "-"
            self.ship_label = "-"
            self.total_label = "NOT IN STOCK"
            print("Price Scraping Error: Out Of Stock\n")
            return
        else:
            self.price_label = self.price_label.get_text().replace(u'\xa0', u' ')
        self.is_buyable = True
        self.ship_label = soup.find(class_="a-size-small a-color-secondary shipping3P")  # get shipping price

        if self.ship_label is None or "FREE" in self.ship_label.get_text().replace(u'\xa0', u' '):
            self.ship_label = "FREE"  # no shipping charge found - assume free
        else:
            self.ship_label = " ".join(self.ship_label.get_text().split()[-3:-1]).replace(u'\xa0', u' ')

        self.price = float(self.price_label.split()[-1])  # store price as float
        self.ship = 0 if self.ship_label == "FREE" else float(self.ship_label.split()[-1]) # store ship price as float
        self.total_price = self.price + self.ship  # store total price as float
        self.total_label = "{} {:.2f}".format(self.price_label.split()[0], self.total_price).replace(u'\xa0', u' ')
        # store total price label - (eg. "CDN$ 25.39")

        print("Total Price: " + self.total_label + "\n")

    def send_email(self, code, prev_labels=[]):
        if code == 0:
            subject = "New Amazon Product Being Tracked"
            body = '"{}" is now being tracked for price and availability changes.\n\nCurrent Product Price: {}\nCurrent Shipping Price: {}\nCurrent Total Price: {}\n\nProduct Link: {}'.format(
                self.title, self.price_label, self.ship_label, self.total_label, self.URL
            )
        elif code == 1:
            subject = "Price Drop Notification! - {}".format(self.title)
            body = "{}\n\nOld Product Price: {}\nOld Shipping Price: {}\nOld Total Price: {}\n\nNew Product Price: {}\nNew Shipping Price: {}\nNew Total Price: {}\n\nProduct Link: {}".format(
                self.title, *(prev_labels[:3]), self.price_label, self.ship_label, self.total_label, self.URL
            )
        elif code == 2:
            subject = "Price Increase Notification! - {}".format(self.title)
            body = "{}\n\nOld Product Price: {}\nOld Shipping Price: {}\nOld Total Price: {}\n\nNew Product Price: {}\nNew Shipping Price: {}\nNew Total Price: {}\n\nProduct Link: {}".format(
                self.title, *(prev_labels[:3]), self.price_label, self.ship_label, self.total_label, self.URL
            )
        elif code == 3:
            subject = 'Item Out of Stock - {}'.format(self.title)
            body = '"{}" is now unavailable for purchase.\n\nProduct Link: {}'.format(
                self.title, self.URL
            )
        elif code == 4:
            subject = "Item Back in Stock! - {}".format(self.title)
            body = '"{}" is now available for purchase.\n\nCurrent Product Price: {}\nCurrent Shipping Price: {}\nCurrent Total Price: {}\n\nProduct Link: {}'.format(
                self.title, self.price_label, self.ship_label, self.total_label, self.URL
            )
        elif code == 5:
            subject = 'Item Out of Stock - {}'.format(self.title)
            body = '"{}" is unfortunately unavailable for purchase.\n\nProduct Link: {}'.format(
                self.title, self.URL
            )

        message = "Subject: {}\n\n{}".format(subject, body).replace(u'\xa0', u' ')
        message = message.replace(u'\uff08', ' (')
        message = message.replace(u'\uff09', ') ')

        server = SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()

        #  replace these with valid gmail address and corresponding app password
        #  to configure, go to myaccounts.google.com/apppasswords
        server.login("validemailaddress", "app-password")

        for destination in self.recipients:
            server.sendmail(
                from_addr="Amazon Price Tracker",
                to_addrs=destination,
                msg=message
            )

        server.quit()
