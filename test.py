from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Edge(options=options)

driver.get("https://google.com")

print("Opened Google")

driver.quit()
