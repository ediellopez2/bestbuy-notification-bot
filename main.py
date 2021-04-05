import variables        # Stores my Google Email & Password
import requests                           # Web Scraping
from bs4 import BeautifulSoup             # Web Scraping
import smtplib                            # Send Email
from email.message import EmailMessage    # Send Email
from datetime import datetime             # Display Time
import time                               # Go To Sleep

# Helpful Links
# 1. Determine the User-Agent
# http://httpbin.org/get

def sendEmail(subject,message):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = variables.EMAIL_USER
    msg['To'] = variables.EMAIL_RECEPIENT
    msg.set_content(message)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(variables.EMAIL_USER, variables.EMAIL_PASS)
        smtp.send_message(msg)

if __name__ == "__main__":
    while (True):
        try:
            #                             Web Scraping
            # =======================================================================
            URL = 'https://www.bestbuy.com/site/nvidia-geforce-rtx-3060-ti-8gb-gddr6-pci-express-4-0-graphics-card-steel-and-black/6439402.p?skuId=6439402'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}

            page = requests.get(URL, headers=headers)
            soup = BeautifulSoup(page.text, 'html.parser')

            # Uncomment this to see all of the source code from the website. IT IS SUPER LONG!!
            # print(soup.prettify())

            # Get the name of the product.
            product_title = soup.find('div', class_='sku-title')
            # print(product_title.string)

            # Get the status of the product (Add to Cart/Sold Out).
            determine_status = soup.find('button', class_='add-to-cart-button')
            # print(determine_status.string)

            message = ""
            if (determine_status.string == "Sold Out"):
                message = datetime.now().strftime('%Y-%m-%d %H:%M:%S').__str__() + ": " + product_title.string + " is " + determine_status.string
            else:
                message = datetime.now().strftime('%Y-%m-%d %H:%M:%S').__str__() + ": " + "GREAT NEWS! " + product_title.string + " is In Stock!"
                sendEmail('BestBuy Notification Bot', message)

            # Print to the console.
            print(message)
            time.sleep(30)
            # =======================================================================
        except Exception as e:

            # Print to the console.
            print("AN ERROR OCCURRED AT " + datetime.now().strftime('%Y-%m-%d %H:%M:%S').__str__() + "!\nHere is the specific error:\n\n")
            print(e.__str__())

            # Create message and send the email.
            message = "AN ERROR OCCURRED AT " + datetime.now().strftime('%Y-%m-%d %H:%M:%S').__str__() + "!\nHere is the specific error:\n\n" + e.__str__()
            sendEmail('Problem: BestBuy Notification Bot', message)
            break