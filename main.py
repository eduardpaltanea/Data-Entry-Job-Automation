from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

form_address = "https://docs.google.com/forms/d/e/1FAIpQLSd1OBQcvxZ39qmE_yUMECvk_KV3QrmbD1-2xcY17P4Kdpp-gg/viewform?usp=sf_link"

response = requests.get("https://appbrewery.github.io/Zillow-Clone/")
web_page = response.text
soup = BeautifulSoup(web_page, "html.parser")
info_tag = soup.find_all(name="div", class_="StyledPropertyCardDataWrapper")
list_of_links, property_price_list, address_list = [], [], []

for tag in info_tag:
    # Getting all the links of the properties
    property_tag = tag.find(name="a")
    property_link = property_tag.get("href")
    list_of_links.append(property_link)

    # Getting all the prices for the properties
    property_price_tag = tag.find(name="span")
    property_price = property_price_tag.getText().split("+")[0].split("/")[0]
    property_price_list.append(property_price)

    # Getting all the addresses for the properties
    address_tag = tag.find(name="address")
    address = address_tag.getText().strip().replace("|", "")
    address_list.append(address)

# Setting up the webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

# For every item
for i in range(len(list_of_links)):
    driver.get(form_address)
    time.sleep(2)

    #Geting the inputs for every question in the form
    current_address = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    current_price = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    current_link = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

    # Submitting the answer for every question
    current_address.send_keys(address_list[i])
    current_price.send_keys(property_price_list[i])
    current_link.send_keys(list_of_links[i])
    submit_button.click()



