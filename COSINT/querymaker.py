from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import re

# Makes search engine queries with chromedriver and Selenium, also returns results
class QueryMaker :
    def __init__(self, chromedriver_path, max_page_num, headless):
        self.chromedriver_path = chromedriver_path
        self.max_page_num = max_page_num
        self.headless = headless
    # Main initiator for LinkedIn queries
    def linkedin_query(self, wordlist):
        employees = self.linkedin_employee_query(wordlist.get("Employee"), wordlist.get("Company"))
        return {"Employees" : employees}

    # Queries employees of a company from LinkedIn
    def linkedin_employee_query(self, word, company_name):
        # Generating random user agents to avoid being detected as a bot
        user_agent = UserAgent()
        random_agent = user_agent.random
        request_header = f"--user_agent={random_agent}"

        # Preparing the necessary arguments and options for the Selenium Webdriver
        options = Options()
        options.add_argument(request_header)
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--window-size=1920,1080")
        if (self.headless == True) :
            options.add_argument("--headless=new")
        options.page_load_strategy = "eager"

        service = Service(self.chromedriver_path)

        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(15)
        driver.maximize_window()
        wait = WebDriverWait(driver, 20)


        url = f"https://www.bing.com/search?q={word}"

        driver.get(url)
        sleep(2)

        filtered_links = []
        all_links_obj = []

        for i in range(0, self.max_page_num - 1):
            if (i == 0) :
                sleep(3)
                all_links_obj = driver.find_elements(By.XPATH, "//a[@href]")

                # There are so many unrelated links, so we need a regex that we can filter out what we want
                regex_control = re.compile(r"^https:\/\/(www|[a-z]{2,3})\.linkedin\.com\/in")
                for bing_link in all_links_obj:
                    try:
                        href = bing_link.get_attribute("href")
                        text = bing_link.get_attribute("text")
                    except Exception as e:
                        print(e)
                        continue
                    if (regex_control.search(href)) and (not "linkedin.com" in text) and (company_name.lower() in text.lower()):
                        filtered_links.append([text, href])

                all_links_obj = []

                if (self.headless == False) :
                    try :
                        wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"bnp_btn_reject\"]")))
                        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"bnp_btn_reject\"]")))
                        sleep(1)
                        driver.find_element(By.XPATH, "//*[@id=\"bnp_btn_reject\"]").click()
                    except :
                        pass

                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#b_results > li.b_pag > nav > ul > li:nth-child(5) > a")))
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#b_results > li.b_pag > nav > ul > li:nth-child(5) > a")))
                sleep(1)
                driver.find_element(By.CSS_SELECTOR, "#b_results > li.b_pag > nav > ul > li:nth-child(5) > a").click()
            else :
                sleep(3)
                all_links_obj = driver.find_elements(By.XPATH, "//a[@href]")

                # There are so many unrelated links, so we need a regex that we can filter out what we want
                regex_control = re.compile(r"^https:\/\/(www|[a-z]{2,3})\.linkedin\.com\/in")
                for bing_link in all_links_obj:
                    try:
                        href = bing_link.get_attribute("href")
                        text = bing_link.get_attribute("text")
                    except Exception as e:
                        print(e)
                        continue
                    if (regex_control.search(href)) and (not "linkedin.com" in text):
                        filtered_links.append([text, href])
                all_links_obj = []

                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                try :
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#b_results > li.b_pag > nav > ul > li:nth-child(7) > a")))
                    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#b_results > li.b_pag > nav > ul > li:nth-child(7) > a")))
                    sleep(1)
                    driver.find_element(By.CSS_SELECTOR, "#b_results > li.b_pag > nav > ul > li:nth-child(7) > a").click()
                except :
                    try :
                        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#b_results > li.b_pag > nav > ul > li:nth-child(8) > a")))
                        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#b_results > li.b_pag > nav > ul > li:nth-child(8) > a")))
                        sleep(1)
                        driver.find_element(By.CSS_SELECTOR,"#b_results > li.b_pag > nav > ul > li:nth-child(8) > a").click()
                    except Exception as e:
                        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#b_results > li.b_pag > nav > ul > li:nth-child(9) > a")))
                        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#b_results > li.b_pag > nav > ul > li:nth-child(9) > a")))
                        sleep(1)
                        driver.find_element(By.CSS_SELECTOR,"#b_results > li.b_pag > nav > ul > li:nth-child(9) > a").click()

        driver.quit()
        return filtered_links

    def github_query(self, domain, company_name):
        emails = self.github_mail_query(domain, company_name)
        return {"E-mails": emails}

    def github_mail_query(self, domain, company_name):
        pass