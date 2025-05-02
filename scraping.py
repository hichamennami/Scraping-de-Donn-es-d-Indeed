from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time

chrome_driver_path = 'C:\\chromedriver-win64\\chromedriver.exe'

def scrape_jobs(ville, domaine):
    base_url = "https://ma.indeed.com/jobs"
    query = f"?q={domaine.replace(' ', '+')}&l={ville.replace(' ', '+')}"
    url = base_url + query

    service = Service(chrome_driver_path)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    job_titles = []
    links = []

    jobs = soup.find_all('div', class_='job_seen_beacon')

    for job in jobs:
        try:
            title = job.find('h2', class_='jobTitle').text.strip()
        except AttributeError:
            title = None
        try:
            link = 'https://ma.indeed.com' + job.find('a', href=True)['href']
        except AttributeError:
            link = None

        job_titles.append(title)
        links.append(link)

    driver.quit()

    # Retourne une liste de tuples
    return list(zip(job_titles, links))
