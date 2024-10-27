from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd

def get_jobs(keyword, num_jobs, verbose, path, slp_time):
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    # Initializing the webdriver
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path='C:/Users/PC/Documents/ds_salaryGlassdoor/chromedriver-win32/chromedriver.exe', options=options)
    driver.set_window_size(1120, 1000)
    
    # URL for "Data Scientist" jobs
    url = f"https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword={keyword}&sc.keyword={keyword}&jobType="
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  # If true, should be still looking for new jobs.
        time.sleep(slp_time)

        # Close the "Sign Up" prompt if it appears
        try:
            driver.find_element_by_class_name("selected").click()
        except ElementClickInterceptedException:
            pass
        time.sleep(.1)

        try:
            driver.find_element_by_css_selector('[alt="Close"]').click()  # Clicking to the X
        except NoSuchElementException:
            pass

        # Going through each job in this page
        job_buttons = driver.find_elements_by_class_name("jl")  # jl for Job Listing
        for job_button in job_buttons:  
            print(f"Progress: {len(jobs)}/{num_jobs}")
            if len(jobs) >= num_jobs:
                break

            job_button.click()
            time.sleep(1)
            collected_successfully = False
            
            while not collected_successfully:
                try:
                    company_name = driver.find_element_by_xpath('.//div[@class="employerName"]').text
                    location = driver.find_element_by_xpath('.//div[@class="location"]').text
                    job_title = driver.find_element_by_xpath('.//div[contains(@class, "title")]').text
                    job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
                    collected_successfully = True
                except Exception as e:
                    print("Error collecting job details:", e)
                    time.sleep(5)

            # Get salary estimate
            try:
                salary_estimate = driver.find_element_by_xpath('.//span[@class="gray salary"]').text
            except NoSuchElementException:
                salary_estimate = -1  # Set a "not found" value

            # Get job rating
            try:
                rating = driver.find_element_by_xpath('.//span[@class="rating"]').text
            except NoSuchElementException:
                rating = -1  # Set a "not found" value

            if verbose:
                print(f"Job Title: {job_title}")
                print(f"Salary Estimate: {salary_estimate}")
                print(f"Job Description: {job_description[:500]}")
                print(f"Rating: {rating}")
                print(f"Company Name: {company_name}")
                print(f"Location: {location}")

            # Go to the Company tab
            try:
                driver.find_element_by_xpath('.//div[@class="tab" and @data-tab-type="overview"]').click()

                try:
                    headquarters = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Headquarters"]//following-sibling::*').text
                except NoSuchElementException:
                    headquarters = -1

                try:
                    size = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*').text
                except NoSuchElementException:
                    size = -1

                try:
                    founded = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*').text
                except NoSuchElementException:
                    founded = -1

                try:
                    type_of_ownership = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Type"]//following-sibling::*').text
                except NoSuchElementException:
                    type_of_ownership = -1

                try:
                    industry = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text
                except NoSuchElementException:
                    industry = -1

                try:
                    sector = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text
                except NoSuchElementException:
                    sector = -1

                try:
                    revenue = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*').text
                except NoSuchElementException:
                    revenue = -1

                try:
                    competitors = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*').text
                except NoSuchElementException:
                    competitors = -1

            except NoSuchElementException:  # Rarely, some job postings do not have the "Company" tab.
                headquarters = size = founded = type_of_ownership = industry = sector = revenue = competitors = -1

            if verbose:
                print("Headquarters:", headquarters)
                print("Size:", size)
                print("Founded:", founded)
                print("Type of Ownership:", type_of_ownership)
                print("Industry:", industry)
                print("Sector:", sector)
                print("Revenue:", revenue)
                print("Competitors:", competitors)
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({
                "Job Title": job_title,
                "Salary Estimate": salary_estimate,
                "Job Description": job_description,
                "Rating": rating,
                "Company Name": company_name,
                "Location": location,
                "Headquarters": headquarters,
                "Size": size,
                "Founded": founded,
                "Type of ownership": type_of_ownership,
                "Industry": industry,
                "Sector": sector,
                "Revenue": revenue,
                "Competitors": competitors
            })

        # Clicking on the "next page" button
        try:
            driver.find_element_by_xpath('.//li[@class="next"]//a').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)  # This line converts the dictionary object into a pandas DataFrame.

# Exemple d'appel de la fonction
if __name__ == "__main__":
    path_to_chromedriver = "C:/path/to/chromedriver.exe"  # Mettez à jour avec le chemin correct
    df_jobs = get_jobs("Data Scientist", 100, verbose=True, path=path_to_chromedriver, slp_time=5)
    df_jobs.to_csv("data_scientist_jobs.csv", index=False)
