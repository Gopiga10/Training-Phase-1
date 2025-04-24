from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def init_driver():
    chrome_options = Options()
    # To see browser while running, comment below line
    # chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("window-size=1920,1080")
    # Fake user-agent
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def scrape_venue_details(url):
    driver = init_driver()
    try:
        driver.get(url)

        # Wait to let page load
        time.sleep(5)

        venue_details = {
            'match_venue_stadium': 'N/A',
            'match_venue_city': 'N/A',
            'match_venue_capacity': 'N/A',
            'match_venue_host_teams': 'N/A'
        }

        # Wait until venue info is present
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'cb-mat-fct-itm')))

        details_elements = driver.find_elements(By.CLASS_NAME, 'cb-mat-fct-itm')
        details_texts = [element.text.strip() for element in details_elements]

        for text in details_texts:
            print("Element text:", text)

        for i in range(len(details_texts)):
            text = details_texts[i]
            if 'Stadium:' in text:
                venue_details['match_venue_stadium'] = details_texts[i + 1] if i + 1 < len(details_texts) else 'N/A'
            elif 'City:' in text:
                venue_details['match_venue_city'] = details_texts[i + 1] if i + 1 < len(details_texts) else 'N/A'
            elif 'Capacity:' in text:
                venue_details['match_venue_capacity'] = details_texts[i + 1] if i + 1 < len(details_texts) else 'N/A'
            elif 'Hosts to:' in text:
                venue_details['match_venue_host_teams'] = details_texts[i + 1] if i + 1 < len(details_texts) else 'N/A'

        print(venue_details)

        df = pd.DataFrame([venue_details])
        df.to_csv('venue_details.csv', index=False)
        print("[Info] Data saved to venue_details.csv")

    except Exception as e:
        print("Error occurred:", e)

    finally:
        driver.quit()

# Test function
scrape_venue_details('https://www.cricbuzz.com/cricket-match-facts/34103/kkr-vs-rcb-30th-match-indian-premier-league-2021')

