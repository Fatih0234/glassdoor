import os
import time
import datetime
import re
from collections import namedtuple
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
import pandas as pd
from bs4 import BeautifulSoup
from typing import Optional



user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
driver_path = os.path.join(os.getcwd(), "chromedriver-win64", "chromedriver.exe")
chrome_service = Service(driver_path)
chrome_options = Options()
chrome_options.add_argument(f"user-agent={user_agent}")

browser = Chrome(service=chrome_service, options=chrome_options)
browser.implicitly_wait(7)
browser.maximize_window()

url = "https://www.glassdoor.com/Job/index.htm"

browser.get(url)

# Search for jobs

search_job = browser.find_element(By.XPATH, "//input[@id='searchBar-jobTitle']")
search_job.send_keys("Data Scientist")
# search_job.send_keys(Keys.ENTER)

time.sleep(2)

# Search for location

search_location = browser.find_element(By.XPATH, "//input[@id='searchBar-location']")
search_location.send_keys("United States")
search_location.send_keys(Keys.ENTER)

def extract_post_data(post) -> dict:
    """
    Extracts job data from a BeautifulSoup object representing a job post.

    This function takes a Selenium WebElement representing a job post, converts it to a BeautifulSoup object, 
    and then extracts the job title, company name, location, days posted, and salary estimate from the post. 
    It uses the BeautifulSoup `find` method to find the first tag that matches each piece of data's class name.

    If a piece of data is not found in the post (i.e., if the `find` method returns None), 
    the function catches the AttributeError that would be raised when trying to access the `text` attribute 
    and instead assigns None to that piece of data.

    Args:
        post (selenium.webdriver.remote.webelement.WebElement): The job post to extract data from.

    Returns:
        dict: A dictionary with the extracted data. The keys are the names of the pieces of data, 
        and the values are the extracted data or None if the data was not found.
    """
    post_soup = BeautifulSoup(post.get_attribute("innerHTML"), "html.parser")

    def find_text(class_name: str) -> Optional[str]:
        try:
            return post_soup.find(attrs={"class": class_name}).text
        except AttributeError:
            return None

    return {
        "job_title": find_text("JobCard_seoLink__WdqHZ"),
        "company_name": find_text("EmployerProfile_employerName__Xemli"),
        "location": find_text("JobCard_location__N_iYE"),
        "days_posted": find_text("JobCard_listingAge__KuaxZ"),
        "salary_estimate": find_text("JobCard_salaryEstimate___m9kY"),
    }



# Find all the posts

# click shows more job button till we have 1000 posts


go_on = True
while go_on:
    try:
        close_button = browser.find_element(By.XPATH, "//button[@class='CloseButton']")
        close_button.click()
    except NoSuchElementException:
        pass
    posts = browser.find_elements(By.XPATH, "//li[@class='JobsList_jobListItem__JBBUV']")
    if len(posts) >= 29:
        go_on = False
        break
    try:
        time.sleep(1)
        show_more_jobs = browser.find_element(By.XPATH, "//button[@data-test='load-more']")
        show_more_jobs.click()
    except ElementNotInteractableException:
        go_on = False
        break
    except NoSuchElementException:
        go_on = False
        break
print(len(posts))


# let's create nambedtuple to store the data we are interested in

glassdoor_post = namedtuple("glassdoor_post", "job_title company_name location days_posted salary_estimate job_description company_rating company_size company_founded company_type company_industry company_sector company_revenue")
all_posts = []
for post in posts:
    post.click()
    time.sleep(1)
    try:
        close_button = browser.find_element(By.XPATH, "//button[@class='CloseButton']")
        close_button.click()
        time.sleep(1)
        
    except NoSuchElementException:
        pass
    
    # post details on the left part of the page
    post_details = extract_post_data(post)
    
    
    # related to posts   
    
    # click to the show more button to see the whole job description
    show_more_post = browser.find_element(By.XPATH, "//button[@class='JobDetails_showMore__j5Z_h']")
    show_more_post.click()
    
    #  only two parts we need
    job_description = browser.find_element(By.XPATH, "//div[@class='JobDetails_jobDescription__6VeBn JobDetails_showHidden__trRXQ']")
    
    company_rating = browser.find_element(By.XPATH, "//div[@id='rating-headline']")
    
    company_details = browser.find_element(By.XPATH, "//div[@class='JobDetails_companyOverviewGrid__CV62w']")
    
    soup = BeautifulSoup(company_details.get_attribute("innerHTML"), "html.parser")
    company_details_soup = soup.find_all("div", {"class": "JobDetails_overviewItem__35s2T"})
    company_size = company_details_soup[0].text
    company_founded = company_details_soup[1].text
    company_type= company_details_soup[2].text
    company_industry = company_details_soup[3].text
    company_sector = company_details_soup[4].text
    company_revenue = company_details_soup[5].text
    
    one_post = glassdoor_post(
                            post_details["job_title"], 
                            post_details["company_name"], 
                            post_details["location"],
                            post_details["days_posted"],
                            post_details["salary_estimate"],
                            job_description.text, 
                            company_rating.text,
                            company_size, 
                            company_founded,
                            company_type, 
                            company_industry, 
                            company_sector, 
                            company_revenue
                              )
    all_posts.append(one_post)
    print(one_post)
    break

print(all_posts)

all_posts_df = pd.DataFrame(all_posts)
all_posts_df.head()
all_posts_df.to_csv("glassdoor_posts.csv", index=False)