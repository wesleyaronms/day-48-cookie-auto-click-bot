from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime
from time import time
import os


chrome_driver_path = os.getenv("DRIVER_PATH")
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)
driver.get("http://orteil.dashnet.org/experiments/cookie/")


def buy_upgrade():
    """Irá comprar o upgrade mais caro disponível."""
    for price in prices[::-1]:
        if money >= price:
            return upgrades[prices.index(price)].click()


upgrades = driver.find_elements(By.CSS_SELECTOR, "#store b")
cookie = driver.find_element(By.ID, "cookie")
prices = [int(item.text.split("-")[1].replace(",", "")) for item in upgrades[:-1]]

#  O objetivo é conseguir o máximo de cookies por segundo em até 5 minutos.
time_out = time() + 60 * 5
while True:
    money = int(driver.find_element(By.ID, "money").text.replace(",", ""))
    if time() > time_out:
        cps = driver.find_element(By.ID, "cps")
        print(cps.text)
        break

    cookie.click()

# A cada 5 segundos compra o upgrade mais caro disponível.
    if datetime.now().second % 5 == 0:
        upgrades = driver.find_elements(By.CSS_SELECTOR, "#store b")
        buy_upgrade()

driver.quit()
