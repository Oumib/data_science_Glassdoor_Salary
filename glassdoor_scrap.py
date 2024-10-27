from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time
import pandas as pd

def get_jobs(keyword, num_jobs, verbose):
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    # Initializing the webdriver
    options = webdriver.ChromeOptions()
    
    # Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    # options.add_argument('headless')

    # Create a Service object with the path to chromedriver
    service = Service(executable_path="C:/Users/PC/Documents/ds_salaryGlassdoor/chromedriver-win32/chromedriver.exe")
    
    # Initialize the Chrome driver with the Service object
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1120, 1000)

    url = f'https://www.glassdoor.com/Job/new-york-city-data-scientist-jobs-SRCH_IL.0,13_IC1132348_KO14,28.htm'
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  # If true, should be still looking for new jobs.
        time.sleep(4)

        # Test for the "Sign Up" prompt and get rid of it.
        try:
            driver.find_element(By.CLASS_NAME, "selected").click()
        except ElementClickInterceptedException:
            pass
        time.sleep(.1)

        try:
            driver.find_element(By.CLASS_NAME, "ModalStyle__xBtn___29PT9").click()
        except NoSuchElementException:
            pass

        # Going through each job in this page
        job_buttons = driver.find_elements(By.CLASS_NAME, "jl")  # jl for Job Listing.
        for job_button in job_buttons:  
            print(f"Progress: {len(jobs)}/{num_jobs}")
            if len(jobs) >= num_jobs:
                break

            job_button.click()  
            time.sleep(1)
            collected_successfully = False
            
            while not collected_successfully:
                try:
                    company_name = driver.find_element(By.XPATH, './/div[@class="employerName"]').text
                    location = driver.find_element(By.XPATH, './/div[@class="location"]').text
                    job_title = driver.find_element(By.XPATH, './/div[contains(@class, "title")]').text
                    job_description = driver.find_element(By.XPATH, './/div[@class="jobDescriptionContent desc"]').text
                    collected_successfully = True
                except Exception:
                    time.sleep(5)

            try:
                salary_estimate = driver.find_element(By.XPATH, './/span[@class="gray small salary"]').text
            except NoSuchElementException:
                salary_estimate = -1
            
            try:
                rating = driver.find_element(By.XPATH, './/span[@class="rating"]').text
            except NoSuchElementException:
                rating = -1

            if verbose:
                print(f"Job Title: {job_title}")
                print(f"Salary Estimate: {salary_estimate}")
                print(f"Job Description: {job_description[:500]}")
                print(f"Rating: {rating}")
                print(f"Company Name: {company_name}")
                print(f"Location: {location}")

            # Additional job details collection would go here...

        # Click on the "next page" button
        try:
            driver.find_element(By.XPATH, './/li[@class="next"]//a').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)  # This line converts the dictionary object into a pandas DataFrame.

# Call the function to start scraping
df = get_jobs("data scientist", 5, False)
print(df)
