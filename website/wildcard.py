from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from .models import User, SimilarPeople
from . import db
import time

def find_similar_people(wildcard, current_user):
    #SETTING UP BROWSER
    #headless mode + stop with the annoying output
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(options=chrome_options)
    chrome_options.add_argument("--log-level=3")
    #going to google images and finding searchbar
    browser.get("https://www.google.com/imghp")
    searchbar = browser.find_element(By.NAME, "q")
    searchbar.click()
    # just doing this part so we can go to the main page one 
    # time and do all searching from that page
    searchbar.send_keys(f"{wildcard} women in STEM")
    searchbar.send_keys(Keys.RETURN)

    img_links = []

    for x in range(20):
        try:
            time.sleep(0.5)
            img = browser.find_element(By.XPATH, f"""//*[@id="islrg"]/div[1]/div[{x}]/a[1]/div[1]/img""")
            img_link = img.get_attribute("src")
            similar_person = SimilarPeople(lnk=img_link, user_id=current_user.id)
            db.session.add(similar_person)
            db.session.commit()
            # img_links.append(img_link)

        except:
            continue
    
    return img_links
