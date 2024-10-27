# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 09:32:36 2020

author: Bounekhla Oumaima
url: https://github.com/Oumib/ds_salaryGlassdoor
"""
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

def get_jobs(target_url):
    """Gathers jobs from Glassdoor and returns a DataFrame."""
    
    # Initialisation du WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(target_url)
    
    driver.maximize_window()
    time.sleep(2)  # Temps d'attente pour charger la page

    resp = driver.page_source
    driver.quit()  # Ferme le navigateur après avoir récupéré le contenu de la page

    soup = BeautifulSoup(resp, 'html.parser')

    # Trouver le conteneur contenant les offres d'emploi
    allJobsContainer = soup.find("ul", {"class": "JobsList_jobsList__lqjTr"})
    allJobs = allJobsContainer.find_all("li") if allJobsContainer else []

    job_list = []  # Liste pour stocker les informations sur les emplois
    for job in allJobs:
        job_info = {}
        
        company_element = job.find("div", {"class": "EmployerProfile_profileContainer__VjVBX"})
        job_info["name-of-company"] = company_element.text.strip() if company_element else None

        job_title_element = job.find("a", {"class": "JobCard_jobTitle___7I6y"})
        job_info["name-of-job"] = job_title_element.text.strip() if job_title_element else None

        location_element = job.find("div", {"class": "JobCard_location__rCz3x"})
        job_info["location"] = location_element.text.strip() if location_element else None

        salary_element = job.find("div", {"class": "JobCard_salaryEstimate__arV5J"})
        job_info["salary"] = salary_element.text.strip() if salary_element else None

        # Ajouter uniquement si le nom de la société et le nom de l'emploi ne sont pas None
        if job_info["name-of-company"] and job_info["name-of-job"]:
            job_list.append(job_info)

    # Convertir en DataFrame et sauvegarder
    df = pd.DataFrame(job_list)
    df.to_csv('C:/Users/PC/Documents/ds_salaryGlassdoor/jobs_glassdoor.csv', index=False, encoding='utf-8', sep=';')

    return df  # Retourner le DataFrame

# Exemple d'utilisation
if __name__ == "__main__":
    target_url = "https://www.glassdoor.com/Job/new-york-python-jobs-SRCH_IL.0,8_IC1132348_KO9,15.htm?clickSource=searchBox"
    df_jobs = get_jobs(target_url)
    print(df_jobs)
