from flask import Flask, render_template, request
from scraping import scrape_jobs

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time

chrome_driver_path = r"C:\Users\Lenovo\Desktop\graphe python\projet data scraping\datascraping\chromedriver.exe"

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


app = Flask(__name__)

# Liste des villes et domaines disponibles
VILLES = ['Casablanca', 'Rabat', 'Marrakech', 'Fès', 'Tanger', 'Agadir', 'Oujda','Mohamedia']
DOMAINES = [
    'Product Manager', 'AI', 'BI', 'Data Science', 'Designer',
    'Sales', 'Project Manager', 'Engineer', 'DevOps'
]

@app.route('/')
def index():
    return render_template('index.html', villes=VILLES, domaines=DOMAINES)

@app.route('/results', methods=['POST'])
def results():
    ville = request.form['ville']
    domaine = request.form['domaine']
    jobs = scrape_jobs(ville, domaine)  # Appel de la fonction de scraping

    return render_template('results.html', jobs=jobs, ville=ville, domaine=domaine)

if __name__ == '__main__':
    app.run(debug=True)
