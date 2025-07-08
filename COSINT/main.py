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
import platform
from time import sleep
import re

class CLI :
    def __init__(self, args):
        self.greet()
        self.dorker = Dorker()
        self.chromedriver_def_path = self.get_chromedriver()
        self.query_maker = QueryMaker(self.chromedriver_def_path)
        self.print_linkedin()


    def get_chromedriver(self):
        if getattr(sys, 'frozen', False):
            chromedriver_def_path = os.path.join(sys._MEIPASS)
        else:
            chromedriver_def_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))

        version_url = "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE"
        version = requests.get(version_url).text

        if (platform.system() == "Windows"):
            url = "https://storage.googleapis.com/chrome-for-testing-public/" + version + "/win64/chromedriver-win64.zip"
            zip_name = "chromedriver-win64.zip"

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
                raise SystemExit(1)

            if os.path.exists(zip_file_path):
                os.remove(zip_file_path)

            exact_path = os.path.join(chromedriver_def_path, "chromedriver-win64/chromedriver.exe")

            try:
                shutil.copy(exact_path, chromedriver_def_path)
            except:
                raise SystemExit(1)

            exact_path = os.path.join(chromedriver_def_path, "chromedriver-win64")

            try:
                shutil.rmtree(exact_path)
            except:
                raise SystemExit(1)

            return chromedriver_def_path + "/chromedriver.exe"

        elif (platform.system() == "Linux"):
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
                raise SystemExit(1)

            if os.path.exists(zip_file_path):
                os.remove(zip_file_path)

            exact_path = os.path.join(chromedriver_def_path, "chromedriver-linux64/chromedriver")

            try:
                shutil.copy(exact_path, chromedriver_def_path)
            except:
                raise SystemExit(1)

            exact_path = os.path.join(chromedriver_def_path, "chromedriver-linux64")

            try:
                shutil.rmtree(exact_path)
            except:
                raise SystemExit(1)

            return chromedriver_def_path + "/chromedriver"
        else :
            print("\033[31m" + "COSINT is not supported by your operating system"  + "\033[0m")
            raise SystemExit(1)

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

class QueryMaker :
    def __init__(self, chromedriver_path):
        self.chromedriver_path = chromedriver_path
    def linkedin_query(self, wordlist):
        employees = self.linkedin_employee_query(wordlist.get("Employee"))
        mails = self.linkedin_mail_query(wordlist.get("Mail"))
        company_info = self.linkedin_company_query(wordlist.get("Company"))
        return {"Employees" : employees, "Mails" : mails, "Company" : company_info}

    def linkedin_employee_query(self, word):
        user_agent = UserAgent()
        random_agent = user_agent.random
        request_header = f"--user_agent={random_agent}"

        options = Options()
        options.add_argument(request_header)
        options.add_argument("--disable-gpu")
        #options.add_argument("--headless")
        options.page_load_strategy = "eager"

        service = Service(self.chromedriver_path)

        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(15)

        url = f"https://www.bing.com/search?q={word}"

        driver.get(url)
        sleep(2)

        all_links_obj = driver.find_elements(By.XPATH, "//a[@href]")
        filtered_links = []

        regex_control = re.compile(r"^https:\/\/(www|[a-z]{2,3})\.linkedin\.com\/in")
        for bing_link in all_links_obj:
            href = bing_link.get_attribute("href")
            text = bing_link.get_attribute("text")
            if (regex_control.search(href)) and (not "linkedin.com" in text):
                filtered_links.append([text, href])

        for linkedin_link in filtered_links:
            print(linkedin_link[0] + "  :  " + linkedin_link[1])


        sleep(30)


    def linkedin_company_query(self, wordlist):
        print()
    def linkedin_mail_query(self, wordlist):
        print()



if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--company", type=str, help="Company Name", required=True)
    parser.add_argument("-o", "--output", type=str, help="Output File Name", required=False)
    parser.add_argument("-d", "--domain", type=str, help="Domain Name", required=True)
    args = parser.parse_args()

    cli = CLI(args)