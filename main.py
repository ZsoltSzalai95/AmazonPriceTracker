import requests
import pprint
from bs4 import BeautifulSoup
import lxml
import smtplib

#_______ Step 1 - Scrape Amazon website

HEADERS = {
    "Accept-Language":"en-US,en;q=0.9",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"

}

URL = "https://www.amazon.com/MSI-GeForce-RTX-3090-VENTUS/dp/B08HR9D2JS/ref=sr_1_7?crid=50VX4WYEW1GI&keywords=3090&qid=1643552177&sprefix=3090%2Caps%2C160&sr=8-7"

response = requests.get(URL, headers=HEADERS)

soup = BeautifulSoup(response.content, "lxml")

price = soup.find(name="span", class_="a-offscreen").getText()
price_wo_currency = price.split("$")[1].replace(',', '')
price_float = float(price_wo_currency)

#______ Step 2 - Sending an email to you when desired price is published

MY_EMAIL = "YOUR_MAIL"
MY_PASSWORD= "YOUR_PASS"

if price_float <= 3900:

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=MY_EMAIL,

                            msg="Subject:Amazon Price Alert\n\n"
                                f"MSI Gaming GeForce RTX 3090 24GB GDRR6X 384-Bit HDMI/DP Nvlink Torx Fan 3 Ampere Architecture OC Graphics Card (RTX 3090 VENTUS 3X 24G OC) is now ${price_float}!\n\n"
                                f"Link:{URL}"
                                )