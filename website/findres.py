from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from .models import Resource
from . import db
import time



def find_resources():
    #SETTING UP BROWSER
    #headless mode + stop with the annoying output
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(options=chrome_options)
    chrome_options.add_argument("--log-level=3")
    #going to google and finding searchbar
    browser.get("https://www.google.com")
    searchbar = browser.find_element(By.NAME, "q")
    searchbar.click()
    # just doing this part so we can go to the main page one 
    # time and do all searching from that page
    searchbar.send_keys("search")

    #----------------------------------------------------------------------------------------------------#
    #CATEGORIES

    # educational categories
    edu_category = ["how to learn to code","How to build a website","learn Java", "learn python", 
                    "learn html", "learn css", "learn sql", "organic chemistry tutor", "integral calculator"
                    "resume vs cv", "what is github", "matlabs", "robotics fairs", "science experiment ideas"]


    # opportunities categories
    # opp_category = ["software engineering internship", "chem engineering internship", "mechanical engineering internships",
    #                 "google internships", "NASA internships", "AI and data science research", "summer research",
    #                 "summer internship", "entry level biochem job", "stem scholarships", "black women in stem scholarships",
    #                 "women in stem scholarships", "machine learning internships", "IT internships", "scholarships for college students",
    #                 "scholarships for graduate students", "scholarships for highschoolers"]


    #----------------------------------------------------------------------------------------------------#
    #SCRAPING RESOURCES

    for category in edu_category: #repeat the process for every category
        searchbar = browser.find_element(By.NAME, "q")
        searchbar.click()
        searchbar.clear()
        searchbar.send_keys(category) #search for category
        searchbar.send_keys(Keys.RETURN)
        time.sleep(1.5)
        for x in range(1,10): #each page has roughly 10 titles
            try:
                # getting the title of an article
                resource_title = browser.find_element(By.XPATH,  f"""//*[@id="rso"]/div[{x}]/div/div/div[1]/div/a/h3""")
                res_tit = resource_title.text
                #finding 'a' element so we can get the link of the title
                a = browser.find_element(By.XPATH, f"""//*[@id="rso"]/div[{x}]/div/div/div[1]/div/a""")
                a = a.get_attribute("href")
                # getting summary of the article
                summary = browser.find_element(By.XPATH, f"""//*[@id="rso"]/div[{x}]/div/div/div[2]/div""")
                summary = summary.text
                # add a new resource to the database
                new_resource = Resource(res_name=res_tit, res_link=a, res_summary=summary, res_type="Educational")
                db.session.add(new_resource)
                db.session.commit()
            except:
                continue

    print("Resources have been added")

