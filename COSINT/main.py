import os
import shutil
import sys
from zipfile import ZipFile
import requests
import argparse
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import platform
from time import sleep
import re

# Responsible for CLI and also orchestrating the main functions
class CLI :
    def __init__(self, args):
        self.greet()
        self.dorker = Dorker()
        self.chromedriver_def_path = self.get_chromedriver()
        self.query_maker = QueryMaker(self.chromedriver_def_path, args.pagenumber)
        self.print_linkedin()

    # Downloads chromedriver's latest release from the internet according to the host OS
    def get_chromedriver(self):
        """
        If I use general path convention, it won't work when we extract this project
        to an executable file. So I decide the path to main.py like this
        """
        if getattr(sys, 'frozen', False):
            chromedriver_def_path = os.path.join(sys._MEIPASS)
        else:
            chromedriver_def_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))

        # Checking and getting the latest version number
        version_url = "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE"
        version = requests.get(version_url).text

        # Paths and executable names differ from OS to OS. So I branched them
        if (platform.system() == "Windows"):
            # chromedriver's download links are following a general pattern
            url = "https://storage.googleapis.com/chrome-for-testing-public/" + version + "/win64/chromedriver-win64.zip"
            zip_name = "chromedriver-win64.zip"

            zip_file_path = os.path.join(chromedriver_def_path, zip_name)

            # Downloading the latest chromedriver zip file
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(zip_file_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
            else:
                print("ah")
                raise SystemExit(1)

            # Extracting the zip file
            try:
                with ZipFile(zip_file_path, 'r') as zip_ref:
                    zip_ref.extractall(chromedriver_def_path)

            except Exception as e:
                print(e)
                raise SystemExit(1)

            # Removing the zip file because it's extracted already
            if os.path.exists(zip_file_path):
                os.remove(zip_file_path)

            exact_path = os.path.join(chromedriver_def_path, "chromedriver-win64/chromedriver.exe")

            # We need only the chromedriver from the extracted folder so we copy it outside the folder
            try:
                shutil.copy(exact_path, chromedriver_def_path)
            except Exception as e:
                print(e)
                raise SystemExit(1)

            exact_path = os.path.join(chromedriver_def_path, "chromedriver-win64")

            # Removing the extracted folder recursively
            try:
                shutil.rmtree(exact_path)
            except Exception as e:
                print(e)
                raise SystemExit(1)

            return chromedriver_def_path + "/chromedriver.exe"

        # Similar things goes on Linux part
        elif (platform.system() == "Linux") :
            url = "https://storage.googleapis.com/chrome-for-testing-public/" + version + "/linux64/chromedriver-linux64.zip"
            zip_name = "chromedriver-linux64.zip"
            exact_path = os.path.join(chromedriver_def_path, "chromedriver-linux64/chromedriver") # bak

            zip_file_path = os.path.join(chromedriver_def_path, zip_name)

            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(zip_file_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
            else:
                raise SystemExit(1)

            try:
                with ZipFile(zip_file_path, 'r') as zip_ref:
                    zip_ref.extractall(chromedriver_def_path)

            except Exception as e:
                print(e)
                raise SystemExit(1)

            if os.path.exists(zip_file_path):
                os.remove(zip_file_path)

            exact_path = os.path.join(chromedriver_def_path, "chromedriver-linux64/chromedriver")

            try:
                shutil.copy(exact_path, chromedriver_def_path)
            except Exception as e:
                print(e)
                raise SystemExit(1)

            exact_path = os.path.join(chromedriver_def_path, "chromedriver-linux64")

            try:
                shutil.rmtree(exact_path)
            except Exception as e:
                print(e)
                raise SystemExit(1)

            # Returning the path of the donwloaded chromedriver latest release
            return chromedriver_def_path + "/chromedriver"

    # Greets the users on CLI
    def greet(self):
        headline = """
  ______    ______    ______   ______  __    __  ________
 /      \\  /      \\  /      \\ |      \\|  \\  |  \\|        \\
|  $$$$$$\\|  $$$$$$\\|  $$$$$$\\ \\$$$$$$| $$\\ | $$ \\$$$$$$$$
| $$   \\$$| $$  | $$| $$___\\$$  | $$  | $$$\\| $$   | $$
| $$      | $$  | $$ \\$$    \\   | $$  | $$$$\\ $$   | $$
| $$   __ | $$  | $$ _\\$$$$$$\\  | $$  | $$\\$$ $$   | $$
| $$__/  \\| $$__/ $$|  \\__| $$ _| $$_ | $$ \\$$$$   | $$
 \\$$    $$ \\$$    $$ \\$$    $$|   $$ \\| $$  \\$$$   | $$
  \\$$$$$$   \\$$$$$$   \\$$$$$$  \\$$$$$$ \\$$   \\$$    \\$$  \n"""

        print("\033[36m" + headline + "\033[0m")

        title = "\033[31m" + "Company Open Source Intelligence" + "\033[0m"
        print(f"{title:^67}")
        signature = "\033[31m" + "by karmagedon" + "\033[0m"
        print(f"{signature:^67}")
        version = "\033[31m" + "v.0.0" + "\033[0m"
        print(f"{version:^67}")
        print()

    # Initiating the functions related to LinkedIn scraping
    def print_linkedin(self):
        linkedin_wordlist = self.dorker.wrap_linkedin(args.company, args.domain)
        self.query_maker.linkedin_query(linkedin_wordlist)

# Generates the strings to be used for query in search engines
class Dorker :
    def __init__(self):
        pass
    # Generates LinkedIn related search strings
    def wrap_linkedin(self, company_name, domain_name):
        company_search = "site:linkedin.com/company \"" + company_name + "\""
        employee_search = "site:linkedin.com/in \"" + company_name + "\""
        mail_search = "site:linkedin.com/ \"" + "@" + domain_name + "\""

        return {"Company" : company_search, "Employee" : employee_search, "Mail" : mail_search}


    # To be completed, not yet
    def mail_guesser(self, employee_name, domain_name):
        results = []
        base = "@" + domain_name

# Makes search engine queries with chromedriver and Selenium, also returns results
class QueryMaker :
    def __init__(self, chromedriver_path, max_page_num):
        self.chromedriver_path = chromedriver_path
        self.max_page_num = max_page_num

    # Main initiator for LinkedIn queries
    def linkedin_query(self, wordlist):
        employees = self.linkedin_employee_query(wordlist.get("Employee"), wordlist.get("Company"))
        mails = self.linkedin_mail_query(wordlist.get("Mail"))
        company_info = self.linkedin_company_query(wordlist.get("Company"))
        return {"Employees" : employees, "Mails" : mails, "Company" : company_info}

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
        #options.add_argument("--headless")
        options.page_load_strategy = "eager"

        service = Service(self.chromedriver_path)

        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(15)
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

                wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id=\"bnp_btn_reject\"]")))
                wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"bnp_btn_reject\"]")))
                sleep(1)
                driver.find_element(By.XPATH, "//*[@id=\"bnp_btn_reject\"]").click()

                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#b_results > li.b_pag > nav > ul > li:nth-child(5) > a")))
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
                    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#b_results > li.b_pag > nav > ul > li:nth-child(7) > a")))
                    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#b_results > li.b_pag > nav > ul > li:nth-child(7) > a")))
                    sleep(1)
                    driver.find_element(By.CSS_SELECTOR, "#b_results > li.b_pag > nav > ul > li:nth-child(7) > a").click()
                except :
                    try :
                        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#b_results > li.b_pag > nav > ul > li:nth-child(8) > a")))
                        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#b_results > li.b_pag > nav > ul > li:nth-child(8) > a")))
                        sleep(1)
                        driver.find_element(By.CSS_SELECTOR,"#b_results > li.b_pag > nav > ul > li:nth-child(8) > a").click()
                    except Exception as e:
                        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#b_results > li.b_pag > nav > ul > li:nth-child(9) > a")))
                        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#b_results > li.b_pag > nav > ul > li:nth-child(9) > a")))
                        sleep(1)
                        driver.find_element(By.CSS_SELECTOR,"#b_results > li.b_pag > nav > ul > li:nth-child(9) > a").click()


        for linkedin_link in filtered_links:
            full_string = linkedin_link[0]
            employee_name = full_string[0:full_string.index(" - ")]
            temp = full_string[full_string.index(" - ")+3:]
            try :
                employee_role = temp[0:temp.index(" - ")]
            except :
                try :
                    employee_role = temp[0:temp.index(" | ")]
                except:
                    employee_role = "Unknown"

            if (employee_role == company_name) :
                print(employee_name + "  :  " + "Unknown" + "   --->  " + linkedin_link[1])
            else :
                print(employee_name + "  :  " + employee_role + "   --->  " + linkedin_link[1])

        print("Total results : ", len(filtered_links))

        driver.quit()
    def linkedin_company_query(self, wordlist):
        print()
    def linkedin_mail_query(self, wordlist):
        print()



if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--company", type=str, help="Company name", required=True)
    parser.add_argument("-o", "--output", type=str, help="Output file name", required=False, default="output.txt")
    parser.add_argument("-d", "--domain", type=str, help="Domain name", required=True)
    parser.add_argument("-p", "--pagenumber", type=int, help="Number of pages to be read", required=False, default=5)
    args = parser.parse_args()

    cli = CLI(args)