# Amazon Price Tracker Tool

## About

This open-source utility is designed to monitor a user-defined set of Amazon products and send email notifications to the user concerning price and availability changes.

For ease of use, these ``.py`` scripts and assets can be hosted remotely (Google Cloud Platform, AWS, etc.) and scheduled via cron.

Scripts are written in Python, and make use of ``BeautifulSoup`` from the [*bs4*](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) package for scraping webpages. Emails are sent using [*smtplib*](https://docs.python.org/3/library/smtplib.html).

## Functionality

Settings for price increase/decrease notification thresholds can be configured in **config.ini**. For example, if you only wish to be notified for price drops greater than 5%, set ``percentage_decrease_notification_threshold=5``.

**URL_list.txt** contains the master list of all tracked products and corresponding destination email addresses. The usage of this file is best explained with an example:

![Example](https://scontent-yyz1-1.xx.fbcdn.net/v/t1.15752-9/69821029_386275908743433_5917483190263480320_n.png?_nc_cat=109&_nc_oc=AQk30XcJKwY9UWK9HTIQOOzozFAmv3bv1AE5-deYJT_RHxOZATJGi7x4dE-U74-O3tg&_nc_ht=scontent-yyz1-1.xx&oh=ca619eb9af75f233e9a0178abbf84214&oe=5DC95E98)

URL's can be truncated in this fashion, and the letters following the URL denote which destination to send the email to. In this example, the emails for the first product will send to person **c** and emails for the third product will send to person **a**, **b**, *and* **c**. The mapping connecting these symbols to actual email addresses is stored in **address_book.txt**:

![Exmple](https://scontent-yyz1-1.xx.fbcdn.net/v/t1.15752-9/69317226_2495849817138076_3772262036545732608_n.png?_nc_cat=100&_nc_oc=AQniA57kkA6SFmGMI_cmgJr1pjWsN3J-2zh3suybz4gzUnOmNZoKE02Jm7wUekkgW_w&_nc_ht=scontent-yyz1-1.xx&oh=4c61b94a976d23af14160392acb3d012&oe=5E059879)

Simply add/remove URL's and email addresses to **URL_list.txt** and **address_book.txt** to tailor the tracker to your needs.

Line [89] of **product.py** will login to the *gmail* acount that sends the notifications. An app password needs to be generated for this *gmail* account which can be done at [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords) (two-factor authentication needs to be configured beforehand). For obvious reasons, I did not include a valid *gmail* account/password in the source code here, so be sure to modify the line of code before attempting to run the utility.

[89]: ``server.login("validemailaddress", "app-password")``

## Running the Utility

#### Installation:

``$ git clone https://github.com/cjporteo/amzn-price-tracker``

The required packages must be installed.
For this utility, we only need [*requests*](https://2.python-requests.org/en/master/) and [*bs4*](https://www.crummy.com/software/BeautifulSoup/bs4/doc/):

``$ pip3 install requests``
<br>
``$ pip3 install bs4``

After the packages have successfully installed, simply run the script:

``$ python3 scrape.py``

#### Scheduling:

Execution of the script can be automated via cron. Use the following command to edit the crontab, where you can specify the frequency with which the script will automatically run:

``$ crontab -e``

To run the script every two hours, for instance, add the following lines to the crontab:

``cd /Tracker-File-Path/`` (replace this with wherever you are keeping the tracker) <br>
``0 */2 * * * python3 scrape.py``

## Email Notification

When the price of a tracked product increases or decreases significantly (surpasses the configured threshold), a notification will be sent. Notifications will also be sent when an item goes back and forth between in stock and unavailable. Here is a sample notification:
<br>
<br>
![E-Mail](https://scontent-yyz1-1.xx.fbcdn.net/v/t1.15752-9/69617471_1146773968841594_6609910159797911552_n.png?_nc_cat=107&_nc_oc=AQlYAalKHgVbA4yzf72iLNudc7YY3eLVVFSKSdbChE2MV-qEu7EtFlgb4oMksk_-aTk&_nc_ht=scontent-yyz1-1.xx&oh=27ac9504d7f79403ed938ac91806a91e&oe=5E088C79)
<br>

## Notes

 - This utility is reliant on the current structure that Amazon uses to encode their product webpages. If implementation changes on their end in the future, the utility will crash until updated.
 - This utility has only been tested for amazon.ca and amazon.com. Other currency systems and their representations in the webpage may be problematic.
