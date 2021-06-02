import variables                          # Stores variables
import requests                           # Web Scraping
from bs4 import BeautifulSoup             # Web Scraping
from twilio.rest import Client            # Twilio
from datetime import datetime             # Display Time
import time                               # Go To Sleep

# Helpful Links
# 1. Determine the User-Agent
# http://httpbin.org/get


def send_sms(recipient, message):
    client = Client(variables.TWILIO_ACCOUNT_SID, variables.TWILIO_AUTH_TOKEN)

    client.messages.create(
        body=message,
        from_=variables.number_twilio,
        to=recipient
    )
    return


if __name__ == "__main__":
    while True:
        try:
            page = requests.get(variables.URL, headers=variables.HEADERS)

            # 2xx successful – the request was successfully received, understood, and accepted
            if page.status_code == 200:
                soup = BeautifulSoup(page.text, 'html.parser')

                # Uncomment this to see all of the source code from the website. IT IS SUPER LONG!!
                # print(soup.prettify())

                # Get the name of the product.
                product_title = soup.find('div', class_='sku-title')
                # print(product_title.string)

                # Get the status of the product (Add to Cart/Sold Out).
                determine_status = soup.find('button', class_='add-to-cart-button')

                message = ""
                if determine_status.text == "Sold Out":
                    message = datetime.now().strftime('%Y-%m-%d %H:%M:%S').__str__() + ": " + product_title.string + " is " + determine_status.string
                else:
                    message = datetime.now().strftime('%Y-%m-%d %H:%M:%S').__str__() + ": " + "GREAT NEWS! " + product_title.string + " is In Stock!"
                    send_sms(variables.number_luis, message)

                # Print to the console.
                print(message)
                time.sleep(30)
        except requests.exceptions.ConnectionError as errc:
            # In the event of a network problem (e.g. DNS failure, refused connection, etc),
            # Requests will raise a ConnectionError exception.
            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.")
            print(errc.__str__())

            # Sleep for 1 minute and try to run the program again.
            time.sleep(60)  # 1 minute
            continue
        except Exception as exc:
            # This block will execute when an unexpected error that is unrelated to connection error occurs.
            errorMessage = "Your bot crashed at " + datetime.now().strftime('%Y-%m-%d %H:%M:%S').__str__() + "!\n"
            print(errorMessage + "Here is the specific error:\n" + exc.__str__())

            send_sms(variables.number_luis, message)
            break
