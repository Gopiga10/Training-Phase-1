from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

chrome_driver_path = r"C:\Users\HP\OneDrive\Desktop\scraping\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"

options = Options()
options.add_argument("--headless")  # Optional
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Set up Chrome driver service
service = Service(executable_path=chrome_driver_path)

try:
    driver = webdriver.Chrome(service=service, options=options)
    print("ChromeDriver is working!")
    driver.quit()
except Exception as e:
    print(" ChromeDriver is not working.")
    print(f"Error: {e}")

